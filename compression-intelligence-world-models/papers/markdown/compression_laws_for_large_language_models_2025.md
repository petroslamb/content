|     |     | Compression    |     |     | Laws for            | Large | Language           | Models |     |     |
| --- | --- | -------------- | --- | --- | ------------------- | ----- | ------------------ | ------ | --- | --- |
|     |     | AyanSengupta*1 |     |     | SiddhantChaudhary*1 |       | TanmoyChakraborty1 |        |     |     |
Abstract (LLMs). Neural scaling laws (Kaplan et al., 2020; Hoff-
mannetal.,2022;Muennighoffetal.,2023)formalizethe
Weintroducecompressionlawsforlanguagelan-
relationshipsbetweenmodelperformance,size,data,and
| guagemodels(LLMs). |     |     | Whilerecentscalinglaws |     |     |     |     |     |     |     |
| ------------------ | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- |
5202 rpA 6  ]LC.sc[  1v24340.4052:viXra computational resources, revealing that performance im-
havesoughttounderstandhowLLMsscalewith
provesasthesefactorsarescaled.Recentstudies(Faizetal.,
respecttomodelsize,pre-trainingdata,andcom-
2024;Diaz&Madaio,2024;Villalobosetal.,2024)have
| putational | resources, |     | we focus | on understand- |     |     |     |     |     |     |
| ---------- | ---------- | --- | -------- | -------------- | --- | --- | --- | --- | --- | --- |
shownthatscalingupneuralnetworks,bothinmodelsize
| ing how | model | compression |     | affects the | perfor- |     |     |     |     |     |
| ------- | ----- | ----------- | --- | ----------- | ------- | --- | --- | --- | --- | --- |
anddatasetsize,resultsinalinearincreaseincomputational
manceofapre-trainedLLMondownstreamtasks.
|     |     |     |     |     |     | demands. | Thisimpliestheurgentneedforcomputationally |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | ------------------------------------------ | --- | --- | --- |
Weempiricallyexaminetheeffectsofstructured
|     |     |     |     |     |     | efficient | LLMs that | can achieve | high performance | while |
| --- | --- | --- | --- | --- | --- | --------- | --------- | ----------- | ---------------- | ----- |
modelcompressiononLLMsthroughover1000
minimizingresourceconsumption.
experimentsacrosseightmodelswithsizesrang-
ingfrom0.5B to14B parameters. Ourfindings Inattemptstomakelargepre-trainedmodelsmorecompute
efficient,modelcompression(akamodelpruning)hasbeen
indicatethatthetestcross-entropylossincreases
quadraticallywiththecompressionratio,whereas widelyadoptedforcompressinglargemodelsintosmaller
performanceondownstreamtasksdeclinesonly andcomputationallymorefeasiblevariants. Post-training
linearly. Ourstudyemphasizestheimportanceof modelcompressionmethods(Ashkboosetal.,2024;Wang
recoveryfine-tuninginenhancinggenerationloss, et al., 2024; Sengupta et al., 2025) prune various compo-
nentsofpre-trainedLLMstoreducetheirsize,oftenwith
showingthatthetestlossofcompressedLLMs
can improve by up to 55% with recovery fine- minimalimpactonperformancepost-compression. Despite
tuning. Athighercompressionratios(upto90%), the growing adoption of model compression techniques,
compressedLLMsdemonstrateaspeedincrease thereisstillnosystematicstudyonhowthesemethodsscale
of 60% during inference compared to their un- acrossdifferentLLMs. Toaddressthisgap,ourworkintro-
compressed counterparts, compensating for the ducescompressionlawsforLLMs,providingastructured
performancedegradationatthislevel. However, frameworktounderstandtheeffectivenessandscalability
for smaller models (≤ 7B), the computational ofstructuredcompressionmethods. Throughamultifaceted
approach,weanalyzethekeyfactorsthatinfluencetheper-
| gainsarelimited,peakingatjust35%. |     |     |     |     | Wecon- |     |     |     |     |     |
| --------------------------------- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
cludethatmodelcompressioncanbehighlybene- formancestabilityofLLMsaftercompression,bothwith
ficialforlargermodels,especiallywhenasmaller andwithoutrecoveryfine-tuning(vanderOuderaaetal.;Ma
modelwithinthesamecomputationalbudgetis etal.,2023). Ourgoalistoofferbothempiricalandanalyti-
notavailable. Theseinsightsprovidethepractical calinsightsintofivecriticalresearchquestionssurrounding
modelcompressionasfollows.
guidelinesforutilizingmodelcompressiontech-
niquesforadoptingLLMsinreal-lifeapplications
|     |     |     |     |     |     | RQ1. | Whatistheimpactofmodelcompressionondown- |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | ---------------------------------------- | --- | --- | --- |
inresource-constrainedsettings.
streamperformance?
|     |     |     |     |     |     | RQ2. | Whatcomputationalbenefitsdoescompressionpro- |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | -------------------------------------------- | --- | --- | --- |
vide?
1.Introduction
|     |     |     |     |     |     | RQ3. | Howmuchperformancecanberegainedwithre- |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | -------------------------------------- | --- | --- | --- |
coveryfine-tuning?
| In recent years, | there | has been | growing | interest | in under- |     |     |     |     |     |
| ---------------- | ----- | -------- | ------- | -------- | --------- | --- | --- | --- | --- | --- |
standinghowthesizeofpre-trainingmodelsanddatasetsim- RQ4. How can we determine which LLM to compress
andatwhatcompressionratiotoachievecomparableper-
pactsthedownstreamperformanceoflargelanguagemodels
formance?
| *Equal |     | 1Department |     |     |     |     |     |     |     |     |
| ------ | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
contribution of Electrical Engineer- RQ5. Iscalibrationnecessaryduringmodelcompression?
| ing, IIT Delhi, | India. | Correspondence |     | to: Ayan | Sengupta |     |     |     |     |     |
| --------------- | ------ | -------------- | --- | -------- | -------- | --- | --- | --- | --- | --- |
<ayan.sengupta@ee.iitd.ac.in>. Weconductover1000experimentsusingQwen-2.5(Qwen
etal.,2025)andLLaMA-3(Dubeyetal.,2024),withpa-
1

CompressionLawsforLargeLanguageModels
|     |       | ARC-c | Qwen2.5-0.5B |     |       | ARC-c    |     |  ot derapmoc pudeeps ecnerefnI |          |     |     |     |     |     |
| --- | ----- | ----- | ------------ | --- | ----- | -------- | --- | ------------------------------ | -------- | --- | --- | --- | --- | --- |
|     |       | 6 0   |              |     |       |          |     | )% ni( ledom desserpmocnu      |          |     |     |     |     |     |
|     | ARC-e | MMLU  |              |     | ARC-e | 6 0 MMLU |     | 60                             |          |     |     |     |     |     |
|     |       | 4 0   |              |     |       | 4 0      |     |                                | Qwen-14B |     |     |     |     |     |
20
|     |           |            |              |     |           |            |     | 50  | LLaMA-8B |     |     |     |     |     |
| --- | --------- | ---------- | ------------ | --- | --------- | ---------- | --- | --- | -------- | --- | --- | --- | --- | --- |
|     | Hellaswag | Winogrande |              |     | Hellaswag | Winogrande |     |     |          |     |     |     |     |     |
|     |           | PiQA       |              |     |           | PiQA       |     | 40  |          |     |     |     |     |     |
|     |           | ARC-c      | Qwen2.5-1.5B |     |           | A8R0C-c    |     | 30  |          |     |     |     |     |     |
6 0
|     | ARC-e | MMLU |     |     | ARC-e | 6 0 MMLU |     |     |     |     |     |     |     |     |
| --- | ----- | ---- | --- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |       | 4 0  |     |     |       | 4 0      |     | 20  |     |     |     |     |     |     |
20
10
|     | Hellaswag | Winogrande |     |     | Hellaswag | Winogrande |     |     |     |     |     |     |     |     |
| --- | --------- | ---------- | --- | --- | --------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |           | PiQA       |     |     |           | PiQA       |     |     |     |     |     |     |     |     |
0
|     |       |             |            |     |       |             |     |     | 10% | 30%               | 50% | 70% | 90% |     |
| --- | ----- | ----------- | ---------- | --- | ----- | ----------- | --- | --- | --- | ----------------- | --- | --- | --- | --- |
|     |       | A 8 R 0 C-c | Qwen2.5-3B |     |       | A 8 R 0 C-c |     |     |     |                   |     |     |     |     |
|     |       | 6 0         |            |     |       | 6 0         |     |     |     | Compression ratio |     |     |     |     |
|     | ARC-e | 4 0 MMLU    |            |     | ARC-e | MMLU        |     |     |     |                   |     |     |     |     |
4 0
|     |     | 20  |     |     |     | 20  |                   |     |         |     |               |     |          |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | ------- | --- | ------------- | --- | -------- | --- |
|     |     |     |     |     |     |     | Figure2.Inference |     | speedup |     | of compressed |     | Qwen-14B | and |
Hellaswag Winogrande Hellaswag Winogrande LLaMA-8B (the two largest models used in the study) models
|     |     | PiQA |     |     |     | PiQA |     |     |     |     |     |     |     |     |
| --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
comparedtothecorrespondinguncompressedmodels.Athigher
|     |     | A R C-c |     |     |     | A R C-c |     |     |     |     |     |     |     |     |
| --- | --- | ------- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
8 0 Qwen2.5-7B 8 0 compressionratios,extrinsicperformancedeclinessignificantly
|     |     | 6 0 |     |     |     | 6 0 |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ARC-e 4 0 MMLU ARC-e 4 0 MMLU (over 40%) for large models (>7B parameters). However, the
|     |     | 20  |     |     |     | 20  |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
inferencespeedupcompensatesforthisperformancedrop.
|     | Hellaswag | Winogrande |             |     | Hellaswag | Winogrande |     |     |     |     |     |     |     |     |
| --- | --------- | ---------- | ----------- | --- | --------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |           | PiQA       |             |     |           | PiQA       |     |     |     |     |     |     |     |     |
|     |           | A R C-c    | Qwen2.5-14B |     |           | A R C-c    |     |     |     |     |     |     |     |     |
|     |           | 8 0        |             |     |           | 8 0        |     |     |     |     |     |     |     |     |
|     | ARC-e     | 6 0 MMLU   |             |     | ARC-e     | 6 0 MMLU   |     |     |     |     |     |     |     |     |
|     |           | 4 0        |             |     |           | 4 0        |     |     |     |     |     |     |     |     |
|     |           | 20         |             |     |           | 20         |     |     |     |     |     |     |     |     |
fine-tuningsizeDanduncompressedmodelperformance
|     | Hellaswag | Winogrande |     |     | Hellaswag | Winogrande |     |                                                  |     |     |     |     |     |     |
| --- | --------- | ---------- | --- | --- | --------- | ---------- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- |
|     |           | PiQA       |     |     |           | PiQA       | L   | 0 usingapower-lawexpression(moredetailsinSection |     |     |     |     |     |     |
3). Thekeyinsightsfromourstudyaddressingfiveresearch
|     |       | ARC-c | Llama-3.2-1B |     |       | ARC-c |                            |     |     |     |     |     |     |     |
| --- | ----- | ----- | ------------ | --- | ----- | ----- | -------------------------- | --- | --- | --- | --- | --- | --- | --- |
|     |       | 60    |              |     |       | 60    |                            |     |     |     |     |     |     |     |
|     | ARC-e | MMLU  |              |     | ARC-e | MMLU  | questionsareoutlinedbelow: |     |     |     |     |     |     |     |
|     |       | 40    |              |     |       | 40    |                            |     |     |     |     |     |     |     |
20
RQ1. Evenintheabsenceofrecoveryfine-tuning,LLMs
Hellaswag Winogrande Hellaswag Winogrande compressedataratiooflessthan50%canretain57%of
|     |     | PiQA |     |     |     | PiQA |                                    |     |     |     |     |                   |     |     |
| --- | --- | ---- | --- | --- | --- | ---- | ---------------------------------- | --- | --- | --- | --- | ----------------- | --- | --- |
|     |     |      |     |     |     |      | theiroriginalextrinsicperformance. |     |     |     |     | Whenrecoveryisap- |     |     |
ARC-c Llama-3.2-3B A8R0C-c plied,theperformancerecoveryincreasesto84%(c.f. Fig-
|     |       | 6 0      |     |     |       | 6 0  |        |     |     |     |     |     |     |     |
| --- | ----- | -------- | --- | --- | ----- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- |
|     | ARC-e | 4 0 MMLU |     |     | ARC-e | MMLU |        |     |     |     |     |     |     |     |
|     |       |          |     |     |       | 4 0  | ure1). |     |     |     |     |     |     |     |
20
|     |     |     |     |     |     |     | RQ2. | For | compression | ratios | ranging | from | 50% | to 90%, |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | ----------- | ------ | ------- | ---- | --- | ------- |
Hellaswag Winogrande Hellaswag Winogrande inferencetimeimprovesby24%to35%. Forlargermodels
|     |     | PiQA |     |     |     | PiQA |     |     |     |     |     |     |     |     |
| --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
(>7Bparameters),thespeedupcanreachupto60%(illus-
|     |       | A R C-c  |                 |     |       | A R C-c  |                   |     |     |     |     |     |     |     |
| --- | ----- | -------- | --------------- | --- | ----- | -------- | ----------------- | --- | --- | --- | --- | --- | --- | --- |
|     |       | 8 0      | Meta-Llama-3-8B |     |       | 8 0      | tratedinFigure2). |     |     |     |     |     |     |     |
|     |       | 6 0      |                 |     |       | 6 0      |                   |     |     |     |     |     |     |     |
|     | ARC-e | 4 0 MMLU |                 |     | ARC-e | 4 0 MMLU |                   |     |     |     |     |     |     |     |
20 20 RQ3. Recovery fine-tuning can enhance intrinsic perfor-
|     |           |            |     |     |           |            | mance      | by  | 63%, while                            | extrinsic | performance |     | is  | improved |
| --- | --------- | ---------- | --- | --- | --------- | ---------- | ---------- | --- | ------------------------------------- | --------- | ----------- | --- | --- | -------- |
|     | Hellaswag | Winogrande |     |     | Hellaswag | Winogrande |            |     |                                       |           |             |     |     |          |
|     |           |            |     |     |           |            | byonly14%. |     | Wealsomeasurecriticalcompressionratio |           |             |     |     |          |
|     |           | PiQA       |     |     |           | PiQA       |            |     |                                       |           |             |     |     |          |
(compressionthresholdbeyondwhichrecoveryisnotpossi-
|     |     | Compression 0%  | Compression 30% |     | Compression 70% |     |                       |     |     |     |     |     |     |     |
| --- | --- | --------------- | --------------- | --- | --------------- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- |
|     |     | Compression 10% | Compression 50% |     | Compression 90% |     | ble)fordifferentLLMs. |     |     |     |     |     |     |     |
RQ4. Whenmaintainingasimilarparameterbudget,com-
Figure1.Zero-shotaccuracyofcompressedQwenandLLaMA
pressingsmallermodels(<3B)atalowercompressionra-
| models | without | (left) | and with | (right) | recovery | fine-tuning for |     |     |     |     |     |     |     |     |
| ------ | ------- | ------ | -------- | ------- | -------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
tioresultsinan8%performancegaincomparedtocompress-
calibration-freemodelcompression(seeFigure8inAppendixD.1
|     |     |     |     |     |     |     | inglargermodels(>3B)atahigherratio. |     |     |     |     |     | Notably,smaller |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- | --- | --------------- | --- |
forcalibrationresults)ondifferentextrinsictasks.
LLMsexhibitahigherextrinsiccriticalcompressionratio,
allowingforgreaterrecoverypotentialpost-compression.
| rameter | size | ranging | from | 0.5B | to 14B. | These models |     |     |     |     |     |     |     |     |
| ------- | ---- | ------- | ---- | ---- | ------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
RQ5. Ourempiricalfindingssuggestthatcalibration-free
arecompressedusingbothcalibration-free(Senguptaetal.,
|     |     |     |     |     |     |     | methods | perform | competitively |     | against | calibration-based |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------- | ------------- | --- | ------- | ----------------- | --- | --- |
2025)andcalibration-based(Ashkboosetal.,2024)struc-
compressionmethods,particularlyinextrinsicevaluation.
| tured | pruning | methods, | with | compression |     | ratios ranging |     |     |     |     |     |     |     |     |
| ----- | ------- | -------- | ---- | ----------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
from10%to90%andrecoveryfine-tuningtokensizesvary- Thecompressionlawsintroducedinthispaperprovidesys-
ingfrom1M to25M. Following Kaplanetal.(2020),we tematicandpracticalguidelinesforemployingmodelcom-
fitthecompressedmodels’performanceL(bothintrinsic pressiontechniquestoadoptLLMsinresource-limited,real-
| andextrinsic)asafunctionofcompressionratior,recovery |     |     |     |     |     |     | worldapplications. |     |     |     |     |     |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- |
2

CompressionLawsforLargeLanguageModels
| 2.RelatedWork      |     |     |                                |     |     | domsubsetofthepre-trainedcomponents.   |     |     |     |     |            |     |
| ------------------ | --- | --- | ------------------------------ | --- | --- | -------------------------------------- | --- | --- | --- | --- | ---------- | --- |
|                    |     |     |                                |     |     | Scalinglawsforparameter-efficientLLMs. |     |     |     |     | Kumaretal. |     |
| Neuralscalinglaws. |     |     | Thestudyofscalinglawsdatesback |     |     |                                        |     |     |     |     |            |     |
several decades, with Cortes et al. (1993) introducing an (2024)introducedprecision-awarescalinglaws,demonstrat-
asymptoticapproachtoanalyzethegeneralizationerrorof ingthattraininginlowerprecisioneffectivelyreducesthe
neuralnetworksasafunctionoftrainingstepsanddataset parametercountofLLMs. Theirfindingssuggestthatlarger
size. Later, Hestnessetal.(2017)andsubsequently Rosen- LLMsscalemoreefficientlywhentrainedatlowerpreci-
|     |     |     |     |     |     | sion. | Recently, |     | Chenetal.(2024)analyzedthescalinglaw |     |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --------- | --- | ------------------------------------ | --- | --- | --- |
feldetal.(2019)studiedthescalingofgeneralizationca-
pabilitiesofdeepneuralnetworksfordifferentmodelsand of recovery fine-tuning on LLMs compressed with struc-
datascales. Kaplanetal.(2020)proposedaclosedfunc- tured pruning methods. While the primary focus of their
tionalformL∼N−α+D−β (akaKaplanscalinglaw)for study was to identify the extent of recovery required for
estimatingtestlossofalargepre-trainedlanguagemodel improvingthepost-recoveryloss, ourstudytacklesmore
|                               |     |     |     |                     |     | fundamental |     | aspects | of model | compression. | We  | present |
| ----------------------------- | --- | --- | --- | ------------------- | --- | ----------- | --- | ------- | -------- | ------------ | --- | ------- |
| usingnumberofmodelparametersN |     |     |     | andpre-trainingdata |     |             |     |         |          |              |     |         |
sizeD,arguingthatmodellossdecreasesforlargermod- ananalyticalframeworkforassessingtheeffectivenessof
els pre-trained on larger corpus. Hoffmann et al. (2022) structuredmodelcompressionondifferentLLMsinterms
ofpost-compressionperformancestability,performancere-
proposedaconstrainedfunctionalformwithanadditional
fixedcomputationbudgetC ∼N·D. TheirproposedChin- covery,andcomputationalupsides.
| chilla scaling  |     | laws hypothesize |        | that smaller    | models with |               |     |     |     |     |     |     |
| --------------- | --- | ---------------- | ------ | --------------- | ----------- | ------------- | --- | --- | --- | --- | --- | --- |
| higher training |     | token            | counts | tend to perform | better. Ca- | 3.Methodology |     |     |     |     |     |     |
balleroetal.(2023)arguedthatthefunctionalformused
3.1.ParametrizationoftheLLMcompressionlaw
| in Kaplan | scaling   | law | is monotonic | and         | fails to capture |     |     |     |     |     |     |     |
| --------- | --------- | --- | ------------ | ----------- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
| emergent  | phenomena |     | and phase    | transitions | in deep neu-     |     |     |     |     |     |     |     |
Withcompressionlaws,weproposeaseriesofanalytical
ralnetworks,includingpre-trainedTransformers(Vaswani,
methodsforestimatingtheintrinsic(e.g.,testcross-entropy
2017). Whilemostofthesescalinglawsmanagetocapture
|     |     |     |     |     |     | loss) | and | extrinsic | (e.g., zero-shot | test accuracy) |     | perfor- |
| --- | --- | --- | --- | --- | --- | ----- | --- | --------- | ---------------- | -------------- | --- | ------- |
theexpectedtest-timebehaviorsofpre-trainedLLMs,they
manceofLLMspost-compression.Buildingonpriorstudies
failtoexplainthescalingbehaviorsofmodelsinparameter
(Kaplanetal.,2020;Hoffmannetal.,2022)thatestablish
anddata-efficientsettings.
|     |     |     |     |     |     | scaling | laws | for | LLM pre-training, | we formulate |     | a rela- |
| --- | --- | --- | --- | --- | --- | ------- | ---- | --- | ----------------- | ------------ | --- | ------- |
Modelcompressionforparameterefficiency. Despitethe tionshipbetweentheperformanceofacompressedmodel
remarkableperformanceofLLMssuchasLLaMA(Dubey anditscorrespondingbasemodelthroughalawdefinedby
etal.,2024)andDeepseek(DeepSeek-AIetal.,2024)ona threekeyparameters: theperformanceofthebasemodel
widerangeoftasks,includingnaturallanguageinference, on a task (denoted by L 0 ), the compression ratio used to
complexreasoning, summarization, translation, andcode compressthemodel(denotedbyr ∈(0,1)),andthenum-
generation,large-scaleutilizationofthesemodelsremains beroftokensinthedataset(datasetsize)usedforrecovery
challenging due to high computational resource require- fine-tuning (RFT) of the compressed model (denoted by
ments. Model compression (aka pruning) is a common D ∈ [0,∞)); we denote the relationship by the notation
techniquetoreducetheparametercountinpre-trainedmod- L:=L(L 0 ,r,D),whereLrepresentstheperformanceof
els,improvingtheircomputationalefficiencyandspeed. It thecompressedmodel. Ourproposedcompressionlawcan
beusedtodeterminetheoptimalvaluesofrandDneeded
| generallyfallsintotwomaincategories: |     |     |     |     | unstructuredand |     |     |     |     |     |     |     |
| ------------------------------------ | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- |
structured pruning. Unstructured pruning focuses on re- toobtainawell-performingcompressedmodel,maximizing
movingindividualweights(Frantar&Alistarh,2023;Sun theperformanceretainmentpost-compression.
| et al., 2023) | from | pre-trained |     | models. Despite | their abil- |     |     |     |     |     |     |     |
| ------------- | ---- | ----------- | --- | --------------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
Thefunctionalformofourparametrizationisdescribedby
| ity to retain | performance |     | post-compression, |     | unstructured |     |     |     |     |     |     |     |
| ------------- | ----------- | --- | ----------------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
thefollowingequation:
pruningoftendemandshardware-specificoptimizationsand
|                                                      |     |     |     |     |     |     |     |                |     | (cid:18) | (cid:19)γ |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | -------- | --------- | --- |
| maynotalwaysleadtosubstantialcomputationalbenefits.  |     |     |     |     |     |     |     |                |     |          | 1         |     |
|                                                      |     |     |     |     |     |     | L(L | ,r,D)=Lα(1+r)β |     | 1+       |           | (1) |
| Conversely,structuredpruningeliminatesentirechannels |     |     |     |     |     |     |     | 0              | 0   |          |           |     |
D+ϵ
orcomponents,makingitmoresuitableforabroaderrange
|     |     |     |     |     |     |     | α,  | β, γ | ϵ   |     | ϵ > | 0   |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
ofhardwareconfigurations. Contemporarystructureprun- where and are all real numbers, and is a
constantaddedtothedatasetsizeDtoconsiderthebound-
ingmethodslikeSliceGPT(Ashkboosetal.,2024),layer
|     |     |     |     |     |     | arycaseofnoRFT.Wetypicallysetϵ=1. |     |     |     |     | Thischoiceof |     |
| --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | --- | ------------ | --- |
collapse(Yangetal.,2024)useasmallcalibrationdataset
toassesstheimportanceofdifferentcomponentsofapre- parametrizationofthefunctionalformofthecompression
lawisbasedonthefollowingprinciples,whichwecallthe
| trained | model | and removes |     | them subsequently, | if found |     |     |     |     |     |     |     |
| ------- | ----- | ----------- | --- | ------------------ | -------- | --- | --- | --- | --- | --- | --- | --- |
feasibilityconditionsofacompressionlaw:
| unimportant. |     | Sengupta | et  | al. (2025) proposed | a policy- |     |     |     |     |     |     |     |
| ------------ | --- | -------- | --- | ------------------- | --------- | --- | --- | --- | --- | --- | --- | --- |
drivencalibration-freemodelcompressionmethodandar-
• Weformulatethecompressionlawasapowerlawwith
guedthatLLMscanwithstandevenwhenprunedbyaran- respect to the mentioned parameters. However, unlike
3

CompressionLawsforLargeLanguageModels
thefunctionalformsinpre-trainingscalinglaws,partic- noisemodeledbytheunitnormaldistribution. Overall,the
ularlyinChinchillascaling(Hoffmannetal.,2022),we regressionproblemcanbestatedas:
|     | hypothesize                               | that the functional |     | form | governing | a com- |            |     |                  |     |     |     |       |
| --- | ----------------------------------------- | ------------------- | --- | ---- | --------- | ------ | ---------- | --- | ---------------- | --- | --- | --- | ----- |
|     |                                           |                     |     |      |           |        | logL=αlogL |     | +βlogr′+γlogD′+ϵ |     |     |     | (5)   |
|     | pressionlawmustbescaleinvariantw.r.trandL |                     |     |      |           | ,i.e., |            |     | 0                |     |     |     | noise |
0
|     | L(L ,r,D)mustbeahomogeneousfunctionofrandL |     |     |     |     |     | .      |          |     |     |     |     |     |
| --- | ------------------------------------------ | --- | --- | --- | --- | --- | ------ | -------- | --- | --- | --- | --- | --- |
|     | 0                                          |     |     |     |     | 0   | whereϵ | ∼N(0,1). |     |     |     |     |     |
noise
Suchalawallowsustoderiveoptimaldecisionregionsfor
choosingrandD,givenasuitableconstraintontheper-
3.3.Thecriticalcompressionratio
|     |               |                         |     |     | (cid:16) | (cid:17)γ |     |     |     |     |     |     |     |
| --- | ------------- | ----------------------- | --- | --- | -------- | --------- | --- | --- | --- | --- | --- | --- | --- |
|     | formancedrop. | Atermsimilartothefactor |     |     | 1+       | 1         | ,   |     |     |     |     |     |     |
D+1
Wenowuseourproposedcompressionlawtoderivecondi-
relatingtheperformanceofthecompressedmodeltothe
RFTdatasetsize,alsoappearsasanadditiveterminpre- tionsonrandDunderwhichrecoveryofthecompressed
|     |     |     |     |     |     |     | modelispossible. |     | Forsimplicity(andwithoutlossofgen- |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ---------------------------------- | --- | --- | --- | --- |
trainingscalinglaws.
erality),weworkwithmodelaccuracyastheperformance
| •   | Withoutanycompression(i.e.,asr |     |     |     | → 0)andRFT(i.e., |     |     |     |     |     |     |     |     |
| --- | ------------------------------ | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
measure. Thefollowingtheoremestablishesalowerbound
asD →0),thefunctionalformmustrecovertheperfor-
onthesizeoftheRFTdatasetDwhichisneededtorecover
manceofthebasemodel.
L
• Thepost-compressionaccuracy(orloss)shoulddecrease a compressed model’s accuracy w.r.t the base model’s
|     |                                                   |               |            |     |                  |     | accuracy                | Lα upto | a recovery | threshold |     | of σ, | i.e., a lower |
| --- | ------------------------------------------------- | ------------- | ---------- | --- | ---------------- | --- | ----------------------- | ------- | ---------- | --------- | --- | ----- | ------------- |
|     | (orincrease)withanincreaseinthecompressionratior, |               |            |     |                  |     |                         | 0       |            |           |     |       |               |
|     |                                                   |               |            |     |                  |     | boundonDwhichguarantees |         |            | L         | ≥σ. |       |               |
|     | i.e., ∂L                                          | < 0 (or > 0). | Similarly, | the | post-compression |     |                         |         |            | L         | α   |       |               |
|     | ∂r                                                |               |            |     |                  |     |                         |         |            |           | 0   |       |               |
accuracy(orloss)shouldincrease(ordecrease)withan Theorem3.1. ConsiderthecompressionlawL=Lα(1+
|     |            |                        |           |          |                |               | (cid:16) | (cid:17)γ |                           |     |     |     | 0      |
| --- | ---------- | ---------------------- | --------- | -------- | -------------- | ------------- | -------- | --------- | ------------------------- | --- | --- | --- | ------ |
|     | i nc re as | e in th e si z e o f t | h e R F T | dat a se | t D , i . e ., | ∂ L > 0 ( o r |          |           |                           |     |     |     |        |
|     |            |                        |           |          |                | ∂ D           | r)β 1+   | 1         | foramodelclass,whereLandL |     |     |     | repre- |
< 0 ). F ro m t he f u n c ti o n a l fo rm i n E q ua t i o n 1 , it is ea s y D +1 0
senttheaccuracyofthecompressedandthebasemodels,
toseethattheserelationsshouldbeeffectivelycaptured
|     |                                                   |     |     |                    |     |      | respectively.                                 | Further,assumethatthescalinglawsatisfies |     |     |     |     |          |
| --- | ------------------------------------------------- | --- | --- | ------------------ | --- | ---- | --------------------------------------------- | ---------------------------------------- | --- | --- | --- | --- | -------- |
|     | bythesignsoftheexponentsβ                         |     |     | andγ,respectively. |     | More |                                               |                                          |     |     |     |     |          |
|     |                                                   |     |     |                    |     |      | feasibilityconditionsw.r.tmodelaccuracy,i.e., |                                          |     |     |     |     | ∂L ≥0and |
|     | specifically,formodelaccuracy,itisrequiredthatβ,γ |     |     |                    |     | <    |                                               |                                          |     |     |     |     | ∂D       |
|     |                                                   |     |     |                    |     |      | ∂L ≤0,whichisequivalenttotheconditionsβ,γ     |                                          |     |     |     |     | <0. Let  |
|     | 0,whereasformodelloss,β,γ                         |     |     | >0musthold.        |     |      | ∂r                                            |                                          |     |     |     |     |          |
L
|     |     |     |     |     |     |     | σ ∈ (0,1)bearecoverythreshold. |     |     |     | Then, |     | ≥ σ ifand |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------ | --- | --- | --- | ----- | --- | --------- |
Lα
| Ablationcompressionlaws. |     |     | Inconjunctionwithourpri- |     |     |     |     |     |     |     |     | 0   |     |
| ------------------------ | --- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
onlyifDsatisfies1
marycompressionlawinEquation1,wealsoperformabla-
| tionstudiestofitthefollowingparametrizations: |     |     |     |     |     |     |     |     | 1       |                 |     |      |     |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --------------- | --- | ---- | --- |
|                                               |     |     |     |     |     |     |     |     | (cid:2) | σ(1+r)−β(cid:3) |     | 1    |     |
|                                               |     |     |     |     |     |     |     |     | ≤       |                 |     | γ −1 | (6) |
D+1
|     |     | L(L ,r)=Lα(1+r)β |          |     |           | (2) |                                                        |     |     |     |     |     |     |
| --- | --- | ---------------- | -------- | --- | --------- | --- | ------------------------------------------------------ | --- | --- | --- | --- | --- | --- |
|     |     | 0                | 0        |     |           |     |                                                        |     |     |     |     |     |     |
|     |     |                  | (cid:18) |     | (cid:19)γ |     |                                                        |     |     |     |     |     |     |
|     |     |                  |          |     | 1         |     | Asacorollaryofthistheorem,wehavethefollowingimpor-     |     |     |     |     |     |     |
|     |     | L(L ,D)=Lα       | 1+       |     |           | (3) |                                                        |     |     |     |     |     |     |
|     |     | 0                | 0        |     |           |     | tantresult,whichessentiallystatesthatforalargerecovery |     |     |     |     |     |     |
D+1
|     |     |     |     |     |     |     | thresholdσ | ∈(0,1)andlargecompressionratiosr,recov- |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --------------------------------------- | --- | --- | --- | --- | --- |
eringamodelusingRFTisnotpossible.
Usingtheseablationstudies,weempiricallyhighlightthe
|                                        |     |     |     |     |           |     | Corollary3.2. |     | ConsiderthesettingofTheorem3.1. |     |     |     | Define |
| -------------------------------------- | --- | --- | --- | --- | --------- | --- | ------------- | --- | ------------------------------- | --- | --- | --- | ------ |
| significanceofboththecompressionratior |     |     |     |     | andtheRFT |     |               |     |                                 |     |     |     |        |
1
datasetsizeDasparametersinthecompressionlaw. r critical (σ) := σβ −1,whichwecallthecriticalcompres-
|     |     |     |     |     |     |     | sion ratio | for | recovery threshold |     | σ   | ∈ (0,1). | Then the |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ------------------ | --- | --- | -------- | -------- |
followinghold:
| 3.2.Fittingthecompressionlaw: |     |     |     | Ordinaryleastsquares |     |     |     |     |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
forlinearregression
(0,2β),
|     |     |     |     |     |     |     | 1. If | σ ∈ | then | for any | compression |     | ratio r ∈ |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | ---- | ------- | ----------- | --- | --------- |
TakinglogarithmsonbothsidesofEquation1,weobtain
(0,1),thereexistsDsuchthatRFTonthecompressed
the following (for the sake of brevity, we only use L to modelwithadatasetsizeofDwillresultin L ≥σ.
Lα
| representtheLHSoftheequation): |            |                   |     |     |          |          |                                           |                     |     |       |           |              | 0       |
| ------------------------------ | ---------- | ----------------- | --- | --- | -------- | -------- | ----------------------------------------- | ------------------- | --- | ----- | --------- | ------------ | ------- |
|                                |            |                   |     |     |          |          | 2. Ifσ                                    | ∈[2β,1),thenforanyr |     |       | ≥r        | (σ),noamount |         |
|                                |            |                   |     |     | (cid:18) | (cid:19) |                                           |                     |     |       | critical  |              |         |
|                                |            |                   |     |     |          | 1        | ofRFTcanrecoverthecompressedmodelaccuracy |                     |     |       |           |              |         |
|                                | logL=αlogL | 0 +βlog(1+r)+γlog |     |     | 1+       | (4)      |                                           |                     |     |       |           |              |         |
|                                |            |                   |     |     | D+1      |          |                                           |                     | L   |       |           |              |         |
|                                |            |                   |     |     |          |          | L                                         | to satisfy          | ≥   | σ. On | the other | hand,        | for any |
Lα 0
|                                                   |     |     |     |     |     |     | r < | r        | ,thereisalargeenoughDsuchthatRFT |     |     |     |     |
| ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | -------- | -------------------------------- | --- | --- | --- | --- |
| Inotherwords,fittingthecompressionlawasoutlinedby |     |     |     |     |     |     |     | critical |                                  |     |     |     |     |
|                                                   |     |     |     |     |     |     |     |          |                                  |     |     | L   | 2   |
Equation1transformsintoalinearregressionproblemin withadatasetofsizeDwillresultin ≥σ.
Lα
0
| thelogarithmicspace. |     | Theregressionisperformedonthe |     |       |          |          |                                                  |             |        |       |            |     |              |
| -------------------- | --- | ----------------------------- | --- | ----- | -------- | -------- | ------------------------------------------------ | ----------- | ------ | ----- | ---------- | --- | ------------ |
|                      |     |                               |     |       | (cid:16) | (cid:17) |                                                  |             |        |       |            |     |              |
|                      |     |                               |     |       |          | 1        | As an                                            | application | of the | above | corollary, |     | consider the |
| variables            |     | L , r′ := (1+r)               | and | D′ := | 1+       | . To     |                                                  |             |        |       |            |     |              |
|                      |     | 0                             |     |       |          | D+1      | LLaMA-3-8Bmodelwiththecompressionlawforextrinsic |             |        |       |            |     |              |
learnα,βandγ,weusethestandardordinaryleastsquares
(OLS)method(Zdaniuk,2014),whereinwealsotakeinto 1RefertoSectionA.1inAppendixfortheproof.
account the standard assumption of unobserved random 2RefertoSectionA.2inAppendixfortheproof.
4

CompressionLawsforLargeLanguageModels
Alpaca Alpaca datasetwillensure L ≥ σ. Next,supposeσ ≥ 0.441;
L0.98
12 Qwen2.5-0.5B forconcreteness,sayσ 0 =0.8. Then,weseethatthecritical
8 4
4 1 compression ratio is r critical = (0.8)1 − .1 1 8 −1 ≈ 0.208. In
otherwords, forcompressionratioshigherthan20%, we
PTB WikiText2 PTB WikiText2 cannotrecovermorethan80%ofthemodelperformance
Alpaca Alpaca usingRFT.
16 Qwen2.5-1.5B
12 4
8
4 ExperimentalSetup
1
In developing the compression laws, we compress var-
PTB WikiText2 PTB WikiText2
ious LLMs, including Qwen-2.5 (Qwen et al., 2025)
Alpaca Alpaca
12 Qwen2.5-3B (with variants of 0.5B, 1.5B, 3B, 7B, and 14B) and
4
8
LLaMA-3 (Dubey et al., 2024) (3.2-1B, 3.2-3B, and
4
1 1 3-8B variants). All the pre-trained model checkpoints
were accessed using Huggingface 3. We utilize random-
PTB WikiText2 PTB WikiText2
PruneNet (Sengupta et al., 2025) for the calibration-free
Alpaca Alpaca
12 Qwen2.5-7B compressionandSliceGPT(Ashkboosetal.,2024)forthe
4
8 calibration-based compression, applying compression ra-
4
1 1 tios of {10%,30%,50%,70%,90%}. As SliceGPT does
notsupportQwenarchitectures,weusethemethodonlyfor
PTB WikiText2 PTB WikiText2
LLaMAseriesmodels. Weexplicitlyexcludeunstructured
Alpaca Alpaca
pruningmethods(Frantar&Alistarh,2023)fromourstudy,
16 Qwen2.5-14B
12 4 as they lack the flexibility required to accommodate the
8
4 1 1 diversemodelfamiliesandcompressionratiosconsidered
in our analysis. For intrinsic evaluation, we use the test
PTB WikiText2 PTB WikiText2 setsfromtheWikiText2(Merityetal.,2016),PTB(Marcus
Alpaca Alpaca et al., 1993), and Alpaca (Taori et al., 2023) datasets on
12 Llama-3.2-1B
8 4 language modeling. For extrinsic evaluation, we use five
4 commonsense reasoning tasks: PIQA (Bisk et al., 2020),
1
WinoGrande(Sakaguchietal.,2021),HellaSwag(Zellers
PTB WikiText2 PTB WikiText2 etal.,2019),ARC-e,andARC-c(Clarketal.,2018)and
Alpaca Alpaca MMLU(Hendrycksetal.,2020)forevaluatingzero-shot
12 Llama-3.2-3B accuracyofcompressedLLMs. Thesetasksareevaluated
8
4 usingtheLMEvaluationHarnesssuite(Gaoetal.,2024)4.
1
Recoveryfine-tuningisperformedonthetrainingsetsof
PTB WikiText2 PTB WikiText2 theWikiText2,PTB,andAlpacadatasets,withamaximum
Alpaca Alpaca sequence length of 1024 and data sizes of {1k,4k,25k}.
12 Meta-Llama-3-8B WeimplementLoRA(Huetal.,2022)witharankof16for
8 4 fine-tuningthecompressedLLMsduringrecoveryandfine-
4
1 1
tuningthemodelsforoneepoch. Table5ofAppendixC
highlightsthetotalexperimentcount. Allexperimentswere
PTB WikiText2 PTB WikiText2
conductedonasingleNvidiaA100-80GBGPU.
Compression 0% Compression 30% Compression 70%
Compression 10% Compression 50% Compression 90%
4.ExperimentalResults
Figure3.Testloss(intrinsicevaluation)withcompressedLLMs
(calibration-free) without (left) and with (right) recovery fine- IntrinsicandextrinsicperformanceofLLMs. Figure3
tuning (with-calibration results are shown in Figure 7 of Ap- highlights the test cross-entropy loss for different LLMs
pendixD.1). when compressed with the calibration-free compression
methodatdifferentcompressionratios. Withoutrecovery
evaluation(i.e.,theaccuracyofthemodelondownstream fine-tuning,theintrinsicperformanceofLLMscandropby
generative tasks; see Table 2). We have α = 0.98, β = even1500%athighercompressionratios(> 50%). How-
−1.18andγ = −0.14. Hence, wehavethat2β ≈ 0.441.
3https://huggingface.co/models
Applying the above corollary, we see that if σ < 0.441,
4TaskdescriptionscanbefoundinAppendixB.
thenforanycompressionratior,RFTwithalargeenough
5

CompressionLawsforLargeLanguageModels
| Form |     |     |     |     | Intrinsic |     |     |     |     | Extrinsic |     |     |     |
| ---- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --------- | --- | --- | --- |
FittedFunction Adj.R2 F-Statistics FittedFunction Adj.R2 F-Statistics
|     |     |     |     | (cid:16) | (cid:17)1.16 |     |     |     |     | (cid:16) (cid:17)−0.14 |     |     |     |
| --- | --- | --- | --- | -------- | ------------ | --- | --- | --- | --- | ---------------------- | --- | --- | --- |
L=f(L0,r,D) L=L0 .63(r+1)1.72 1+ 1 0.96 5114 L=L0 .98(r+1)−1.03 1+ 1 0.99 22420
|     |     | 0   |     |     | D +1 |     |     | 0   |     | D +1 |     |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | ---- | --- | --- | --- |
L=f(L0,r) L=L0 .74(r+1)2.02 0.89 2720 L=L1 .01(r+1)−1.05 0.98 28000
|           |     | 0    |              |                |     |           |      | 0   |                          |     |      |     |      |
| --------- | --- | ---- | ------------ | -------------- | --- | --------- | ---- | --- | ------------------------ | --- | ---- | --- | ---- |
|           |     | L=L1 | .30 (cid:16) | 1 (cid:17)1.46 |     |           | L=L1 | .73 | (cid:16) 1 (cid:17)−0.22 |     |      |     |      |
| L=f(L0,D) |     | 0    | 1+ D         | +1             |     | 0.86 1991 |      | 0   | 1+ D +1                  |     | 0.93 |     | 5320 |
Table1.FittedcompressionlawsonintrinsicandextrinsicperformanceofcompressedLLMs. HigheradjustedR2 andF-statistics
indicatebettergoodness-of-fitforthefunctionalformL=f(L ,r,D),highlightingthenecessityofallthevariablesindeterminingthe
0
post-compressionperformance.
| Type | Model         |     | α    | β    | γ    | Adj.R2 |                               |             |             |                            |           |                   |        |
| ---- | ------------- | --- | ---- | ---- | ---- | ------ | ----------------------------- | ----------- | ----------- | -------------------------- | --------- | ----------------- | ------ |
|      |               |     |      |      |      |        | based                         | compression | method      | is                         | much less | effective         | during |
|      | Qwen-2.5-0.5B |     | 0.67 | 1.68 | 1.16 | 0.98   |                               |             |             |                            |           |                   |        |
|      |               |     |      |      |      |        | extrinsicevaluation(c.f.      |             |             | Figure8inAppendixD.1),with |           |                   |        |
|      | Qwen-2.5-1.5B |     | 0.66 | 1.48 | 0.97 | 0.97   |                               |             |             |                            |           |                   |        |
|      |               |     |      |      |      |        | maximum                       | 72%         | performance | recovery                   |           | post-compression, |        |
|      | Qwen-2.5-3B   |     | 0.67 | 1.47 | 0.89 | 0.96   |                               |             |             |                            |           |                   |        |
|      | Qwen-2.5-7B   |     | 0.66 | 1.61 | 0.56 | 0.95   | evenafterrecoveryfine-tuning. |             |             |                            |           |                   |        |
Intrinsic
|     | Qwen-2.5-14B |     | 0.44 | 1.85 | 1.34 | 0.94 |             |     |          |           |     |           |         |
| --- | ------------ | --- | ---- | ---- | ---- | ---- | ----------- | --- | -------- | --------- | --- | --------- | ------- |
|     | LLaMA-3.2-1B |     | 0.74 | 1.58 | 1.43 | 0.99 |             |     |          |           |     |           |         |
|     |              |     |      |      |      |      | Compression |     | laws for | intrinsic | and | extrinsic | perfor- |
|     | LLaMA-3.2-3B |     | 0.60 | 1.88 | 1.30 | 0.97 |             |     |          |           |     |           |         |
mance.
LLaMA-3-8B 0.48 2.36 1.31 0.97 Basedontheintrinsicandextrinsicperformance
Qwen-2.5-0.5B 1.11 -0.64 -0.05 0.87 obtainedwithdifferentLLMswithcalibration-freecompres-
|     | Qwen-2.5-1.5B |     | 1.01 | -1.00 | -0.08 | 0.95 |       |        |                 |      |         |     |             |
| --- | ------------- | --- | ---- | ----- | ----- | ---- | ----- | ------ | --------------- | ---- | ------- | --- | ----------- |
|     |               |     |      |       |       |      | sion, | we fit | the compression | laws | defined | in  | Equations 1 |
|     | Qwen-2.5-3B   |     | 0.91 | -1.19 | -0.11 | 0.96 |       |        |                 |      |         |     |             |
Qwen-2.5-7B 0.64 -1.34 -0.11 0.98 andtheablationsinTable1. Theintrinsiccompressionlaws
Extrinsic
Qwen-2.5-14B 0.55 -1.51 -0.10 0.87 exhibitanegativescalingfactor(β =1.72>0)forthecom-
LLaMA-3.2-1B 1.28 -0.60 -0.08 0.81 pressionratior,indicatingthathighercompressionratios
|     | LLaMA-3.2-3B |     | 1.23 | -0.80 | -0.24 | 0.90 |                                  |     |     |     |                         |     |     |
| --- | ------------ | --- | ---- | ----- | ----- | ---- | -------------------------------- | --- | --- | --- | ----------------------- | --- | --- |
|     |              |     |      |       |       |      | resultinagreaterperformanceloss. |     |     |     | TheRFTdatasizeD         |     |     |
|     | LLaMA-3-8B   |     | 0.98 | -1.18 | -0.14 | 0.92 |                                  |     |     |     |                         |     |     |
|     |              |     |      |       |       |      | hasapositivescalingfactor(γ      |     |     |     | =1.16>0),indicatingbet- |     |     |
Table2.Fittedcompressioncoefficientsforintrinsicandextrinsic terperformancewithmorefine-tuningsteps. However,the
performancefordifferentLLMswiththefunctionalformL = scalingfactorofDisoverminedbythescalingfactorofr,
(cid:16) (cid:17)γ
Lα(r+1)β 1 highlightingtheirreduciblelossduetomodelcompression,
| 0   | 1+  | .Lowerα,theinfluenceofL |     |     |     | 0 ,forboth |     |     |     |     |     |     |     |
| --- | --- | ----------------------- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
D+1
intrinsicandextrinsicscalinglaws,indicatehigherperformance evenafterRFT.HighadjustedR2 andF-statisticindicate
stabilitypost-compression. Similarly,lower(higher)β,scaling thegoodness-of-fitofthecompressionlaw,justifyingthe
factorofcompressionratior,forintrinsic(extrinsic)scalinglaws functionalformdefinedinEquation1. Theextrinsicscaling
indicatehigherrobustnessundercompression.Lower(higher)γ, factorsexhibitanoppositetrend,whereincreasingrreduces
scalingfactorofRFTdatasizeD,forintrinsic(extrinsic)scaling theextrinsicperformance(averagezero-shotaccuracy). In-
lawsindicatehighereffectivenessofRFT.
|     |     |     |     |     |     |     | creasing                            | the | RFT data | size has | a positive, | albeit          | minor, |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | -------- | -------- | ----------- | --------------- | ------ |
|     |     |     |     |     |     |     | influenceontheextrinsicperformance. |     |          |          |             | Ontheotherhand, |        |
thescalingfactoroftheuncompressedmodelperformance
ever,afterRFT,theperformancegapdecreasestoonly100%
L is0.98,indicatingastronginfluenceonthecompressed
0
(animprovementof80%thanthepre-RFTmodel). Figure7 model’sextrinsicperformance. Thefittedscalingfactorsas-
inAppendixD.1showsthatthecalibration-basedcompres-
sertthattheextrinsicperformanceofthecompressedLLMs
| sionismorerobustintermsofintrinsicperformance. |             |       |     |      |                   | The |             |            |             |                 |     |                  |          |
| ---------------------------------------------- | ----------- | ----- | --- | ---- | ----------------- | --- | ----------- | ---------- | ----------- | --------------- | --- | ---------------- | -------- |
|                                                |             |       |     |      |                   |     | is less     | influenced | by          | the compression |     | ratio and        | recovery |
| intrinsic                                      | performance | drops | by  | 300% | post-compression; |     |             |            |             |                 |     |                  |          |
|                                                |             |       |     |      |                   |     | fine-tuning |            | token size. | We exhibit      | the | fitted intrinsic | and      |
however,theperformancegainisonlymeager(25%)after
|     |     |     |     |     |     |     | extrinsiccompressionlawsinFigure4. |     |     |     |     | Weobservethatthe |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- | --- | --- | ---------------- | --- |
recovery. fittedintrinsiccompressionlawtendstooverestimatethe
Figure1inSection1highlightstheextrinsicperformance testloss. However,withrecovery,thefitismoreaccurate,
indicatingtheimportanceofbothcompressionratiorand
| (average | zero-shot | accuracy) |     | for different |     | compressed |     |     |     |     |     |     |     |
| -------- | --------- | --------- | --- | ------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
RFTdatasizeDinestimatingtestcross-entropyloss.
LLMs. Extrinsicperformanceremainslessinfluencedby
thecompressionratio,wheretheperformancepost-pruning
dropsbyamaximumof47%athighercompressionratios. Model-wisecompressionlaws. Wereportthemodel-wise
Atalowercompressionratio(< 50%),post-compression scalinglawsinTable2andFigure9(inAppendixD.2). We
extrinsic performance can be up to 67% of the original observe low intrinsic and extrinsic α for larger language
uncompressedmodel’sperformance. Afterrecoveryfine- models (> 7B), indicating higher performance recovery
tuning,theperformancecanbeimprovedby3%,onaverage post-compression. On the other hand, larger LLMs have
athighercompressionratios. However,atlowercompres- lowerextrinsicβ,demonstratingtheirlackofrobustnessat
sion(<50%),theextrinsicperformancecangetashighas highercompressionratios,particularlyonextrinsicdown-
94%oftheoriginaluncompressedmodel. Thecalibration- streamtasks. Figure5highlightsthecriticalcompression
6

CompressionLawsforLargeLanguageModels
| Calibration |     |     |     | Intrinsic |     |     |     | Extrinsic |     |     |
| ----------- | --- | --- | --- | --------- | --- | --- | --- | --------- | --- | --- |
FittedFunction Adj.R2 F-Statistics FittedFunction Adj.R2 F-Statistics
|     |     |     |     | (cid:16) (cid:17)0.24 |     |     |     | (cid:16) | (cid:17)−0.06 |     |
| --- | --- | --- | --- | --------------------- | --- | --- | --- | -------- | ------------- | --- |
L=L0.70(r+1)1.40 1+ 1 0.98 3378 L=L1.25(r+1)−0.91 1+ 1 0.98 3960
|     |     | 0   |     | D+1                   |     | 0   |     | D+1      |               |     |
| --- | --- | --- | --- | --------------------- | --- | --- | --- | -------- | ------------- | --- |
|     |     |     |     | (cid:16) (cid:17)1.38 |     |     |     | (cid:16) | (cid:17)−0.20 |     |
L=L0.60(r+1)1.93 1+ 1 0.98 3295 L=L1.17(r+1)−0.79 1+ 1 0.99 10940
|     |     | 0   |     | D+1 |     | 0   |     | D+1 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Table3.FittedcompressionlawsforLLaMAmodelswhencompressedwithcalibration-freeandcalibration-basedcompressionmethods.
|     |     |              |                    |     |     |     |     |     | FFiitttteedd | EEmmppiirriiccaall |
| --- | --- | ------------ | ------------------ | --- | --- | --- | --- | --- | ------------ | ------------------ |
|     |     | FFiitttteedd | EEmmppiirriiccaall |     |     | 70  |     |     |              |                    |
17.5
ycarucca tohs-orez egarevA
15.0
60
12.5
ssol tseT
50
10.0
7.5
40
5.0
|     | 2.5 |       |                   |       |     | 30  |       |                   |       |     |
| --- | --- | ----- | ----------------- | ----- | --- | --- | ----- | ----------------- | ----- | --- |
|     |     | 10 30 |                   | 50 70 | 90  |     | 10 30 |                   | 50 70 | 90  |
|     |     |       | Compression ratio |       |     |     |       | Compression ratio |       |     |
|     |     |       |                   |       | L = |     |       |                   |       | L = |
(a) Intrinsic performance follows (b) Extrinsic performance follows
|     | L0.74(r+1)2.02 |     |     |     |     | L1.01(r+1)−1.05 |     |     |     |     |
| --- | -------------- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- |
|     | 0              |     |     |     |     | 0               |     |     |     |     |
18
|     |     |     |     | FFiitttteedd | EEmmppiirriiccaall |     |     |     |              |                    |
| --- | --- | --- | --- | ------------ | ------------------ | --- | --- | --- | ------------ | ------------------ |
|     | 16  |     |     |              |                    | 80  |     |     | FFiitttteedd | EEmmppiirriiccaall |
ycarucca tohs-orez egarevA
|     | 14  |     |     |     |     | 70  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
12
|     | ssol tseT |     |     |     |     | 60  |     |     |     |     |
| --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
10
|     | 8   |     |     |     |     | 50  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 6   |     |     |     |     | 40  |     |     |     |     |
4
30
2
|     | 0                   | 1000 | 4000          |          | 25000        | 0                    | 1000    | 4000          |          | 25000         |
| --- | ------------------- | ---- | ------------- | -------- | ------------ | -------------------- | ------- | ------------- | -------- | ------------- |
|     |                     |      | RFT data size |          |              |                      |         | RFT data size |          |               |
|     | 10%                 | 30%  |               | 50% 70%  | 90%          |                      | 10% 30% |               | 50% 70%  | 90%           |
|     |                     |      |               | (cid:16) | (cid:17)1.16 |                      |         |               | (cid:16) | (cid:17)−0.14 |
|     | (c)L=L0.63(r+1)1.72 |      |               | 1+ 1     |              | (d)L=L0.98(r+1)−1.03 |         |               | 1+ 1     |               |
|     |                     | 0    |               | D+1      |              |                      | 0       |               | D+1      |               |
Figure4.Fitofintrinsic(a)andextrinsic(b)compressionlawsfordifferentLLMsatdifferentcompressionratiosusingthecalibration-free
method.DifferentlinesindicatedifferentL frontiers.Impactofrecoveryfine-tuningontheintrinsic(c)andextrinsic(d)performanceof
0
compressedLLMsusingthecalibration-freemethod.Figure11ofAppendixD.5highlightsthecompressionlawswithcalibration-based
compressionmethod.
ratios(definedinCorollary3.2)ofdifferentmodelsizeson Effect of calibration in compression. To understand
intrinsicandextrinsictasks. Weobservehigherandlower the influence of calibration on post-compression perfor-
criticalcompressionratioforlargerLLMs(>3B)onintrin-
mance’seffectiveness,wefitthecompressionlawforboth
sicandextrinsictasks,respectively. Theresultsindicatethat calibration-freeandcalibration-basedmethods,reportedin
whilelargerLLMsaremorerobustundercompression(they Table3. Calibration-basedmethodhashigherintrinsicand
canwithstandlargercompression)onintrinsictasks,their extrinsicα,indicatinglowerpost-compressionrobustness.
performancedropssignificantlybelowtherecoverylevelon Contrarily,calibration-basedmethodhaslowerintrinsicand
extrinsictasks,athighercompressionlevel. Theseresults extrinsic β. Therefore, this method is more effective at
indicatethatcompressinglargerLLMsatlargercompres- higher compression ratios on intrinsic task, but performs
sionratioshouldbeavoided, unlesssmallerLLMsatthe poorlyondownstreamextrinsictasks. Similarly,lowerin-
givenbudgetisnotavailable. trinsicγ andhigherextrinsicγ demonstratethatcalibration-
7

CompressionLawsforLargeLanguageModels
|     |     | )% ni( oitar noisserpmoc lacitirC |     |     |     |     | )% ni( oitar noisserpmoc lacitirC |     |     |     |     |     |     |
| --- | --- | --------------------------------- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- |
|     |     | 100                               |     |     |     |     | 100                               |     |     |     |     |     |     |
|     |     | 80                                |     |     |     |     | 80                                |     |     |     |     |     |     |
60
60
|     |     | 40  |     |     |     |     | 40  |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
20
20
0
|     |     | 1                                           | 3   | 5   | 7   | 9   | 10                                   | 30  | 50  | 70  | 90  |     |     |
| --- | --- | ------------------------------------------- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- | --- | --- |
|     |     | Ratio of compressed/uncompressed model loss |     |     |     |     | Expected performance recovery (in %) |     |     |     |     |     |     |
<<11BB 11BB--33BB 44BB--77BB 88BB--1144BB <<11BB 11BB--33BB 44BB--77BB 88BB--1144BB
|     |     | (a)Intrinsiccriticalcompressionratio |     |     |     |     | (b)Extrinsiccriticalcompressionratio |     |     |     |     |     |     |
| --- | --- | ------------------------------------ | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- | --- | --- |
Figure5.Criticalcompressionratiofordifferentmodelsizesforintrinsic(a)andextrinsic(b)performances.Highcriticalcompression
ratioindicatesthatanLLMcanretainperformanceevenwhencompressedextremely.
|     |     |     |     |     |     |     | Model |     | β Adj.R2 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | -------- | --- | --- | --- | --- |
basedmethodscaleseffectivelywithrecoveryfine-tuning
|                                   |     |     |     |                   |     |     | Qwen-2.5-0.5B |     | -0.21 | 0.69 | Table4.Fitted |              | com- |
| --------------------------------- | --- | --- | --- | ----------------- | --- | --- | ------------- | --- | ----- | ---- | ------------- | ------------ | ---- |
| onbothintrinsicandextrinsictasks. |     |     |     | Therefore,weargue |     |     |               |     |       |      |               |              |      |
|                                   |     |     |     |                   |     |     |               |     |       |      | pression      | coefficients |      |
thatcalibration-basedmethodshouldonlybeusedforlower Qwen-2.5-1.5B -1.12 0.94
|     |     |     |     |     |     |     |             |     |       |      | for inference |     | runtime |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ----- | ---- | ------------- | --- | ------- |
|     |     |     |     |     |     |     | Qwen-2.5-3B |     | -1.45 | 0.92 |               |     |         |
compressionratios,whenrecoveryfine-tuningdatasetsare
|            |                                             |     |     |     |     |     | Qwen-2.5-7B  |     | -1.93 | 0.95 | of compressed |     | LLMs       |
| ---------- | ------------------------------------------- | --- | --- | --- | --- | --- | ------------ | --- | ----- | ---- | ------------- | --- | ---------- |
| available. | Inanyothercases,calibration-freemethodguar- |     |     |     |     |     |              |     |       |      |               |     |            |
|            |                                             |     |     |     |     |     | Qwen-2.5-14B |     | -1.62 | 0.93 | with          | the | functional |
anteeshigherpost-compressionrobustness. LLaMA-3.2-1B -0.92 0.97 formS =C(r+1)β.
|     |     |     |     |     |     |     | LLaMA-3.2-3B |     | -1.67 | 0.82 | Lower | β   | indicates |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ----- | ---- | ----- | --- | --------- |
8000 FFiitttteedd EEmmppiirriiccaall LLaMA-3-8B -1.87 0.92 higher inference
)ceS ni( emitnuR ecnerefnI
|     |     |     |     |     |     |     |     |     |     |     | efficiency |     | at higher |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --------- |
7000
|     | 6000 |     |     |     |     |     |     |     |     |     | compressionratios. |     |     |
| --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- |
5000
4000
|     | 3000 |     |     |     |     |     | offeringnewinsightsintotherelationshipsbetweencom- |     |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | -------------------------------------------------- | --- | --- | --- | --- | --- | --- |
2000 pression ratios, performance metrics, and recovery fine-
|     | 1000 |      |     |       |     |     | tuning.                                      | We provided | practical | guidelines |     | for implement- |       |
| --- | ---- | ---- | --- | ----- | --- | --- | -------------------------------------------- | ----------- | --------- | ---------- | --- | -------------- | ----- |
|     |      | 0    |     |       |     |     | ingmodelcompressioninreal-worldapplications, |             |           |            |     |                | where |
|     |      | 0 10 | 30  | 50 70 | 90  |     |                                              |             |           |            |     |                |       |
Compression Ratio bothperformancestabilityandscalabilityarecrucial. Our
studyrevealedthatwhencompressingLLMslargerthan7B
|     |     | Qwen2.5-0.5B | Qwen2.5-3B |     | Llama-3.2-3B |     |     |     |     |     |     |     |     |
| --- | --- | ------------ | ---------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
parameters,compressionratiosexceeding70%shouldbe
|     |     | Qwen2.5-1.5B | Qwen2.5-7B   |     | Meta-Llama-3-8B |     |          |               |     |            |     |              |     |
| --- | --- | ------------ | ------------ | --- | --------------- | --- | -------- | ------------- | --- | ---------- | --- | ------------ | --- |
|     |     | Qwen2.5-14B  | Llama-3.2-1B |     |                 |     |          |               |     |            |     |              |     |
|     |     |              |              |     |                 |     | avoided. | We emphasized | the | importance |     | of selecting | ap- |
propriatecompressiontechniquesbasedonmodelsizeand
Figure6.InferenceruntimeofcompressedLLMsfollowsapower
lawL=L1.0(r+1)−0.67,withL resourceconstraints. Forscenarioswhereextrinsicperfor-
|     | 0   |     |     | 0 beingtheinferenceruntime |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
manceisprioritized,calibration-freecompressionmethods
oftheuncompressedLLM.Wecalculatethetotalinferencetime
|     |     |     |     |     |     |     | tend to | offer greater | robustness, |     | while calibration-based |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------- | ----------- | --- | ----------------------- | --- | --- |
insecondsontheextrinsicbenchmark.
techniquesprovidebetterstabilityintermsofintrinsicloss.
| Influenceofmodelcompressiononinferencespeed. |     |     |     |     |     | We  |     |     |     |     |     |     |     |
| -------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Moreover,westressedtheneedtobalanceefficiencywith
reportthescalingoftheinferenceruntimeofcompressed
downstreamtaskperformanceinproductionenvironments.
| LLMs | in Figure | 6. Negative |     | β indicates | that | inference |     |     |     |     |     |     |     |
| ---- | --------- | ----------- | --- | ----------- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
Largermodelsparticularlybenefitfromhighcompressionin
runtimereducesexponentiallyatlargercompressionratios termsofinferencespeedupbutshouldonlybecompressedif
| foralltheLLMs. |     | However,Table4highlightsthatlarger |     |     |     |     |     |     |     |     |     |     |     |
| -------------- | --- | ---------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
smallerpre-trainedvariantsofsimilarsizesareunavailable.
LLMs(>7B)tendtohavebettercomputescalingathigher
Thisworklaysthefoundationforfutureresearchintoadap-
compressionratios,assertingthecomputationalbenefitsof tive, task-aware compression methods, and the effects of
compressinglargermodelsthanthesmallerones.
compressiononlong-contextreasoningandgenerativecapa-
bilities. Wealsosuggestinvestigatinghybridcompression
5.Conclusion
|     |     |     |     |     |     |     | strategies | that combine | structured |     | and unstructured |     | prun- |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------------ | ---------- | --- | ---------------- | --- | ----- |
Inthispaper, weintroducedcompressionlawsforLLMs ingwithquantizationtoachieveamorebalancedtrade-off
that explore the impact of structured model compression, betweencomputationalsavingsandperformanceretention.
8

CompressionLawsforLargeLanguageModels
| References |               |                    |             | Y.,Gong,Y.,Zou,Y.,He,Y.,Zha,Y.,Xiong,Y.,Ma,Y., |               |                    |         |        |
| ---------- | ------------- | ------------------ | ----------- | ---------------------------------------------- | ------------- | ------------------ | ------- | ------ |
|            |               |                    |             | Yan, Y.,                                       | Luo, Y., You, | Y., Liu, Y., Zhou, | Y., Wu, | Z. F., |
| Ashkboos,  | S., Croci, M. | L., do Nascimento, | M. G., Hoe- |                                                |               |                    |         |        |
Ren,Z.Z.,Ren,Z.,Sha,Z.,Fu,Z.,Xu,Z.,Huang,Z.,
| fler,T.,andHensman,J. |     | Slicegpt: Compresslargelan- |     |     |     |     |     |     |
| --------------------- | --- | --------------------------- | --- | --- | --- | --- | --- | --- |
Zhang,Z.,Xie,Z.,Zhang,Z.,Hao,Z.,Gou,Z.,Ma,Z.,
| guagemodelsbydeletingrowsandcolumns,2024. |     |     | URL |     |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Yan,Z.,Shao,Z.,Xu,Z.,Wu,Z.,Zhang,Z.,Li,Z.,Gu,
https://arxiv.org/abs/2401.15024.
|     |     |     |     | Z., Zhu,  | Z., Liu, Z., Li,                 | Z., Xie, Z., | Song, Z., | Gao, Z., |
| --- | --- | --- | --- | --------- | -------------------------------- | ------------ | --------- | -------- |
|     |     |     |     | andPan,Z. | Deepseek-v3technicalreport,2024. |              |           | URL      |
Bisk,Y.,Zellers,R.,Gao,J.,Choi,Y.,etal.Piqa:Reasoning
https://arxiv.org/abs/2412.19437.
| aboutphysicalcommonsenseinnaturallanguage. |     |     | InPro- |     |     |     |     |     |
| ------------------------------------------ | --- | --- | ------ | --- | --- | --- | --- | --- |
ceedingsoftheAAAIconferenceonartificialintelligence,
|     |     |     |     | Diaz, F. | and Madaio, M. | Scaling laws | do not | scale, |
| --- | --- | --- | --- | -------- | -------------- | ------------ | ------ | ------ |
volume34,pp.7432–7439,2020.
http://arxiv.org/abs/2307.
|     |     |     |     | July 2024. | URL |     |     |     |
| --- | --- | --- | --- | ---------- | --- | --- | --- | --- |
Caballero,E.,Gupta,K.,Rish,I.,andKrueger,D. Broken 03201. arXiv:2307.03201.
| neuralscalinglaws,July2023. |     | URLhttp://arxiv.  |     |            |                     |             |               |     |
| --------------------------- | --- | ----------------- | --- | ---------- | ------------------- | ----------- | ------------- | --- |
| org/abs/2210.14891.         |     | arXiv:2210.14891. |     |            |                     |             |               |     |
|                             |     |                   |     | Dubey, A., | Jauhri, A., Pandey, | A., Kadian, | A., Al-Dahle, |     |
A.,Letman,A.,Mathur,A.,Schelten,A.,Yang,A.,Fan,
Chen,X.,Hu,Y.,Zhang,J.,Zhang,X.,Li,C.,andChen,H.
|                                              |     |     |       | A., et al. | The llama 3 | herd of models. | arXiv | preprint |
| -------------------------------------------- | --- | --- | ----- | ---------- | ----------- | --------------- | ----- | -------- |
| Scalinglawforpost-trainingaftermodelpruning. |     |     | arXiv |            |             |                 |       |          |
arXiv:2407.21783,2024.
preprintarXiv:2411.10272,2024.
|     |     |     |     | Faiz, A., | Kaneda, S., | Wang, R., Osi, | R., Sharma, | P., |
| --- | --- | --- | --- | --------- | ----------- | -------------- | ----------- | --- |
Clark,P.,Cowhey,I.,Etzioni,O.,Khot,T.,Sabharwal,A.,
Schoenick, C., andTafjord, O. Thinkyouhavesolved Chen, F., and Jiang, L. Llmcarbon: modeling the end-
|                    |                                  |     |     | to-end     | carbon footprint               | of large language | models, | Jan- |
| ------------------ | -------------------------------- | --- | --- | ---------- | ------------------------------ | ----------------- | ------- | ---- |
| questionanswering? | tryarc,theai2reasoningchallenge. |     |     |            |                                |                   |         |      |
|                    |                                  |     |     | uary 2024. | URL http://arxiv.org/abs/2309. |                   |         |      |
arXivpreprintarXiv:1803.05457,2018.
|     |     |     |     | 14393. | arXiv:2309.14393. |     |     |     |
| --- | --- | --- | --- | ------ | ----------------- | --- | --- | --- |
Cortes,C.,Jackel,L.D.,Solla,S.,Vapnik,V.,andDenker,
|                    |                               |     |     | Frantar,E.andAlistarh,D. |     | Sparsegpt: | Massivelanguage |     |
| ------------------ | ----------------------------- | --- | --- | ------------------------ | --- | ---------- | --------------- | --- |
| J. Learningcurves: | Asymptoticvaluesandrateofcon- |     |     |                          |     |            |                 |     |
vergence. Advances in neural information processing modelscanbeaccuratelyprunedinone-shot,2023. URL
| systems,6,1993. |     |     |     | https://arxiv.org/abs/2301.00774. |     |     |     |     |
| --------------- | --- | --- | --- | --------------------------------- | --- | --- | --- | --- |
DeepSeek-AI,Liu,A.,Feng,B.,Xue,B.,Wang,B.,Wu,B.,
Gao,L.,Tow,J.,Abbasi,B.,Biderman,S.,Black,S.,DiPofi,
Lu,C.,Zhao,C.,Deng,C.,Zhang,C.,Ruan,C.,Dai,D., A., Foster, C., Golding, L., Hsu, J., Le Noac’h, A., Li,
Guo,D.,Yang,D.,Chen,D.,Ji,D.,Li,E.,Lin,F.,Dai,
H.,McDonell,K.,Muennighoff,N.,Ociepa,C.,Phang,
| F., Luo, | F., Hao, G., Chen, | G., Li, G., | Zhang, H., Bao, |     |     |     |     |     |
| -------- | ------------------ | ----------- | --------------- | --- | --- | --- | --- | --- |
J.,Reynolds,L.,Schoelkopf,H.,Skowron,A.,Sutawika,
H.,Xu,H.,Wang,H.,Zhang,H.,Ding,H.,Xin,H.,Gao, L., Tang, E., Thite, A., Wang, B., Wang, K., and Zou,
H.,Li,H.,Qu,H.,Cai,J.L.,Liang,J.,Guo,J.,Ni,J.,Li,
A. Aframeworkforfew-shotlanguagemodelevaluation,
J.,Wang,J.,Chen,J.,Chen,J.,Yuan,J.,Qiu,J.,Li,J., 072024. URLhttps://zenodo.org/records/
| Song,J.,Dong,K.,Hu,K.,Gao,K.,Guan,K.,Huang, |     |     |     | 12608602. |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --------- | --- | --- | --- | --- |
K.,Yu,K.,Wang,L.,Zhang,L.,Xu,L.,Xia,L.,Zhao,
L.,Wang,L.,Zhang,L.,Li,M.,Wang,M.,Zhang,M., Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika,
Zhang,M.,Tang,M.,Li,M.,Tian,N.,Huang,P.,Wang,
|     |     |     |     | M., Song, | D., and Steinhardt, | J.  | Measuring | mas- |
| --- | --- | --- | --- | --------- | ------------------- | --- | --------- | ---- |
P.,Zhang,P.,Wang,Q.,Zhu,Q.,Chen,Q.,Du,Q.,Chen, sive multitask language understanding. arXiv preprint
R. J., Jin, R. L., Ge, R., Zhang, R., Pan, R., Wang, R., arXiv:2009.03300,2020.
Xu,R.,Zhang,R.,Chen,R.,Li,S.S.,Lu,S.,Zhou,S.,
Chen,S.,Wu,S.,Ye,S.,Ye,S.,Ma,S.,Wang,S.,Zhou, Hestness,J.,Narang,S.,Ardalani,N.,Diamos,G.,Jun,H.,
S.,Yu,S.,Zhou,S.,Pan,S.,Wang,T.,Yun,T.,Pei,T., Kianinejad,H.,Patwary,M.M.A.,Yang,Y.,andZhou,Y.
Sun,T.,Xiao,W.L.,Zeng,W.,Zhao,W.,An,W.,Liu, Deeplearningscalingispredictable,empirically. arXiv
W., Liang, W., Gao, W., Yu, W., Zhang, W., Li, X. Q., preprintarXiv:1712.00409,2017.
Jin,X.,Wang,X.,Bi,X.,Liu,X.,Wang,X.,Shen,X.,
Chen,X.,Zhang,X.,Chen,X.,Nie,X.,Sun,X.,Wang, Hoffmann,J.,Borgeaud,S.,Mensch,A.,Buchatskaya,E.,
X., Cheng, X., Liu, X., Xie, X., Liu, X., Yu, X., Song, Cai,T.,Rutherford,E.,Casas,D.d.L.,Hendricks,L.A.,
X.,Shan,X.,Zhou,X.,Yang,X.,Li,X.,Su,X.,Lin,X., Welbl,J.,Clark,A.,Hennigan,T.,Noland,E.,Millican,
Li, Y. K., Wang, Y. Q., Wei, Y. X., Zhu, Y. X., Zhang, K., Driessche, G.v.d., Damoc, B., Guy, A., Osindero,
Y.,Xu,Y.,Xu,Y.,Huang,Y.,Li,Y.,Zhao,Y.,Sun,Y., S.,Simonyan,K.,Elsen,E.,Rae,J.W.,Vinyals,O.,and
Li, Y., Wang, Y., Yu, Y., Zheng, Y., Zhang, Y., Shi, Y., Sifre,L. Trainingcompute-optimallargelanguagemod-
Xiong,Y.,He,Y.,Tang,Y.,Piao,Y.,Wang,Y.,Tan,Y., els, March 2022. URL http://arxiv.org/abs/
Ma,Y.,Liu,Y.,Guo,Y.,Wu,Y.,Ou,Y.,Zhu,Y.,Wang, 2203.15556. arXiv:2203.15556.
9

CompressionLawsforLargeLanguageModels
Hu, E. J., yelong shen, Wallis, P., Allen-Zhu, Z., Li, Y., Sakaguchi,K.,Bras,R.L.,Bhagavatula,C.,andChoi,Y.
Wang,S.,Wang,L.,andChen,W.LoRA:Low-rankadap- Winogrande: Anadversarialwinogradschemachallenge
tationoflargelanguagemodels. InInternationalConfer- at scale. Communications of the ACM, 64(9):99–106,
| enceonLearningRepresentations,2022. |     |     |     |     |     | URLhttps: |     | 2021. |     |     |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | --- | --------- | --- | ----- | --- | --- | --- | --- | --- | --- |
//openreview.net/forum?id=nZeVKeeFYf9.
|         |                 |     |     |           |     |        |        | Sengupta,      | A., | Chaudhary,                         | S., | and Chakraborty, |     | T. You |
| ------- | --------------- | --- | --- | --------- | --- | ------ | ------ | -------------- | --- | ---------------------------------- | --- | ---------------- | --- | ------ |
|         |                 |     |     |           |     |        |        | onlypruneonce: |     | Designingcalibration-freemodelcom- |     |                  |     |        |
| Kaplan, | J., McCandlish, |     | S., | Henighan, | T., | Brown, | T. B., |                |     |                                    |     |                  |     |        |
Chess,B.,Child,R.,Gray,S.,Radford,A.,Wu,J.,and pression with policy learning, 2025. URL https:
//arxiv.org/abs/2501.15296.
Amodei,D.Scalinglawsforneurallanguagemodels,Jan-
| uary 2020. |                   | URL http://arxiv.org/abs/2001. |     |     |     |     |     |                                      |         |          |     |           |            |         |
| ---------- | ----------------- | ------------------------------ | --- | --- | --- | --- | --- | ------------------------------------ | ------- | -------- | --- | --------- | ---------- | ------- |
|            |                   |                                |     |     |     |     |     | Sun,M.,Liu,Z.,Bair,A.,andKolter,J.Z. |         |          |     |           | Asimpleand |         |
| 08361.     | arXiv:2001.08361. |                                |     |     |     |     |     |                                      |         |          |     |           |            |         |
|            |                   |                                |     |     |     |     |     | effective                            | pruning | approach |     | for large | language   | models. |
arXivpreprintarXiv:2306.11695,2023.
| Kumar,       | T., Ankner,       |                            | Z., Spector, |           | B. F.,         | Bordelon, | B.,     |                                        |                                         |        |            |         |         |             |
| ------------ | ----------------- | -------------------------- | ------------ | --------- | -------------- | --------- | ------- | -------------------------------------- | --------------------------------------- | ------ | ---------- | ------- | ------- | ----------- |
| Muennighoff, |                   | N.,                        | Paul, M.,    | Pehlevan, | C.,            | Re´,      | C., and |                                        |                                         |        |            |         |         |             |
|              |                   |                            |              |           |                |           |         | Taori, R.,                             | Gulrajani,                              |        | I., Zhang, | T.,     | Dubois, | Y., Li, X., |
| Raghunathan, |                   | A.                         | Scaling      | laws      | for precision, |           | Novem-  |                                        |                                         |        |            |         |         |             |
|              |                   |                            |              |           |                |           |         | Guestrin,C.,Liang,P.,andHashimoto,T.B. |                                         |        |            |         |         | Stanford    |
| ber 2024.    | URL               | http://arxiv.org/abs/2411. |              |           |                |           |         |                                        |                                         |        |            |         |         |             |
|              |                   |                            |              |           |                |           |         | alpaca:                                | Aninstruction-followingllamamodel,2023. |        |            |         |         |             |
| 04330.       | arXiv:2411.04330. |                            |              |           |                |           |         |                                        |                                         |        |            |         |         |             |
|              |                   |                            |              |           |                |           |         | van der                                | Ouderaa,                                | T. F., | Nagel,     | M., Van | Baalen, | M., and     |
Levesque,H.J.,Davis,E.,andMorgenstern,L. Thewino- Blankevoort,T. Thellmsurgeon. InTheTwelfthInterna-
gradschemachallenge. InProceedingsoftheThirteenth tionalConferenceonLearningRepresentations.
| International  |     | Conference |            | on Principles |        | of Knowledge |     |            |                        |     |     |     |                  |     |
| -------------- | --- | ---------- | ---------- | ------------- | ------ | ------------ | --- | ---------- | ---------------------- | --- | --- | --- | ---------------- | --- |
|                |     |            |            |               |        |              |     | Vaswani,A. | Attentionisallyouneed. |     |     |     | AdvancesinNeural |     |
| Representation |     | and        | Reasoning, |               | KR’12, | pp. 552–561. |     |            |                        |     |     |     |                  |     |
AAAIPress,2012. ISBN9781577355601. InformationProcessingSystems,2017.
Ma,X.,Fang,G.,andWang,X. Onthestructuralpruning Villalobos,P.,Ho,A.,Sevilla,J.,Besiroglu,T.,Heim,L.,
|                        |     |     |     |                          |     |     |     | and Hobbhahn, |     | M.      | Will  | we run             | out of | data? Lim- |
| ---------------------- | --- | --- | --- | ------------------------ | --- | --- | --- | ------------- | --- | ------- | ----- | ------------------ | ------ | ---------- |
| oflargelanguagemodels. |     |     |     | NeurIPS,Llm-pruner,2023. |     |     |     |               |     |         |       |                    |        |            |
|                        |     |     |     |                          |     |     |     | its of        | LLM | scaling | based | on human-generated |        | data,      |
Marcus, M. P., Santorini, B., and Marcinkiewicz, M. A. June2024. URLhttp://arxiv.org/abs/2211.
|               |     |                                     |                           |        |     |          |     | 04325.    | arXiv:2211.04325. |     |          |         |               |         |
| ------------- | --- | ----------------------------------- | ------------------------- | ------ | --- | -------- | --- | --------- | ----------------- | --- | -------- | ------- | ------------- | ------- |
| Building      | a   | large                               | annotated                 | corpus | of  | English: | The |           |                   |     |          |         |               |         |
| PennTreebank. |     | ComputationalLinguistics,19(2):313– |                           |        |     |          |     |           |                   |     |          |         |               |         |
|               |     |                                     |                           |        |     |          |     | Wang, X., | Zheng,            | Y., | Wan,     | Z., and | Zhang,        | M. Svd- |
| 330, 1993.    |     | URL                                 | https://aclanthology.org/ |        |     |          |     |           |                   |     |          |         |               |         |
|               |     |                                     |                           |        |     |          |     | llm:      | Truncation-aware  |     | singular | value   | decomposition |         |
J93-2004.
|     |     |     |     |     |     |     |     | for large | language | model | compression. |     | arXiv | preprint |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | -------- | ----- | ------------ | --- | ----- | -------- |
Merity, S., Xiong, C., Bradbury, J., and Socher, R. arXiv:2403.07378,2024.
arXiv preprint
| Pointer | sentinel |     | mixture | models. |     |     |     |           |      |         |       |          |       |          |
| ------- | -------- | --- | ------- | ------- | --- | --- | --- | --------- | ---- | ------- | ----- | -------- | ----- | -------- |
|         |          |     |         |         |     |     |     | Yang, Y., | Cao, | Z., and | Zhao, | H. Laco: | Large | language |
arXiv:1609.07843,2016.
|     |     |     |     |     |     |     |     | modelpruningvialayercollapse,2024. |     |     |     |     | URLhttps: |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- | --- | --- | --------- | --- |
//arxiv.org/abs/2402.11187.
| Muennighoff, |     | N., Rush, | A.  | M., Barak, | B., | Scao, | T. L., |     |     |     |     |     |     |     |
| ------------ | --- | --------- | --- | ---------- | --- | ----- | ------ | --- | --- | --- | --- | --- | --- | --- |
Piktus, A., Tazi, N., Pyysalo, S., Wolf, T., and Raf- Zdaniuk, B. Ordinary Least-Squares (OLS) Model,
| fel, C.    | Scaling | data-constrained              |     |     | language | models, | Oc- |                |      |                    |          |              |      |            |
| ---------- | ------- | ----------------------------- | --- | --- | -------- | ------- | --- | -------------- | ---- | ------------------ | -------- | ------------ | ---- | ---------- |
|            |         |                               |     |     |          |         |     | pp. 4515–4517. |      |                    | Springer | Netherlands, |      | Dordrecht, |
| tober2023. |         | URLhttp://arxiv.org/abs/2305. |     |     |          |         |     |                |      |                    |          |              |      |            |
|            |         |                               |     |     |          |         |     | 2014.          | ISBN | 978-94-007-0753-5. |          |              | doi: | 10.1007/   |
16264. arXiv:2305.16264. 978-94-007-0753-5 2008. URLhttps://doi.org/
10.1007/978-94-007-0753-5_2008.
Qwen,Yang,A.,Yang,B.,Zhang,B.,Hui,B.,Zheng,B.,
Yu,B.,Li,C.,Liu,D.,Huang,F.,Wei,H.,Lin,H.,Yang, Zellers,R.,Holtzman,A.,Bisk,Y.,Farhadi,A.,andChoi,
J.,Tu,J.,Zhang,J.,Yang,J.,Yang,J.,Zhou,J.,Lin,J., Y. Hellaswag:Canamachinereallyfinishyoursentence?
Dang,K.,Lu,K.,Bao,K.,Yang,K.,Yu,L.,Li,M.,Xue,
arXivpreprintarXiv:1905.07830,2019.
M.,Zhang,P.,Zhu,Q.,Men,R.,Lin,R.,Li,T.,Tang,T.,
Xia,T.,Ren,X.,Ren,X.,Fan,Y.,Su,Y.,Zhang,Y.,Wan,
| Y., Liu,                     | Y., Cui, | Z.,        | Zhang, | Z., and           | Qiu, | Z. Qwen2. | 5       |     |     |     |     |     |     |     |
| ---------------------------- | -------- | ---------- | ------ | ----------------- | ---- | --------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| technicalreport,January2025. |          |            |        | URLhttp://arxiv.  |      |           |         |     |     |     |     |     |     |     |
| org/abs/2412.15115.          |          |            |        | arXiv:2412.15115. |      |           |         |     |     |     |     |     |     |     |
| Rosenfeld,                   | J. S.,   | Rosenfeld, |        | A., Belinkov,     |      | Y., and   | Shavit, |     |     |     |     |     |     |     |
N. Aconstructivepredictionofthegeneralizationerror
| acrossscales. |     | arXivpreprintarXiv:1909.12673,2019. |     |     |     |     |     |     |     |     |     |     |     |     |
| ------------- | --- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
10

CompressionLawsforLargeLanguageModels
A.TheoreticalResults
A.1.ProofofTheorem3.1
Proof. Theproofisstraightforward. Wewant L ≥σ,whichisequivalenttothecondition
Lα
0
|     |     | (cid:18) | (cid:19)γ |     |     |
| --- | --- | -------- | --------- | --- | --- |
1
|     | (1+r)β | 1+  | ≥σ  |     | (7) |
| --- | ------ | --- | --- | --- | --- |
D+1
This inequality gives us a constrained region in [0,1]×[0,∞] from which we can pick the optimal values of (r,D).
Particularly,theaboveconditionisequivalentto
(cid:18) 1 (cid:19)γ
≥σ(1+r)−β
1+ (8)
D+1
Byourassumption,γ <0,implyingthat 1 <0. Clearly,thismeansthatthemapx(cid:55)→xγ 1
isdecreasing. So,applyingthis
γ
maptobothsidesoftheaboveinequality,weget
1
|     |     | ≤[σ(1+r)−β]γ | 1   |     |     |
| --- | --- | ------------ | --- | --- | --- |
1+ (9)
D+1
whichgivesusthedesiredboundonD. Notethattheaboveargumentalsogivesusthebackwardimplicationsinceallthe
| aboveinequalitiesareequivalent. | Thiscompletestheproof. |     |     |     |     |
| ------------------------------- | ---------------------- | --- | --- | --- | --- |
A.2.ProofofCorollary3.2
Proof. NotethatbyTheorem3.1,foragivenrandD,theinequality L ≥σholdsifandonlyifrandDsatisfy
Lα
0
1
|     |     | ≤[σ(1+r)−β]γ | 1   |     |      |
| --- | --- | ------------ | --- | --- | ---- |
|     |     |              | −1  |     | (10) |
D+1
For the rest of the proof, we interpret the RHS above as a function of r ∈ [0,1] and denote the RHS by ϕ(r), i.e.,
| ϕ(r):=[σ(1+r)−β]γ 1 −1. |     |     |     |     |     |
| ----------------------- | --- | --- | --- | --- | --- |
−β
Now,considerthefunctionϕ(r). Byourassumptions,weknowthatβ,γ <0;inparticular,thisimpliesthat <0. So,
γ
thismeansthatthefunctionϕ(r)isadecreasingfunctionw.r.tr. So,themaximumandminimumvaluesofthisfunction
overr ∈[0,1]areobtainedbyputtingr =0andr =1,respectively;particularly,themaximumandminimumvaluesare
|     | σγ 1 −1 | and [σ2−β]γ | 1 −1 |     | (11) |
| --- | ------- | ----------- | ---- | --- | ---- |
Wenowclaimthatthemaximumvalueispositive. Toseethis,wejustneedtoshowthat
|     |     | σγ 1 >1 |     |     | (12) |
| --- | --- | ------- | --- | --- | ---- |
Sinceγ <0(byassumption),theaboveinequalityisequivalenttoσ <1,whichistriviallytrue. Next,weconsidertwo
1
cases,namelywhentheminimumvalue[σ2−β]γ −1is>0andwhenthisminimumvalueis≤0.
1
• Case1: [σ2−β]γ −1>0. Notethatthiscaseoccurspreciselywhenσ ∈(0,2β). Inotherwords,foranyr ∈[0,1],
| wehavethatϕ(r)≥[σ2−β]γ | 1              | 1     |                                     |     |     |
| ---------------------- | -------------- | ----- | ----------------------------------- | --- | --- |
|                        | −1>0. So,since | →0asD | →∞,wecanchoosealargeenoughDsuchthat |     |     |
D+1
1 ≤ϕ(r),satisfyingtheconditionsofTheorem3.1. Inparticular,RFTwithadatasetsizeofD,whereDislarge
D+1
| enough,ensuresthat L | ≥σ. |     |     |     |     |
| -------------------- | --- | --- | --- | --- | --- |
Lα
0
| [σ2−β]γ 1 |     |     | ∈[2β,1). |     |     |
| --------- | --- | --- | -------- | --- | --- |
• Case2: −1≤0. Notethatthisoccurspreciselywhenσ Inthiscase,theminimumvalueofthe
functionϕ(r)is≤0,andthemaximumvalueis>0. So,wedefinetheuniquepointr tobethepointsuchthat
critical
1
ϕ(r )=0. Itiseasytoseethatr =σβ −1. Now,observethatifr ≥r ,thenϕ(r)≤0. Inparticular,
| critical | critical |     |     | critical |     |
| -------- | -------- | --- | --- | -------- | --- |
forsuchr,thereisnoD ∈[0,∞]whichsatisfies 1 ≤ϕ(r),andhence L ≥σisnotpossibleforsuchr(forany
|     |     | D+1 | Lα  |     |     |
| --- | --- | --- | --- | --- | --- |
0
choiceofD). Ontheotherhand,ifr <r ,thenϕ(r)>0;inparticular,wecanfindalargeenoughDsuchthat
critical
| 1 ≤ϕ(r),andhenceforthispairof(r,D)we’llhave |     | L ≥σ. |     |     |     |
| ------------------------------------------- | --- | ----- | --- | --- | --- |
Lα
| D+1 |     | 0   |     |     |     |
| --- | --- | --- | --- | --- | --- |
11

CompressionLawsforLargeLanguageModels
B.DatasetDescriptions
Intrinsic evaluation and RFT datasets. The WikiText dataset (Merity et al., 2016) is a widely used benchmark for
languagemodeling. Thesearticlesarehuman-reviewedandareconsideredwell-written,factuallyaccurate,andneutralin
perspective. ThedatasetisavailableinWikiText-2andWikiText-103,withourexperimentsutilizingWikiText-2. ThePenn
Treebank(PTB)(Marcusetal.,1993)isalargeannotatedcorpusfeaturingover4.5millionwordsofAmericanEnglish. A
notableportionofthiscorpus,comprisingarticlesfromtheWallStreetJournal,isprimarilyusedtoevaluatemodelson
sequencelabelingtasks. Additionally,theAlpacadataset(Taorietal.,2023)includes52,000instructionsanddemonstrations
generatedbyOpenAI’stext-davinci-003model,commonlyemployedforinstructiontuninginlanguagemodels.
Extrinsic (zero-shot) evaluation datasets. The PIQA dataset (Bisk et al., 2020) focuses on physical common-sense
reasoningineverydaysituations,emphasizingunconventionalsolutions. Eachexampleprovidesinstructionsforbuilding,
crafting,baking,ormanipulatingobjectsusingeverydaymaterials. Thereasoningtaskisstructuredasamultiple-choice
question(MCQ)format,where,givenaquestionandtwopossiblesolutions,amodelmustselectthecorrectsolution,with
preciselyonebeingcorrect. TheWinoGrandedataset(Sakaguchietal.,2021)expandsontheWinogradSchemaChallenge
(Levesqueetal.,2012),offeringalarge-scalecollectionofpronounresolutionproblemsthatarestraightforwardforhumans
butchallengingforAIsystems. TheHellaSwagdataset(Zellersetal.,2019)addressescommon-sensenaturallanguage
inference(NLI),wherethetaskistopredictthemostplausiblefollow-uptoagivensentence. TheAI2ReasoningChallenge
dataset(Clarketal.,2018)consistsofnaturalsciencequestion-answeringproblemsatagrade-schoollevel,createdfor
humanassessments,andrequiresrobustreasoningandknowledgetosolve. Lastly,theMMLUbenchmark(Hendrycksetal.,
2020)evaluatesmodelsacross57subjects,includingSTEM,humanities,andsocialsciences. Itteststheknowledgemodels
acquiredduringpre-trainingbyassessingtheirperformanceinzero-shotandfew-shotsettings.
C.Experiments
ModelClass #Models #Calibration #Compression #RFTDataset #RFTDatasize #Experiments
Qwen 5 1 5 3+1(noRFT) 3 2×5×1×5×(3×3+1)=500
LLaMA 3 2 5 3+1(noRFT) 3 2×3×2×5×(3×3+1)=600
Table5.Numberofexperimentsperformedinthestudy. ForeachQwenmodel,weuseonlycalibration-freemethodfor5different
compressionratios,3differentRFTdatasetwith3differentRFTdatasizeforbothintrinsicandextrinsicevaluations.ForLLaMAmodels
weusebothcalibration-freeandcalibration-basedcompressionmethods.
Wehighlighttheexperiments’detailsinTable5. ForeachQwenmodel,werunthecalibration-freemethodandevaluate
2 experiments (intrinsic and extrinsic) for each of the 5 compression ratios with no RFT and RFT on three datasets
(Alpaca,WikiText2,andPTB)with3differentdatasizes. ForLLaMAseriesmodels,weusebothcalibration-freeand
calibration-basedcompressionmethods.
D.Results
D.1.IntrinsicandextrinsicevaluationsofLLMswithcalibration-basedcompression
InFigure7,wevisualizethetestloss(intrinsicevaluation)ofcompressedmodelswithandwithoutrecoveryfine-tuning,
where the models are compressed using a calibration-based method. We perform recovery fine-tuning on the Alpaca,
PTB,andWikiText2datasets. AcomparisonbetweenFigure7andFigure3highlightsthestarkdifferencebetweenthe
effectofrecoveryfine-tuningforcalibration-basedandcalibration-freecompressionmethodsonacompressedmodel’s
performance. WhileFigure3suggeststhatLLMscompressedwithanon-calibration-basedmethodexperiencesignificant
improvementsinperformancepost-recoveryfine-tuning,weobservefromFigure7that,infact,there’sonlyamarginal
increaseintheperformanceofLLMscompressedwithourchosencalibration-basedmethod. Thishighlightsthefactthat
thecalibration-basedmethodismorestablewithrespecttorecoveryfine-tuning. Anotherpointtobenotedisthatthechoice
ofthecalibrationdatasetalsoinfluencesthisbehavior. Particularly,notethatforbothcalibration-freeandcalibration-based
methods,theperformanceimprovementpostRFTisthelargestfortheAlpacadataset. Atthesametime,itisonlymarginal
forthePTBandWikiText2datasets. ThiscouldbebecausealltheLLMsusedinthestudyarepre-trainedonautoregressive
languagemodelingtasks,enablingthemtoperformwellonlanguagemodelingdatasetslikeWikiTextandPTBinherently.
Ontheotherhand,theseLLMsarenotpredominantlypre-trainedoninstructionfine-tuningtaskslikeAlpaca. Therefore,
calibratingthesemodelsoninstructionfine-tuningismoreeffective.
12

CompressionLawsforLargeLanguageModels
WevisualizetheextrinsicperformanceofLLaMAmodelscompressedwiththecalibration-basedmethodpost-recovery
fine-tuninginFigure8. Thecalibration-freemethodismuchmoreeffectivepost-recoveryfind-tuning,asitperformsbetter
thanthecalibration-basedcounterpart(Figure1)onmostzero-shotgenerativetasks.Thisobservationhighlightsthepractical
importanceofusingsimplercalibration-freecompressionmethodsforrobustdownstreamperformanceofLLMs.
Llama-3.2-1B Llama-3.2-3B Meta-Llama-3-8B
Alpaca Alpaca Alpaca
4
4 4
1 1
PTB WikiText2 PTB WikiText2 PTB WikiText2
Compression 0% Compression 30% Compression 70%
Compression 10% Compression 50% Compression 90%
(a)Withoutrecoveryperformance
Llama-3.2-1B Llama-3.2-3B Meta-Llama-3-8B
Alpaca Alpaca Alpaca
4 4 4
1 1
PTB WikiText2 PTB WikiText2 PTB WikiText2
Compression 0% Compression 30% Compression 70%
Compression 10% Compression 50% Compression 90%
(b)Withrecoveryperformance
Figure7.Testloss(intrinsic)withcompressedLLMswithout(a)andwith(b)recoveryfine-tuningusingthecalibration-basedcompression
method.
Llama-3.2-1B Llama-3.2-3B Meta-Llama-3-8B
ARC-c ARC-c ARC-c
80
60 60 60
ARC-e MMLU ARC-e MMLU ARC-e MMLU
40 40 40
20 20 20
Hellaswag Winogrande Hellaswag Winogrande Hellaswag Winogrande
PiQA PiQA PiQA
Compression 0% Compression 30% Compression 70%
Compression 10% Compression 50% Compression 90%
Figure8. ExtrinsicperformanceofcompressedLLaMAmodelsaftercompressingwithcalibratedmethod(post-RFT).
D.2.Compressionlawsfordifferentmodelsizes
In Figures 9, we visualize the relationship between compressed LLMs’ intrinsic and extrinsic performance and the
compressionratioformodelsofvaryingsizeswithoutrecoveryfine-tuning. Weobservethatevenpost-compression,model
performance is still monotonic with respect to the model size. Notably, larger models perform better intrinsically and
extrinsicallythansmallermodelswithoutrecoveryfine-tuning. Fromthetwofigures,wealsoseethattheslopesoftheloss
13

CompressionLawsforLargeLanguageModels
ycarucca tohs-orez egarevA
7 FFiitttteedd EEmmppiirriiccaall 0.7 FFiitttteedd EEmmppiirriiccaall
6
0.6
ssol tseT
5
0.5
4
| 3   |     |     |     |     |     | 0.4 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2
0.3
1
|     | 10 30             | 50  | 70    | 90  |        | 10  | 30                | 50  | 70    | 90     |
| --- | ----------------- | --- | ----- | --- | ------ | --- | ----------------- | --- | ----- | ------ |
|     | Compression ratio |     |       |     |        |     | Compression ratio |     |       |        |
| <1B | 1B-3B             |     | 4B-7B |     | 8B-14B | <1B | 1B-3B             |     | 4B-7B | 8B-14B |
(a)Intrinsicperformanceatdifferentcompressionratios (b)Extrinsicperformanceatdifferentcompressionratios
Figure9. Compressionlawsfordifferentmodelsizesonintrinsic(a)andextrinsic(b)performance.
Models Calibration Dataset FittedFunction Adj.R2 F-Statistics
|     |              |     |         | Alpaca                                           | L=L−0.27(r+1)1.96(1+  |     | 1 )1.44   | 0.90 | 534.1 |     |
| --- | ------------ | --- | ------- | ------------------------------------------------ | --------------------- | --- | --------- | ---- | ----- | --- |
|     |              |     |         |                                                  | 0                     |     | D+1       |      |       |     |
|     | QwenandLLaMA |     |         |                                                  | L=L0.64(r+1)1.74(1+   |     | 1 )1.0    |      |       |     |
|     |              |     |         | PTB                                              | 0                     |     |           | 0.98 | 3740  |     |
|     |              |     |         |                                                  |                       |     | D+1 )1.04 |      |       |     |
|     |              |     |         | WikiText2                                        | L=L0.58(r+1)2.01(1+   |     | 1         | 0.98 | 2386  |     |
|     |              |     |         |                                                  | 0                     |     | D+1       |      |       |     |
|     |              |     |         | Alpaca                                           | L=L−0.63(r+1)2.30(1+  |     | 1 )1.75   | 0.96 | 593.7 |     |
|     |              |     |         |                                                  | 0                     |     | D+1       |      |       |     |
|     | LLaMA        |     |         |                                                  |                       |     | 1 )1.19   |      |       |     |
|     |              |     |         | PTB                                              | L=L0.71(r+1)1.70(1+ 0 |     |           | 0.99 | 4252  |     |
|     |              |     |         |                                                  |                       |     | D+1 )1.20 |      |       |     |
|     |              |     |         | WikiText2                                        | L=L0.64(r+1)2.10(1+   |     | 1         | 0.99 | 2113  |     |
|     |              |     |         |                                                  | 0                     |     | D+1       |      |       |     |
|     |              |     |         | Alpaca                                           | L=L−0.17(r+1)1.24(1+  |     | 1 )0.39   | 0.97 | 535.2 |     |
|     |              |     |         |                                                  | 0                     |     | D+1       |      |       |     |
|     | LLaMA        |     |         |                                                  |                       |     | )0.19     |      |       |     |
|     |              |     |         | PTB                                              | L=L0.76(r+1)0.88(1+   |     | 1         | 0.99 | 5961  |     |
|     |              |     |         |                                                  | 0                     |     | D+1       |      |       |     |
|     |              |     |         | WikiText2                                        | L=L0.79(r+1)1.19(1+   |     | 1 )0.22   | 0.99 | 9231  |     |
|     |              |     |         |                                                  | 0                     |     | D+1       |      |       |     |
|     |              |     | Table6. | Intrinsiccompressionlawfordifferenttestdatasets. |                       |     |           |      |       |     |
(oraccuracy)curvesarenearlyidenticalacrossallmodelsizeswithslightvariation;particularly,forintrinsicevaluation,the
curveformodelswithsize<1Bhasalargerslopeasthecompressionratioincreases,implyingthatmodelswithsize<1B
degradefasterwithmorecompressioncomparedtomodelswithsize>1B. Fortheextrinsicevaluationsetting,models
withsize> 1B degradefasterthanthosewithsize< 1B,buttherateofdegradationbecomessomewhatsimilarasthe
compressionratioincreasesto1.
D.3.Compressionlawsfordifferentdatasets
We report the fitted intrinsic compression laws for different test datasets in Table 6 and Figure 10. On the instruction
tuningdatasetAlpaca,weobservenegativeα,indicatingbetterperformancethanthelargeruncompressedmodel. Wealso
observeahigherγ fortheAlpacadatasetforallmodels,indicatingbetterrecoverypost-fine-tuning. However,thescaling
factorofthecompressionratio(β)isalsohigherforAlpaca,indicatinghigherperformancelosswhensubjectedtohigher
compression. Ontheotherhand, alltheLLMstendtostrugglewithlanguagemodelingdatasets–WikiTextandPTB,
irrespectiveofRFT.Finally,theβ andγ valuesforthecalibration-basedmethodaremuchsmallerthanthecalibration-free
method,whichagainshowcasesthehigherperformancestabilitywiththecalibration-basedmethod,withrespecttoRFT
andthecompressionratio.
D.4.CriticalcompressionratiofordifferentLLMs
Inthissection,westudythevariationofthecriticalcompressionratior (σ)formodelsofdifferentsizeswithrespectto
critical
Wedothisbothintheintrinsic(i.e.,modelloss)andextrinsic(i.e.,modelevaluation)settings.
therecoverythresholdσ. It
shouldbenotedthat,incontrasttotheextrinsicevaluationsetting,fortheintrinsicevaluationsetting,weconsiderσ-recovery
oftheform L ≤σ,whereσ ∈(1,∞). Notethatforthissetting,wehaveβ,γ >0. Moreover,wecanprovethefollowing
Lα
0
14

CompressionLawsforLargeLanguageModels
7
6
5
4
3
2
1
10 30 50 70 90
Compression ratio
ssol
tseT
FFiitttteedd EEmmppiirriiccaall
Alpaca Ptb Wikitext2
Figure10. Intrinsicscalingfordifferenttestdatasets.
variantofCorollary3.2forthecaseofmodelloss(intrinsicevaluation):
1. Ifσ >2β,thenforanycompressionratior ∈(0,1),thereexistsDsuchthatRFTonthecompressedmodelwitha
datasetofsizeDwillresultin L ≤σ.
Lα
0
2. Ifσ ∈(1,2β),wedefinethecriticalcompressionratior
critical
(σ):=σβ 1 −1. Then,foranyr ≥r
critical
(σ),noamount
ofRFTcanrecoverthecompressedmodellosstosatisfy L ≤σ. Ontheotherhand,foranyr <r ,thereisa
Lα critical
0
largeenoughDsuchthatRFTwithadatasetofsizeDwillresultin L ≤σ.
Lα
0
InFigure5,weplotthecriticalcompressionratioformodelsofvaryingsizes. Figure5(a)plotsthecriticalratioforthe
intrinsicevaluationsetting(i.e.,formodelloss). Inthissetting,weobservethatthecriticalcompressionratioreducesto0as
theratioofthelossesofthecompressedanduncompressedmodelsreducesto1;inotherwords,astherecoverythreshold
σ ∈(1,∞)reducesto1. Thisalsoexplainsthatmodelrecoverybecomesharderforbetterrecoverythresholds. Analogously,
theplotinFigure5(b)showsasimilartrend,whereinthecriticalcompressionratioreducesto0astherecoverythresholdσ
increasesto1intheextrinsicevaluationsetting(i.e.,formodelaccuracy). Moreover,smallermodelstendtohaveahigher
criticalcompressionratio(withafewexceptions)fortheintrinsicevaluationsetting,makingthemmoresuitableforrecovery
post-compression. Forthecaseofextrinsicevaluation,modelswithsizesupto3Bhaveahighercriticalcompressionratio
comparedtomodelswithsizes>4B;however,modelsofsimilarsize-typesdon’tnecessarilyfollowamonotonictrendin
theircompressionratios.
D.5.Impactofcalibrationonmodelcompression
Figures4and11representablationsthatweperformedtostudytheeffectofcalibrationdataonthemodelaccuracy/loss
curveswithrespecttothecompressionratioandthesizeoftherecoveryfine-tuningdataset. FromFigures4(a),(b)and
11(a),(b),weobservethatforboththecalibration-freeandcalibration-basedcompressionmethods,theintrinsicandextrinsic
compressionlawsbehavesimilarlyintermsoftheexponentsαandβ ofthebasemodelperformanceandthecompression
ratiorespectively. However,forbothsettings,theslopesofthecurvesforthecalibration-freemethodarelargerinmagnitude
thanthoseofthecalibration-basedmethod. Yetagain,thisshedslightonthefactthattheperformanceofcalibration-based
methods is more stable with respect to the compression ratio compared to the calibration-free counterpart. A similar
trendinbehaviourisobservedinplots4(c),(d)and11(c),(d). Observethattherecoveryinintrinsicperformanceforthe
calibration-freemethod(4(c))ismuchhigherthanthecalibration-basedmethod(11(c))asthesizeoftherecoveryfine-tuning
dataset increases from 0 to approximately 1000. However, the intrinsic performance in both cases stabilizes beyond a
thresholddatasetsize. Thishappensinthecaseofextrinsicperformanceaswell(4(d)and11(d)),thoughinthiscase,the
15

CompressionLawsforLargeLanguageModels
| 7   | FFiitttteedd | EEmmppiirriiccaall |     |     |     |     |     |     |              |                    |
| --- | ------------ | ------------------ | --- | --- | --- | --- | --- | --- | ------------ | ------------------ |
|     |              |                    |     |     |     |     |     |     | FFiitttteedd | EEmmppiirriiccaall |
ycarucca tohs-orez egarevA
| 6   |     |     |     |     | 60  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ssol tseT 5
50
4
| 3   |     |     |     |     | 40  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2
30
1
| 10  | 30  |                   | 50  | 70 90 |     | 10  |     | 30                | 50  | 70 90 |
| --- | --- | ----------------- | --- | ----- | --- | --- | --- | ----------------- | --- | ----- |
|     |     | Compression ratio |     |       |     |     |     | Compression ratio |     |       |
(a)IntrinsicperformancefollowsL=L0.73(r+1)2.13 (b)ExtrinsicperformancefollowsL=L1.0(r+1)−1.08
|     |     |              |                    | 0   |     |     |     |     |     | 0   |
| --- | --- | ------------ | ------------------ | --- | --- | --- | --- | --- | --- | --- |
| 6   |     | FFiitttteedd | EEmmppiirriiccaall |     | 80  |     |     |     |     |     |
ycaruccA tohs-orez egarevA
|           |     |     |     |     |     |     |     | FFiitttteedd | EEmmppiirriiccaall |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | ------------ | ------------------ | --- |
| 5         |     |     |     |     | 70  |     |     |              |                    |     |
| ssol tseT |     |     |     |     | 60  |     |     |              |                    |     |
4
50
3
40
2
30
| 1                   |     |               |          |              | 20  |                      |     |               |          |               |
| ------------------- | --- | ------------- | -------- | ------------ | --- | -------------------- | --- | ------------- | -------- | ------------- |
| 0 1000              |     | 4000          |          | 25000        |     | 0 1000               |     | 4000          |          | 25000         |
|                     |     | RFT data size |          |              |     |                      |     | RFT data size |          |               |
| 10%                 | 30% | 50%           |          | 70% 90%      |     | 10%                  | 30% | 50%           |          | 70% 90%       |
|                     |     |               | (cid:16) | (cid:17)1.15 |     |                      |     |               | (cid:16) | (cid:17)−0.14 |
| (c)L=L0.61(r+1)1.80 |     |               | 1+       | 1            |     | (d)L=L0.97(r+1)−1.05 |     |               | 1+       | 1             |
|                     | 0   |               |          | D+1          |     |                      | 0   |               |          | D+1           |
Figure11.(a-b)CompressionlawsofintrinsicandextrinsicperformanceofLLMscompressedwiththecalibration-basedmethodat
differentcompressionratios. DifferentlinesindicatedifferentL frontiers. (c-d)Impactofrecoveryfine-tuningontheintrinsicand
0
extrinsicperformanceofLLMscompressedwiththecalibration-basedmethodatdifferentcompressionratios.
performanceofthecalibration-freemethodismorestable. Similartotheablationw.r.tthecompressionratio,theexponents
ofthecompressionlawsforthecalibration-freemethodarelargerthanthoseofthecalibration-basedmethod.
D.6.InferencespeedofcompressedLLMs
Model compression significantly enhances the inference efficiency of LLMs by reducing computational overhead and
improvingprocessingspeed. AsshowninFigure6,inferenceruntimefollowsapower-lawrelationshipwithcompression
ratio, where larger models exhibit greater efficiency gains. Table 4 presents the fitted compression coefficients (β),
demonstratingthatmodelssuchasQwen-2.5-14BandLLaMA-3-8Bachievesubstantialinferencespeedups,withreductions
of nearly 60% at 90% compression. This trend indicates that larger models benefit more from compression, whereas
smallermodels(e.g.,Qwen-2.5-0.5B)showmoremodestimprovements. Qwen-2.5-7B(β =−1.93)achievesoneofthe
highestefficiencyimprovements,reducingruntimebyover50%at70%compression. Theempiricaldataalignswellwith
thefittedpower-lawcurves,confirmingthepredictabilityofcompression-drivenefficiencygains. However,whilehigher
compressionratiosaccelerateinference,theymayalsodegrademodelperformanceondownstreamtasks. Acompression
ratiobetween30-50%oftenprovidesagoodbalance,maintainingover80%ofthemodel’soriginalperformancewhile
improving inference speed by 24-35%. Therefore, an optimal balance must be maintained between compression ratio
andaccuracytoensurereal-worldusability. Thesefindingssuggestthatmodelcompressionisparticularlyvaluablefor
resource-constraineddeployments,wherereducinginferencetimeiscrucialforscalabilityandcost-effectiveness.
16