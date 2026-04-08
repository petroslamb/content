|     |     |     | Designing | Network | Design | Spaces |     |     |
| --- | --- | --- | --------- | ------- | ------ | ------ | --- | --- |
IlijaRadosavovic RajPrateekKosaraju RossGirshick KaimingHe PiotrDolla´r
FacebookAIResearch(FAIR)
Abstract
0202 raM 03  ]VC.sc[  1v87631.3002:viXra
|     |     |     |     |     |     |     | B   | A   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Inthiswork,wepresentanewnetworkdesignparadigm.
|          |            |         |                   |         | A B |     | C   |     |
| -------- | ---------- | ------- | ----------------- | ------- | --- | --- | --- | --- |
| Our goal | is to help | advance | the understanding | of net- |     | C   |     |     |
workdesignanddiscoverdesignprinciplesthatgeneralize
| acrosssettings. | Insteadoffocusingondesigningindividual |        |                |             |     |     |     |     |
| --------------- | -------------------------------------- | ------ | -------------- | ----------- | --- | --- | --- | --- |
| network         | instances, we                          | design | network design | spaces that |     |     |     |     |
Figure1.Designspacedesign.Weproposetodesignnetworkde-
| parametrize | populations | of networks. | The overall | process |     |     |     |     |
| ----------- | ----------- | ------------ | ----------- | ------- | --- | --- | --- | --- |
signspaces,whereadesignspaceisaparametrizedsetofpossible
isanalogoustoclassicmanualdesignofnetworks,butele-
|                             |     |     |                       |     | modelarchitectures.                         | Designspacedesignisakintomanualnet- |     |              |
| --------------------------- | --- | --- | --------------------- | --- | ------------------------------------------- | ----------------------------------- | --- | ------------ |
| vatedtothedesignspacelevel. |     |     | Usingourmethodologywe |     |                                             |                                     |     |              |
|                             |     |     |                       |     | workdesign,butelevatedtothepopulationlevel. |                                     |     | Ineachstepof |
explorethestructureaspectofnetworkdesignandarriveat ourprocesstheinputisaninitialdesignspaceandtheoutputisa
alow-dimensionaldesignspaceconsistingofsimple,regu- refineddesignspaceofsimplerorbettermodels. Following[21],
lar networks that we call RegNet. The core insight of the wecharacterizethequalityofadesignspacebysamplingmodels
andinspectingtheirerrordistribution.
RegNetparametrizationissurprisinglysimple: widthsand Forexample,inthefigure
depths of good networks can be explained by a quantized abovewestartwithaninitialdesignspaceAandapplytworefine-
mentstepstoyielddesignspacesBthenC.InthiscaseC⊆B⊆A
| linear function. | We  | analyze the | RegNet design | space and |     |     |     |     |
| ---------------- | --- | ----------- | ------------- | --------- | --- | --- | --- | --- |
(left),andtheerrordistributionsarestrictlyimprovingfromAtoB
arriveatinterestingfindingsthatdonotmatchthecurrent
toC(right).Thehopeisthatdesignprinciplesthatapplytomodel
| practiceofnetworkdesign. |     | TheRegNetdesignspacepro- |     |     |     |     |     |     |
| ------------------------ | --- | ------------------------ | --- | --- | --- | --- | --- | --- |
populationsaremorelikelytoberobustandgeneralize.
videssimpleandfastnetworksthatworkwellacrossawide
| rangeofflopregimes. |     | Undercomparabletrainingsettings |     |     |     |     |     |     |
| ------------------- | --- | ------------------------------- | --- | --- | --- | --- | --- | --- |
networks,NASautomaticallyfindsagoodmodelwithinthe
andflops,theRegNetmodelsoutperformthepopularEffi- searchspace. Recently,NAShasreceivedalotofattention
cientNetmodelswhilebeingupto5×fasteronGPUs.
andshownexcellentresults[34,18,29].
DespitetheeffectivenessofNAS,theparadigmhaslim-
itations. Theoutcomeofthesearchisasinglenetworkin-
1.Introduction
stancetunedtoaspecificsetting(e.g.,hardwareplatform).
Deepconvolutionalneuralnetworksaretheengineofvi- Thisissufficientinsomecases;however,itdoesnotenable
sualrecognition.Overthepastseveralyearsbetterarchitec- discoveryofnetworkdesignprinciplesthatdeepenourun-
tureshaveresultedinconsiderableprogressinawiderange derstanding and allow us to generalize to new settings. In
of visual recognition tasks. Examples include LeNet [15], particular,ouraimistofindsimplemodelsthatareeasyto
AlexNet [13], VGG [26], and ResNet [8]. This body of understand,buildupon,andgeneralize.
workadvancedboththeeffectivenessofneuralnetworksas Inthiswork,wepresentanewnetworkdesignparadigm
| wellasourunderstandingofnetworkdesign. |     |     |     | Inparticular, |               |                |                  |          |
| -------------------------------------- | --- | --- | --- | ------------- | ------------- | -------------- | ---------------- | -------- |
|                                        |     |     |     |               | that combines | the advantages | of manual design | and NAS. |
theabovesequenceofworksdemonstratedtheimportance Instead of focusing on designing individual network in-
ofconvolution,networkanddatasize,depth,andresiduals, stances, we design design spaces that parametrize popula-
networks.1
respectively. Theoutcomeoftheseworksisnotjustpartic- tions of Like in manual design, we aim for in-
ular network instantiations, but also design principles that terpretabilityandtodiscovergeneraldesignprinciplesthat
canbegeneralizedandappliedtonumeroussettings.
|     |     |     |     |     | describenetworksthataresimple, |     | workwell,andgeneral- |     |
| --- | --- | --- | --- | --- | ------------------------------ | --- | -------------------- | --- |
Whilemanualnetworkdesignhasledtolargeadvances, izeacrosssettings. LikeinNAS,weaimtotakeadvantage
findingwell-optimizednetworksmanuallycanbechalleng- ofsemi-automatedprocedurestohelpachievethesegoals.
ing,especiallyasthenumberofdesignchoicesincreases.A
1Weusethetermdesignspacefollowing[21],ratherthansearchspace,
popularapproachtoaddressthislimitationisneuralarchi-
toemphasizethatwearenotsearchingfornetworkinstanceswithinthe
tecturesearch(NAS).Givenafixedsearchspaceofpossible space.Instead,wearedesigningthespaceitself.
1

| Thegeneralstrategyweadoptistoprogressivelydesign |          |     |             |            |     |                |     | 2.RelatedWork |     |     |     |     |     |     |
| ------------------------------------------------ | -------- | --- | ----------- | ---------- | --- | -------------- | --- | ------------- | --- | --- | --- | --- | --- | --- |
| simplified                                       | versions | of  | an initial, | relatively |     | unconstrained, |     |               |     |     |     |     |     |     |
design space while maintaining or improving its quality Manualnetworkdesign.TheintroductionofAlexNet[13]
(Figure1). Theoverallprocessisanalogoustomanualde- catapulted network design into a thriving research area.
sign,elevatedtothepopulationlevelandguidedviadistri- In the following years, improved network designs were
butionestimatesofnetworkdesignspaces[21]. proposed; examples include VGG [26], Inception [27,
As a testbed for this paradigm, our focus is on ex- 28], ResNet [8], ResNeXt [31], DenseNet [11], and Mo-
ploring network structure (e.g., width, depth, groups, etc.) bileNet[9,25]. Thedesignprocessbehindthesenetworks
assuming standard model families including VGG [26], waslargelymanualandfocussedondiscoveringnewdesign
ResNet [8], and ResNeXt [31]. We start with a relatively choicesthatimproveaccuracye.g.,theuseofdeepermodels
unconstrained design space we call AnyNet (e.g., widths orresiduals. Welikewisesharethegoalofdiscoveringnew
anddepthsvaryfreelyacrossstages)andapplyourhuman- designprinciples. Infact,ourmethodologyisanalogousto
manualdesignbutperformedatthedesignspacelevel.
in-the-loopmethodologytoarriveatalow-dimensionalde-
signspaceconsistingofsimple“regular”networks,thatwe
|             |                                     |     |     |     |     |     |     | Automatednetworkdesign. |     |     | Recently,thenetworkdesign |     |     |     |
| ----------- | ----------------------------------- | --- | --- | --- | --- | --- | --- | ----------------------- | --- | --- | ------------------------- | --- | --- | --- |
| callRegNet. | ThecoreoftheRegNetdesignspaceissim- |     |     |     |     |     |     |                         |     |     |                           |     |     |     |
processhasshiftedfromamanualexplorationtomoreau-
ple: stagewidthsanddepthsaredeterminedbyaquantized
|                  |     |            |     |         |     |        |        | tomated   | network | design,   | popularized |             | by NAS. | NAS has |
| ---------------- | --- | ---------- | --- | ------- | --- | ------ | ------ | --------- | ------- | --------- | ----------- | ----------- | ------- | ------- |
| linear function. |     | Comparedto |     | AnyNet, | the | RegNet | design |           |         |           |             |             |         |         |
|                  |     |            |     |         |     |        |        | proven to | be an   | effective | tool        | for finding | good    | models, |
space has simpler models, is easier to interpret, and has a e.g.,[35,23,17,20,18,29]. ThemajorityofworkinNAS
higherconcentrationofgoodmodels.
focusesonthesearchalgorithm,i.e.,efficientlyfindingthe
| We design | the | RegNet | design | space | in a | low-compute, |     |              |           |     |          |        |          |          |
| --------- | --- | ------ | ------ | ----- | ---- | ------------ | --- | ------------ | --------- | --- | -------- | ------ | -------- | -------- |
|           |     |        |        |       |      |              |     | best network | instances |     | within a | fixed, | manually | designed |
low-epochregimeusingasinglenetworkblocktypeonIm-
|                       |     |        |                              |          |          |          |       | search space | (which             | we  | call a design |        | space).      | Instead, our |
| --------------------- | --- | ------ | ---------------------------- | -------- | -------- | -------- | ----- | ------------ | ------------------ | --- | ------------- | ------ | ------------ | ------------ |
| ageNet [3].           | We  | then   | show that                    | the      | RegNet   | design   | space |              |                    |     |               |        |              |              |
|                       |     |        |                              |          |          |          |       | focus is     | on a paradigm      |     | for designing |        | novel design | spaces.      |
| generalizes           | to  | larger | compute                      | regimes, | schedule | lengths, |       |              |                    |     |               |        |              |              |
|                       |     |        |                              |          |          |          |       | The two      | are complementary: |     | better        | design | spaces       | can im-      |
| andnetworkblocktypes. |     |        | Furthermore,animportantprop- |          |          |          |       |              |                    |     |               |        |              |              |
provetheefficiencyofNASsearchalgorithmsandalsolead
ertyofthedesignspacedesignisthatitismoreinterpretable
toexistenceofbettermodelsbyenrichingthedesignspace.
| andcanleadtoinsightsthatwecanlearnfrom. |     |     |     |     |     | Weanalyze |     |     |     |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
the RegNet design space and arrive at interesting findings Network scaling. Both manual and semi-automated net-
that do not match the current practice of network design. workdesigntypicallyfocusonfindingbest-performingnet-
|     |     |     |     |     |     |     |     | work instances |     | for a specific | regime | (e.g., | number | of flops |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | -------------- | ------ | ------ | ------ | -------- |
Forexample,wefindthatthedepthofthebestmodelsissta-
ble across compute regimes (∼20 blocks) and that the best comparable to ResNet-50). Since the result of this proce-
dureisasinglenetworkinstance,itisnotclearhowtoadapt
modelsdonotuseeitherabottleneckorinvertedbottleneck.
theinstancetoadifferentregime(e.g.,fewerflops).Acom-
| We compare |     | top REGNET |     | models | to existing | networks |     |     |     |     |     |     |     |     |
| ---------- | --- | ---------- | --- | ------ | ----------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
in various settings. First, models are surprisingly monpracticeistoapplynetworkscalingrules,suchasvary-
REGNET
ingnetworkdepth[8],width[32],resolution[9],orallthree
| effective | in the | mobile | regime. | We  | hope | that these | sim- |     |     |     |     |     |     |     |
| --------- | ------ | ------ | ------- | --- | ---- | ---------- | ---- | --- | --- | --- | --- | --- | --- | --- |
ple models can serve as strong baselines for future work. jointly[29]. Instead,ourgoalistodiscovergeneraldesign
|              |     |        |         |              |     |              |     | principles | that hold | across | regimes | and | allow | for efficient |
| ------------ | --- | ------ | ------- | ------------ | --- | ------------ | --- | ---------- | --------- | ------ | ------- | --- | ----- | ------------- |
| Next, REGNET |     | models | lead to | considerable |     | improvements |     |            |           |        |         |     |       |               |
tuningfortheoptimalnetworkinanytargetregime.
| over standard | RESNE(X)T |     | [8, | 31] | models | in all metrics. |     |     |     |     |     |     |     |     |
| ------------- | --------- | --- | --- | --- | ------ | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Wehighlighttheimprovementsforfixedactivations,which
|     |     |     |     |     |     |     |     | Comparingnetworks. |     |     | Giventhevastnumberofpossible |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | ---------------------------- | --- | --- | --- |
is of high practical interest as the number of activations networkdesignspaces,itisessentialtouseareliablecom-
| can strongly | influence |     | the runtime |     | on accelerators |     | such as |         |           |       |            |          |     |               |
| ------------ | --------- | --- | ----------- | --- | --------------- | --- | ------- | ------- | --------- | ----- | ---------- | -------- | --- | ------------- |
|              |           |     |             |     |                 |     |         | parison | metric to | guide | our design | process. |     | Recently, the |
GPUs. Next,wecomparetothestate-of-the-artEFFICIENT- authorsof[21]proposedamethodologyforcomparingand
NET [29] models across compute regimes. Under compa- analyzing populations of networks sampled from a design
| rable training | settings |     | and flops, | REGNET |     | models | outper- |                                                         |     |     |     |     |     |     |
| -------------- | -------- | --- | ---------- | ------ | --- | ------ | ------- | ------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
|                |          |     |            |        |     |        |         | space. Thisdistribution-levelviewisfully-alignedwithour |     |     |     |     |     |     |
formEFFICIENTNETmodelswhilebeingupto5×fasteron goal of finding general design principles. Thus, we adopt
GPUs. WefurthertestgeneralizationonImageNetV2[24].
thismethodologyanddemonstratethatitcanserveasause-
We note that network structure is arguably the simplest fultoolforthedesignspacedesignprocess.
| form of | a design | space | design | one | can consider. | Focusing |     |                   |     |     |                 |     |        |             |
| ------- | -------- | ----- | ------ | --- | ------------- | -------- | --- | ----------------- | --- | --- | --------------- | --- | ------ | ----------- |
|         |          |       |        |     |               |          |     | Parameterization. |     | Our | final quantized |     | linear | parameteri- |
ondesigningricherdesignspaces(e.g.,includingoperators)
zationsharessimilaritywithpreviouswork,e.g.howstage
mayleadtobetternetworks.Nevertheless,thestructurewill
|     |     |     |     |     |     |     |     | widthsareset[26,7,32,11,9]. |     |     |     | However,therearetwokey |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------------- | --- | --- | --- | ---------------------- | --- | --- |
likelyremainacorecomponentofsuchdesignspaces.
|          |               |     |        |          |     |              |     | differences.            | First,weprovideanempiricalstudyjustifying |     |                           |     |     |     |
| -------- | ------------- | --- | ------ | -------- | --- | ------------ | --- | ----------------------- | ----------------------------------------- | --- | ------------------------- | --- | --- | --- |
| In order | to facilitate |     | future | research | we  | will release | all |                         |                                           |     |                           |     |     |     |
|          |               |     |        |          |     |              |     | thedesignchoiceswemake. |                                           |     | Second,wegiveinsightsinto |     |     |     |
codeandpretrainedmodelsintroducedinthiswork.2
|     |     |     |     |     |     |     |     | structural | design | choices | that were | not | previously | under- |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------ | ------- | --------- | --- | ---------- | ------ |
2https://github.com/facebookresearch/pycls stood(e.g.,howtosetthenumberofblocksineachstages).
2

3.DesignSpaceDesign 1.0
0.8
Our goal is to design better networks for visual recog- 0.6
0.4
nition. Ratherthandesigningorsearchingforasinglebest 0.2
modelunderspecificsettings,westudythebehaviorofpop- 0.0 40 45 50 55 60 65
error
ulationsofmodels.Weaimtodiscovergeneraldesignprin-
ciples that can apply to and improve an entire model pop-
ulation. Such design principles can provide insights into
networkdesignandaremorelikelytogeneralizetonewset-
tings(unlikeasinglemodeltunedforaspecificscenario).
We rely on the concept of network design spaces intro-
ducedbyRadosavovicetal.[21]. Adesignspaceisalarge,
possibly infinite, population of model architectures. The
core insight from [21] is that we can sample models from
adesignspace,givingrisetoamodeldistribution,andturn
totoolsfromclassicalstatisticstoanalyzethedesignspace.
Wenotethatthisdiffersfromarchitecturesearch,wherethe
goalistofindthesinglebestmodelfromthespace.
Inthiswork,weproposetodesignprogressivelysimpli-
fiedversionsofaninitial, unconstraineddesignspace. We
refer to this process as design space design. Design space
designisakintosequentialmanualnetworkdesign,butel-
evatedtothepopulationlevel. Specifically,ineachstepof
our design process the input is an initial design space and
theoutputisarefineddesignspace,wheretheaimofeach
designstepistodiscoverdesignprinciplesthatyieldpopu-
lationsofsimplerorbetterperformingmodels.
Webeginbydescribingthebasictoolsweusefordesign
space design in §3.1. Next, in §3.2 we apply our method-
ologytoadesignspace,calledAnyNet,thatallowsuncon-
strainednetworkstructures. In§3.3,afterasequenceofde-
signsteps,weobtainasimplifieddesignspaceconsistingof
onlyregular networkstructuresthatwenameRegNet. Fi-
nally,asourgoalisnottodesignadesignspaceforasingle
setting,butrathertodiscovergeneralprinciplesofnetwork
design that generalize to new settings, in §3.4 we test the
generalizationoftheRegNetdesignspacetonewsettings.
Relative to the AnyNet design space, the RegNet de-
signspaceis: (1)simplifiedbothintermsofitsdimension
andtypeofnetworkconfigurationsitpermits, (2)contains
ahigherconcentrationoftop-performingmodels,and(3)is
moreamenabletoanalysisandinterpretation.
3.1.ToolsforDesignSpaceDesign
Webeginwithanoverviewoftoolsfordesignspacede-
sign. To evaluate and compare design spaces, we use the
toolsintroducedbyRadosavovicetal.[21],whoproposeto
quantifythequalityofadesignspacebysamplingasetof
modelsfromthatdesignspaceandcharacterizingtheresult-
ingmodelerrordistribution. Thekeyintuitionbehindthis
approachisthatcomparingdistributionsismorerobustand
informative than using search (manual or automated) and
comparingthebestfoundmodelsfromtwodesignspaces.
.borp
evitalumuc
70
60
50
[39.0|49.0] AnyNetX 40
10 20 30 40 50
depth
rorre
70
60
50
40
200 400 600 800 1000
w4
rorre
Figure2.StatisticsoftheAnyNetXdesignspacecomputedwith
n = 500sampledmodels. Left: Theerrorempiricaldistribution
function(EDF)servesasourfoundationaltoolforvisualizingthe
qualityofthedesignspace. Inthelegendwereporttheminerror
andmeanerror(whichcorrespondstotheareaunderthecurve).
Middle: Distributionofnetworkdepthd(numberofblocks)ver-
suserror. Right: Distributionofblockwidthsinthefourthstage
(w )versuserror. Theblueshadedregionsarerangescontaining
4
thebestmodelswith95%confidence(obtainedusinganempirical
bootstrap),andtheblackverticallinethemostlikelybestvalue.
Toobtainadistributionofmodels, wesampleandtrain
nmodelsfromadesignspace. Forefficiency,weprimarily
dosoinalow-compute,low-epochtrainingregime. Inpar-
ticular,inthissectionweusethe400millionflop3(400MF)
regimeandtraineachsampledmodelfor10epochsonthe
ImageNet dataset [3]. We note that while we train many
models, each training run is fast: training 100 models at
400MFfor10epochsisroughlyequivalentinflopstotrain-
ingasingleResNet-50[8]modelat4GFfor100epochs.
As in [21], our primary tool for analyzing design space
quality is the error empirical distribution function (EDF).
TheerrorEDFofnmodelswitherrorse isgivenby:
i
n
1 X
F(e)= 1[e <e]. (1)
n i
i=1
F(e)givesthefractionofmodelswitherrorlessthane. We
showtheerrorEDFforn = 500sampledmodelsfromthe
AnyNetXdesignspace(describedin§3.2)inFigure2(left).
Given a population of trained models, we can plot and
analyze various network properties versus network error,
see Figure 2 (middle) and (right) for two examples taken
fromtheAnyNetXdesignspace. Suchvisualizationsshow
1D projections of a complex, high-dimensional space, and
can help obtain insights into the design space. For these
plots, we employ an empirical bootstrap4 [5] to estimate
thelikelyrangeinwhichthebestmodelsfall.
To summarize: (1) we generate distributions of models
obtainedbysamplingandtrainingnmodelsfromadesign
space, (2) we compute and plot error EDFs to summarize
designspacequality,(3)wevisualizevariouspropertiesofa
designspaceanduseanempiricalbootstraptogaininsight,
and(4)weusetheseinsightstorefinethedesignspace.
3Following common practice, we use flops to mean multiply-adds.
Moreover,weuseMFandGFtodenote106and109flops,respectively.
4Givennpairs(xi,ei)ofmodelstatisticxi (e.g.depth)andcorre-
spondingerrorei,wecomputetheempiricalbootstrapby: (1)sampling
withreplacement25%ofthepairs,(2)selectingthepairwithminerror
inthesample,(3)repeatingthis104times,andfinally(4)computingthe
95%CIfortheminxvalue.Themediangivesthemostlikelybestvalue.
3

|     |                |     |                |     |            |     |     |               | wi, ri, ri | wi, ri, ri    |     |          |
| --- | -------------- | --- | -------------- | --- | ---------- | --- | --- | ------------- | ---------- | ------------- | --- | -------- |
|     | n, 1, 1        |     | w4, r/32, r/32 |     | wi, ri, ri |     |     |               |            |               |     |          |
|     |                |     |                |     |            |     |     |               | ⨁          | ⨁             |     |          |
|     | head           |     | stage 4        |     | block di   |     |     | 1×1, s=1      |            | 1×1, s=1      |     |          |
|     |                |     | …              |     | …          |     |     |               |            |               |     |          |
|     | w4, r/32, r/32 |     |                |     |            |     |     | wi/bi, ri, ri |            | wi/bi, ri, ri |     |          |
|     | body           |     | stage 2        |     | block 2    |     |     | 3×3, gi, s=1  |            | 3×3, gi, s=2  |     | 1×1, s=2 |
w0, r/2, r/2 w1, r/4, r/4 wi, ri, ri wi/bi, ri, ri wi/bi, 2ri, 2ri
|     | stem |     | stage 1 |     | block 1 |     |     | 1×1, s=1 |     | 1×1, s=1 |     |     |
| --- | ---- | --- | ------- | --- | ------- | --- | --- | -------- | --- | -------- | --- | --- |
3, r, r w0, r/2, r/2 wi-1, 2ri, 2ri wi, ri, ri wi-1, 2ri, 2ri
(a) network  (b) body  (c) stage i (a)Xblock, s=1 (b) Xblock, s=2
Figure 3. General network structure for models in our design Figure4.TheXblockisbasedonthestandardresidualbottleneck
spaces. (a)Eachnetworkconsistsofastem(stride-two3×3conv blockwithgroupconvolution[31]. (a)EachXblockconsistsofa
withw =32outputchannels),followedbythenetworkbodythat 1×1conv,a3×3groupconv,andafinal1×1conv,wherethe1×1
0
performs the bulk of the computation, and then a head (average convsalterthechannelwidth. BatchNorm[12]andReLUfollow
poolingfollowedbyafullyconnectedlayer)thatpredictsnoutput eachconv. Theblockhas3parameters: thewidthw ,bottleneck
i
classes.(b)Thenetworkbodyiscomposedofasequenceofstages ratiob ,andgroupwidthg .(b)Thestride-two(s=2)version.
|                                              |     |     |     |     |                |     | i   |     | i   |     |     |     |
| -------------------------------------------- | --- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
| thatoperateatprogressivelyreducedresolutionr |     |     |     |     | . (c)Eachstage |     |     |     |     |     |     |     |
i
consists of a sequence of identical blocks, except the first block TheAnyNetXdesignspacehas16degreesoffreedomas
eachnetworkconsistsof4stagesandeachstageihas4pa-
whichusesstride-twoconv.Whilethegeneralstructureissimple,
thetotalnumberofpossiblenetworkconfigurationsisvast. rameters: thenumberofblocksd i , blockwidthw i , bottle-
|     |     |     |     |     |     |     | neckratiob | ,andgroupwidthg |     | .Wefixtheinputresolution |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --------------- | --- | ------------------------ | --- | --- |
|     |     |     |     |     |     |     |            | i               |     | i                        |     |     |
r = 224
3.2.TheAnyNetDesignSpace unless otherwise noted. To obtain valid models,
|     |     |     |     |     |     |     | weperformlog-uniformsamplingofd |     |     |     | ≤   | 16, w ≤ 1024 |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | ------------ |
|     |     |     |     |     |     |     |                                 |     |     |     | i   | i            |
WenextintroduceourinitialAnyNetdesignspace. Our and divisible by 8, b ∈ {1,2,4}, and g ∈ {1,2,...,32}
|       |                 |     |               |     |                 |     |          |       | i              |           | i   |                |
| ----- | --------------- | --- | ------------- | --- | --------------- | --- | -------- | ----- | -------------- | --------- | --- | -------------- |
| focus | is on exploring |     | the structure | of  | neural networks | as- |          |       |                |           |     |                |
|       |                 |     |               |     |                 |     | (we test | these | ranges later). | We repeat | the | sampling until |
suming standard, fixed network blocks (e.g., residual bot- weobtainn=500modelsinourtargetcomplexityregime
tleneckblocks). Inourterminologythestructureofthenet- (360MF to 400MF), and train each model for 10 epochs.5
work includes elements such as the number of blocks (i.e. BasicstatisticsforAnyNetXwereshowninFigure2.
networkdepth),blockwidths(i.e.numberofchannels),and Thereare(16·128·3·6)4 ≈1018possiblemodelconfigu-
| other | block parameters |     | such as | bottleneck | ratios | or group |     |     |     |     |     |     |
| ----- | ---------------- | --- | ------- | ---------- | ------ | -------- | --- | --- | --- | --- | --- | --- |
rationsintheAnyNetXdesignspace.Ratherthansearching
widths. Thestructureofthenetworkdeterminesthedistri- forthesinglebestmodeloutofthese∼1018configurations,
butionofcompute,parameters,andmemorythroughoutthe weexplorewhethertherearegeneraldesignprinciplesthat
computationalgraphofthenetworkandiskeyindetermin- canhelpusunderstandandrefinethisdesignspace. Todo
ingitsaccuracyandefficiency. so, we apply our approach of designing design spaces. In
|     | The basic design |     | of networks | in  | our AnyNet | design |     |     |     |     |     |     |
| --- | ---------------- | --- | ----------- | --- | ---------- | ------ | --- | --- | --- | --- | --- | --- |
eachstepofthisapproach,ouraimsare:
space is straightforward. Given an input image, a network 1. tosimplifythestructureofthedesignspace,
consistsofasimplestem,followedbythenetworkbodythat
2. toimprovetheinterpretabilityofthedesignspace,
performs the bulk of the computation, and a final network 3. toimproveormaintainthedesignspacequality,
| head | that predicts | the | output | classes, | see Figure | 3a. We |     |     |     |     |     |     |
| ---- | ------------- | --- | ------ | -------- | ---------- | ------ | --- | --- | --- | --- | --- | --- |
4. tomaintainmodeldiversityinthedesignspace.
keepthestemandheadfixedandassimpleaspossible,and
WenowapplythisapproachtotheAnyNetXdesignspace.
| instead | focus on | the | structure | of the network | body | that is |     |     |     |     |     |     |
| ------- | -------- | --- | --------- | -------------- | ---- | ------- | --- | --- | --- | --- | --- | --- |
centralindeterminingnetworkcomputeandaccuracy. AnyNetX A .Forclarity,goingforwardwerefertotheinitial,
Thenetworkbodyconsistsof4stagesoperatingatpro- unconstrainedAnyNetXdesignspaceasAnyNetX .
A
gressively reduced resolution, see Figure 3b (we explore AnyNetX . We first test a shared bottleneck ratio b = b
|                                  |     |     |     |     |                   |     |         | B      |                   |        |        | i         |
| -------------------------------- | --- | --- | --- | --- | ----------------- | --- | ------- | ------ | ----------------- | ------ | ------ | --------- |
| varyingthenumberofstagesin§3.4). |     |     |     |     | Eachstageconsists |     |         |        |                   |        |        |           |
|                                  |     |     |     |     |                   |     | for all | stages | i for the AnyNetX | design | space, | and refer |
A
ofasequenceofidenticalblocks,seeFigure3c.Intotal,for to the resulting design space as AnyNetX . As before, we
B
eachstageithedegreesoffreedomincludethenumberof
|         |              |     |                              |     |     |     | sample    | and train        | 500 models | from       | AnyNetX | B in the same |
| ------- | ------------ | --- | ---------------------------- | --- | --- | --- | --------- | ---------------- | ---------- | ---------- | ------- | ------------- |
| blocksd | ,blockwidthw |     | ,andanyotherblockparameters. |     |     |     |           |                  |            |            |         |               |
|         | i            |     | i                            |     |     |     | settings. | TheEDFsofAnyNetX |            | andAnyNetX |         | ,shownin      |
|         |              |     |                              |     |     |     |           |                  |            | A          |         | B             |
While the general structure is simple, the total number of Figure5(left),arevirtuallyidenticalbothintheaverageand
possiblenetworksintheAnyNetdesignspaceisvast.
|     |     |     |     |     |     |     | bestcase. | Thisindicatesnolossinaccuracywhencoupling |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | ----------------------------------------- | --- | --- | --- | --- |
Mostofourexperimentsusethestandardresidualbottle- theb . Inadditiontobeingsimpler,theAnyNetX ismore
|     |     |     |     |     |     |     | i   |     |     |     |     | B   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
necksblockwithgroupconvolution[31],showninFigure4.
amenabletoanalysis,seeforexampleFigure5(right).
WerefertothisastheXblock,andtheAnyNetdesignspace
|       |                  |     |             |       |        |           | 5Ourtrainingsetupin§3exactlyfollows[21]. |     |     |     | WeuseSGDwithmo- |     |
| ----- | ---------------- | --- | ----------- | ----- | ------ | --------- | ---------------------------------------- | --- | --- | --- | --------------- | --- |
| built | on it as AnyNetX |     | (we explore | other | blocks | in §3.4). |                                          |     |     |     |                 |     |
mentumof0.9,mini-batchsizeof128on1GPU,andahalf-periodcosine
| While | the X block | is  | quite rudimentary, |     | we show | it can be |     |     |     |     |     |     |
| ----- | ----------- | --- | ------------------ | --- | ------- | --------- | --- | --- | --- | --- | --- | --- |
schedulewithinitiallearningrateof0.05andweightdecayof5·10−5.
surprisinglyeffectivewhennetworkstructureisoptimized. Tenepochsareusuallysufficienttogiverobustpopulationstatistics.
4

1.0
0.8
0.6
0.4
0.2
0.0
40 45 50 55 60 65 70
error
.borp
evitalumuc
1.0
0.8
0.6
0.4
[39.0|49.0] AnyNetXA0.2
[39.0|49.2] AnyNetXB
0.0
40 50 60 70
error
.borp
evitalumuc
70
60
50
[39.0|49.2] AnyNetXB
[38.9|49.4] AnyNetXC 40
1 2 4
b
rorre
Figure5.AnyNetX B (left)andAnyNetX C (middle)introducea
shared bottleneck ratio b = b and shared group width g = g, i i
respectively. Thissimplifiesthedesignspaceswhileresultingin
virtuallynochangeintheerrorEDFs. Moreover,AnyNetX Band
AnyNetX C aremoreamendabletoanalysis. Applyinganempir-
ical bootstrap to b and g we see trends emerge, e.g., with 95%
confidenceb≤2isbestinthisregime(right).Nosuchtrendsare
evidentintheindividualb i andg i inAnyNetX A(notshown).
1024
256
64
0 1 2 3 4 5 6 7 8
htdiw
d wi i = = [ [ 1 4 , 8 2 , , 8 2 0 , , 4 3 ] 52,560] d wi i = = [ [ 2 6 , 4 3 , , 1 1 2 , 8 6 , ] 448,656] d wi i = = [ [ 2 4 , 8 7 , , 4 1 8 7 , , 2 6 0 ] 8,608] g=8, b=1, e=38.9% g=8, b=2, e=39.7% g=8, b=2, e=40.4%
0 2 4 6 8 10 0 4 8 12 16 20 24 28
1024
256
64
0 1 2 3 4 block index
htdiw
1.0
0.8
0.6
0.4
0.2
0.0
40 50 60 70
error
d wi
i
=
=
[
[
1
4
,
8
1
,
,
7
1
0
,
4
2
,
]
32,48]
d wi
i
=
=
[
[
3
4
,
8
2
,
,
5
2
7
,
6
4
,
]
128,32]
d wi
i
=
=
[
[
1
6
,
4
1
,
,
9
9
6
,
0
9
,
]
64,64]
g=8, b=2, e=72.0% g=8, b=4, e=65.7% g=8, b=4, e=65.0%
0 2 4 6 8 10 0 2 4 6 8 1012141618 block index block index
Figure6.ExamplegoodandbadAnyNetX Cnetworks,shownin
thetopandbottomrows,respectively. Foreachnetwork,weplot
thewidthw ofeveryblockj uptothenetworkdepthd. These j
per-blockwidthsw arecomputedfromtheper-stageblockdepths
j
d andblockwidthsw (listedinthelegendsforreference).
i i
AnyNetX . Oursecondrefinementstepcloselyfollowsthe
C
first. StartingwithAnyNetX ,weadditionallyuseashared B
groupwidthg = g forallstagestoobtainAnyNetX . As
i C
before,theEDFsarenearlyunchanged,seeFigure5(mid-
dle). Overall, AnyNetX has 6 fewer degrees of freedom
C
than AnyNetX , and reduces the design space size nearly
A
four orders of magnitude. Interestingly, we find g > 1 is
best(notshown);weanalyzethisinmoredetailin§4.
AnyNetX . Next,weexaminetypicalnetworkstructuresof
D
both good and bad networks from AnyNetX in Figure 6.
C
A pattern emerges: good network have increasing widths.
Wetestthedesignprincipleofw ≥ w ,andrefertothe
i+1 i
designspacewiththisconstraintasAnyNetX . InFigure7
D
(left)weseethisimprovestheEDFsubstantially.Wereturn
toexaminingotheroptionsforcontrollingwidthshortly.
AnyNetX . Upon further inspection of many models (not E
shown),weobservedanotherinterestingtrend. Inaddition
to stage widths w increasing with i, the stage depths d i i
likewisetendto increaseforthebestmodels, although not
necessarilyinthelaststage. Nevertheless,wetestadesign
spacevariantAnyNetX withd ≥d inFigure7(right),
E i+1 i
and see it also improves results. Finally, we note that the
constraintsonw andd eachreducethedesignspaceby4!,
i i
withacumulativereductionofO(107)fromAnyNetX .
A
.borp
evitalumuc
1.0
0.8
0.6
[38.9|49.4] AnyNetXC
[38.7|43.2] + wi+1 wi 0.4
[47.5|56.1] + wi+1=wi 0.2
[52.2|63.2] + wi+1 wi
0.0
40 45 50 55
error
.borp
evitalumuc
[38.7|43.2] AnyNetXD
[38.7|42.7] + di+1 di
[39.0|46.6] + di+1=di
[41.0|48.8] + di+1 di
Figure7.AnyNetX D(left)andAnyNetX E(right). Weshowvar-
iousconstraintsontheperstagewidthsw anddepthsd . Inboth i i
cases,havingincreasingw andd isbeneficial,whileusingcon-
i i
stantordecreasingvaluesismuchworse. NotethatAnyNetX D
= AnyNetX C + w i+1 ≥ w i , and AnyNetX E = AnyNetX D +
d ≥d .Weexplorestrongerconstraintsonw andd shortly.
i+1 i i i
1024
512
256
128
64
32 0 3 6 9 12 15 18 21 block index
htdiw
512
256
128
64
32 0 2 4 6 8 10 12 14 block index
htdiw
d w g i i = = = 4 [ [ 2 , 6 , b 4 4 , = , 1 5 2 2 , , 8 5 e , ] 2 = 7 3 2 8 ,7 .7 0 % 4] d w g i i = = = 1 [ [ 1 6 3 , , 2 1 b , , 1 = 3 4 , 1 4 5 , , ] 2 e 5 = 6 3 ,4 9 4 .7 8 % ]
wa=30, w0=80, wm=1.9 wa=61, w0=48, wm=2.2 0 1 2 3 4 5 6 7 8 9 block index
80
70
60
50
40
0 1 2 3 4 5
efit
rorre
AnyNetXC AnyNetXD AnyNetXE
0 1 2 3 4 5 0 1 2 3 4 5
efit efit
Figure 8. Linear fits. Top networks from the AnyNetX design
spacecanbewellmodeledbyaquantizedlinearparameterization,
and conversely, networks for which this parameterization has a
higherfittingerrore tendtoperformpoorly.Seetextfordetails.
fit
3.3.TheRegNetDesignSpace
Togainfurtherinsightintothemodelstructure,weshow
thebest20modelsfromAnyNetX inasingleplot,seeFig- E
ure8(top-left).Foreachmodel,weplottheper-blockwidth
w ofeveryblockjuptothenetworkdepthd(weuseiand j
j to index over stages and blocks, respectively). See Fig-
ure6forreferenceofourmodelvisualization.
Whilethereissignificantvarianceintheindividualmod-
els(graycurves),intheaggregateapatternemerges.Inpar-
ticular,inthesameplotweshowthelinew =48·(j+1)for
j
0≤j ≤20(solidblackcurve,pleasenotethatthey-axisis
logarithmic). Remarkably,thistriviallinearfitseemstoex-
plainthepopulationtrendofthegrowthofnetworkwidths
fortopmodels. Note,however,thatthislinearfitassignsa
differentwidthw toeachblock,whereasindividualmodels
j
havequantizedwidths(piecewiseconstantfunctions).
To see if a similar pattern applies to individual models,
weneedastrategytoquantizealinetoapiecewiseconstant
function. InspiredbyourobservationsfromAnyNetX and
D
AnyNetX , we propose the following approach. First, we E
introducealinearparameterizationforblockwidths:
u =w +w ·j for 0≤j <d (2)
j 0 a
Thisparameterizationhasthreeparameters: depthd,initial
width w > 0, and slope w > 0, and generates a differ-
0 a
ent block width u for each block j < d. To quantize u ,
j j
5

.borp evitalumuc 1.0 .borp evitalumuc 1.0 55 A n yN e t X A restriction dim. combinations total
0.8 0.8 R eg N e t X AnyNetXA none 16 (16·128·3·6)4 ∼1.8·1018
|     |     |     |     |     | 50    |     |     | AnyNetXB |     |          |     | (16·128·6)4·3 |     | ∼6.8·1016 |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | -------- | --- | -------- | --- | ------------- | --- | --------- | --- |
| 0.6 |     |     | 0.6 |     | rorre |     |     |          |     | +bi+1=bi | 13  |               |     |           |     |
|     |     |     |     |     |       |     |     | AnyNetXC |     | +gi+1=gi | 10  | (16·128)4·3·6 |     | ∼3.2·1014 |     |
0.4 [39.0|49.0] AnyNetXA 0.4 [38.2|41.0] RegNetX  45 AnyNetXD (16·128)4·3·6/(4!) ∼1.3·1013
|     | [38.7|42.7] AnyNetXE |     | [38.0|40.7] RegNetX wm=2 |     |     |     |     |     |     | +wi+1≥wi | 10  |     |     |     |     |
| --- | -------------------- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
0.2 0.2 [38.2|40.1] RegNetX w0=wa 40 AnyNetXE +di+1≥di 10 (16·128)4·3·6/(4!)2 ∼5.5·1011
| 0.0 | [38.2|41.0] RegNetX |     | 0.0 |     |     |     |     | RegNet |     |     |     | ∼644·6·3 |     | ∼3.0·108 |     |
| --- | ------------------- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | -------- | --- | -------- | --- |
40 45 50 55 60 65 38 40 42 44 46 2 8 32 128 quantizedlinear 6
|     | error |     |     | error |     | sample size |     |     |     |     |     |     |     |     |     |
| --- | ----- | --- | --- | ----- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Table1.Designspacesummary.Seetextfordetails.
Figure9.RegNetXdesignspace.Seetextfordetails.
| weintroduceanadditionalparameterw |     |             |        |       |        | >0thatcontrols |         |                      |     |     |     |     |     |     |     |
| --------------------------------- | --- | ----------- | ------ | ----- | ------ | -------------- | ------- | -------------------- | --- | --- | --- | --- | --- | --- | --- |
|                                   |     |             |        |       | m      |                |         | .borp evitalumuc 1.0 |     |     |     |     |     |     |     |
| quantization                      |     | as follows. | First, | given | u from | Eqn.           | (2), we | 0.8                  |     |     |     |     |     |     |     |
j
computes foreachblockjsuchthatthefollowingholds: 0.6 flops=800M epochs=50 stages=5
j 0.4 [35.8|44.5] AnyNetXA [30.0|38.8] AnyNetXA [40.4|49.9] AnyNetXA
|     |     |     |      |      |     |     |     |     | [35.1|38.5] AnyNetXE |     |     | [30.0|32.5] AnyNetXE |     | [38.4|42.8] AnyNetXE |     |
| --- | --- | --- | ---- | ---- | --- | --- | --- | --- | -------------------- | --- | --- | -------------------- | --- | -------------------- | --- |
|     |     |     | u =w | ·wsj |     |     | (3) | 0.2 |                      |     |     |                      |     |                      |     |
j 0 m 0.0 [34.6|36.8] RegNetX [29.4|31.5] RegNetX [37.9|41.4] RegNetX
|                                     |     |     |                 |     |     |              |     | 35                   | 40 45 50 | 55 60 | 30 35 40 | 45 50 | 55 60 | 40 45 50 55 60 | 65 70 |
| ----------------------------------- | --- | --- | --------------- | --- | --- | ------------ | --- | -------------------- | -------- | ----- | -------- | ----- | ----- | -------------- | ----- |
| Then,toquantizeu                    |     |     | ,wesimplyrounds |     |     | (denotedbybs | e)  |                      |          |       |          |       |       |                |       |
|                                     |     | j   |                 |     | j   |              | j   | .borp evitalumuc 1.0 |          |       |          |       |       |                |       |
| andcomputequantizedper-blockwidthsw |     |     |                 |     |     | j via:       |     | 0.8                  |          |       |          |       |       |                |       |
0.6
·wbsje
w =w (4) 0.4 [42.9|53.1] AnyNetRA [47.0|61.2] AnyNetVA [48.1|58.9] AnyNetVRA
j 0 m 0.2 [42.0|45.7] AnyNetRE [46.8|56.4] AnyNetVE [47.4|53.3] AnyNetVRE
|                           |     |     |     |                        |     |     |     |     | [41.9|44.3] RegNetR |          |     | [46.0|49.2] RegNetV |     | [46.6|49.3] RegNetVR |       |
| ------------------------- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | ------------------- | -------- | --- | ------------------- | --- | -------------------- | ----- |
| Wecanconverttheper-blockw |     |     |     | toourper-stageformatby |     |     |     | 0.0 |                     |          |     |                     |     |                      |       |
|                           |     |     |     | j                      |     |     |     | 45  | 50 55               | 60 65 70 | 50  | 60 70               | 80  | 50 55 60             | 65 70 |
simplycountingthenumberofblockswithconstantwidth, error error error
|     |     |     |     |     |     |     |     | Figure10.RegNetXgeneralization. |     |     |     |     | WecompareRegNetXto |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | ------------------ | --- | --- |
·wi
| thatis,eachstageihasblockwidthw |     |     |      |       | i =w                | 0 m andnum- |     | AnyNetX |           |       |             |        |        |               |     |
| ------------------------------- | --- | --- | ---- | ----- | ------------------- | ----------- | --- | ------- | --------- | ----- | ----------- | ------ | ------ | ------------- | --- |
|                                 |     | P   |      |       |                     |             |     |         | at higher | flops | (top-left), | higher | epochs | (top-middle), |     |
| berofblocksd                    |     | =   | 1[bs | e=i]. | Whenonlyconsidering |             |     |         |           |       |             |        |        |               |     |
i j j with 5-stage networks (top-right), and with various block types
fourstagenetworks,weignoretheparametercombinations
|     |     |     |     |     |     |     |     | (bottom). | Inallcasestheorderingofthedesignspacesisconsis- |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ----------------------------------------------- | --- | --- | --- | --- | --- | --- |
thatgiverisetoadifferentnumberofstages. tentandweseenosignsofdesignspaceoverfitting.
| We       | test this | parameterization |       | by  | fitting | to models  | from |                                         |     |     |     |     |     |                |     |
| -------- | --------- | ---------------- | ----- | --- | ------- | ---------- | ---- | --------------------------------------- | --- | --- | --- | --- | --- | -------------- | --- |
| AnyNetX. | In        | particular,      | given | a   | model,  | we compute | the  |                                         |     |     |     |     |     |                |     |
|          |           |                  |       |     |         |            |      | simplifyingthelinearparameterizationtou |     |     |     |     |     | j =w a ·(j+1). |     |
fitbysettingdtothenetworkdepthandperformingagrid
|             |     |                                            |     |                            |     |     |     | Interestingly,thisperformsevenbetter.                |     |     |     |     | However,tomain- |     |     |
| ----------- | --- | ------------------------------------------ | --- | -------------------------- | --- | --- | --- | ---------------------------------------------------- | --- | --- | --- | --- | --------------- | --- | --- |
| searchoverw |     | ,w andw                                    |     | tominimizethemeanlog-ratio |     |     |     |                                                      |     |     |     |     |                 |     |     |
|             |     | 0 a                                        | m   |                            |     |     |     | tainthediversityofmodels,wedonotimposeeitherrestric- |     |     |     |     |                 |     |     |
| (denotedbye |     | fit )ofpredictedtoobservedper-blockwidths. |     |                            |     |     |     |                                                      |     |     |     |     |                 |     |     |
tion.Finally,inFigure9(right)weshowthatrandomsearch
| Results   | for | two top      | networks | from      | AnyNetX | are  | shown   |                                                    |     |     |     |     |     |     |     |
| --------- | --- | ------------ | -------- | --------- | ------- | ---- | ------- | -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|           |     |              |          |           |         | E    |         | efficiencyismuchhigherforRegNetX;searchingoverjust |     |     |     |     |     |     |     |
| in Figure | 8   | (top-right). | The      | quantized | linear  | fits | (dashed |                                                    |     |     |     |     |     |     |     |
∼32randommodelsislikelytoyieldgoodmodels.
curves)aregoodfitsofthesebestmodels(solidcurves).
Next, we plot the fitting error e versus network error Table1showsasummaryofthedesignspacesizes(for
fit
|                          |     |     |     |                  |     |     |        | RegNet | we estimate |     | the size | by quantizing |     | its continuous |     |
| ------------------------ | --- | --- | --- | ---------------- | --- | --- | ------ | ------ | ----------- | --- | -------- | ------------- | --- | -------------- | --- |
| foreverynetworkinAnyNetX |     |     |     | C throughAnyNetX |     | E   | inFig- |        |             |     |          |               |     |                |     |
parameters).IndesigningRegNetX,wereducedthedimen-
| ure8(bottom). |     | First, | wenotethatthebestmodelsineach |     |     |     |     |     |     |     |     |     |     |     |     |
| ------------- | --- | ------ | ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
design space all have good linear fits. Indeed, an empiri- sionoftheoriginalAnyNetXdesignspacefrom16to6di-
|               |     |         |        |      |      |             |        | mensions, | andthesizenearly10ordersofmagnitude. |     |     |     |     |     | We  |
| ------------- | --- | ------- | ------ | ---- | ---- | ----------- | ------ | --------- | ------------------------------------ | --- | --- | --- | --- | --- | --- |
| cal bootstrap |     | gives a | narrow | band | of e | near 0 that | likely |           |                                      |     |     |     |     |     |     |
fit
containsthebestmodelsineachdesignspace. Second,we note, however, that RegNet still contains a good diversity
ofmodelsthatcanbetunedforavarietyofsettings.
| note that | on  | average,                                  | e fit improves |     | going | from AnyNetX | C   |     |     |     |     |     |     |     |     |
| --------- | --- | ----------------------------------------- | -------------- | --- | ----- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| toAnyNetX |     | ,showingthatthelinearparametrizationnatu- |                |     |       |              |     |     |     |     |     |     |     |     |     |
E
rallyenforcesrelatedconstraintstow andd increasing. 3.4.DesignSpaceGeneralization
|     |         |          |        |                   | i   | i         |     |     |     |     |     |     |     |     |     |
| --- | ------- | -------- | ------ | ----------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| To  | further | test the | linear | parameterization, |     | we design | a   |     |     |     |     |     |     |     |     |
design space that only contains models with such linear WedesignedtheRegNetdesignspaceinalow-compute,
|            |                                             |     |     |     |     |     |     | low-epoch | training | regime | with | only | a single | block | type. |
| ---------- | ------------------------------------------- | --- | --- | --- | --- | --- | --- | --------- | -------- | ------ | ---- | ---- | -------- | ----- | ----- |
| structure. | Inparticular,wespecifyanetworkstructurevia6 |     |     |     |     |     |     |           |          |        |      |      |          |       |       |
However,ourgoalisnottodesignadesignspaceforasin-
| parameters: |     | d,w ,w | ,w  | (andalsob,g). |     | Giventhese,we |     |     |     |     |     |     |     |     |     |
| ----------- | --- | ------ | --- | ------------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|             |     | 0      | a m |               |     |               |     |     |     |     |     |     |     |     |     |
generateblockwidthsanddepthsviaEqn.(2)-(4). Werefer glesetting,butrathertodiscovergeneralprinciplesofnet-
workdesignthatcangeneralizetonewsettings.
totheresultingdesignspaceasRegNet,asitcontainsonly
simple,regularmodels. Wesampled<64,w ,w <256, InFigure10,wecomparetheRegNetXdesignspaceto
|       |     |           |     |     |     | 0 a |     |     |     |     |     |     |     |     |     |
| ----- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.5 ≤ | w ≤ | 3andbandg |     |     |     |     |     |     |     |     |     |     |     |     |     |
m asbefore(rangessetbasedon AnyNetX A and AnyNetX E at higher flops, higher epochs,
e onAnyNetX ). with 5-stage networks, and with various block types (de-
| fit |     | E   |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The error EDF of RegNetX is shown in Figure 9 scribed in the appendix). In all cases the ordering of the
(left). Models in RegNetX have better average error than designspacesisconsistent,withRegNetX>AnyNetX E >
AnyNetX while maintaining the best models. In Figure 9 AnyNetX . In other words, we see no signs of overfitting.
A
(middle) we test two further simplifications. First, using TheseresultsarepromisingbecausetheyshowRegNetcan
w =2(doublingwidthbetweenstages)slightlyimproves generalize to new settings. The 5-stage results show the
m
the EDF, but we note that using w ≥ 2 performs better regularstructureofRegNetcangeneralizetomorestages,
m
(shown later). Second, we test setting w 0 = w a , further whereAnyNetX A hasevenmoredegreesoffreedom.
6

60
50 40 30 20 10 d
all 4.0
good 3.5 best 3.0 2.5 2.0 1.5 1.0 b
all 3.00
good 2.75 best 2.50 2.25 2.00 1.75 1.50 mw
all
good best 30
25 20 15 10
5
0
0.2 0.4 0.8 1.6 3.2 6.4 12.8
flops (B)
g
all 250
g b o e o st d 200 150 100
50
0
0.2 0.4 0.8 1.6 3.2 6.4 12.8
flops (B)
aw
all 250
g b o e o st d 200 150 100
50
0
0.2 0.4 0.8 1.6 3.2 6.4 12.8
flops (B)
0w
all
good best
Figure11.RegNetXparametertrends. Foreachparameterand
each flop regime we apply an empirical bootstrap to obtain the
rangethatcontainsbestmodelswith95%confidence(shownwith
blueshading)andthelikelybestmodel(blackline),seealsoFig-
ure2.Weobservethatforbestmodelsthedepthsdareremarkably
stableacrossflops regimes, andb = 1andw ≈ 2.5arebest.
m
Blockandgroupswidths(w ,w ,g)tendtoincreasewithflops.
a 0
flops paramsacts. 60
1×1conv w2r2 w2 wr2 50
3×3conv 32w2r2 32w2 wr2 40 3×3grconv 32wgr2 32wg wr2 30
3×3dwconv 32wr2 32w wr2 20 10
0.2 0.4 0.6 0.8 1.0 1.2 1.4 1.6 flops (B)
)sm(
emit
ecnerefni
60
50
40 30
20 r=0.643 10 r=0.897
2 4 6 8 10 12 14 activations (M)
30 25 20 15 10
5
0.2 0.4 0.8 1.6 3.2 6.4 12.8
flops (B)
)M( snoitavitca all 200 g b o e o st d 150 6 R . e 5 sN f et 100 ResNeXt 50
0
0.2 0.4 0.8 1.6 3.2 6.4 12.8
flops (B)
)M( smarap 300 all good 250 best 200 3.0+5.5f ResNet 150 ResNeXt 100
50 0
0.2 0.4 0.8 1.6 3.2 6.4 12.8
flops (B)
)sm( emit ecnerefni
1.0
0.8 0.6 0.4 0.2 0.0 25.0 27.5 30.0 32.5 35.0 37.5
error
all good best 24f+6.0f ResNet ResNeXt
Figure 12. Complexity metrics. Top: Activations can have a
strongercorrelationtoruntimeonhardwareacceleratorsthanflops
(wemeasureinferencetimefor64imagesonanNVIDIAV100
GPU).Bottom: Trendanalysisofcomplexityvs.flopsandbestfit
curves(showninblue)ofthetrendsforbestmodels(blackcurves).
4.AnalyzingtheRegNetXDesignSpace
We next further analyze the RegNetX design space and
revisitcommondeepnetworkdesignchoices. Ouranalysis
yieldssurprisinginsightsthatdon’tmatchpopularpractice,
whichallowsustoachievegoodresultswithsimplemodels.
As the RegNetX design space has a high concentration
ofgoodmodels,forthefollowingresultsweswitchtosam-
pling fewer models (100) but training them for longer (25
epochs) with a learning rate of 0.1 (see appendix). We do
sotoobservemorefine-grainedtrendsinnetworkbehavior.
RegNettrends. WeshowtrendsintheRegNetXparame-
tersacrossflopregimesinFigure11.Remarkably,thedepth
of best models is stable across regimes (top-left), with an
optimaldepthof∼20blocks(60layers). Thisisincontrast
to the common practice of using deeper models for higher
flop regimes. We also observe that the best models use a
bottleneckratiobof1.0(top-middle),whicheffectivelyre-
moves the bottleneck (commonly used in practice). Next,
we observe that the width multiplier w of good models
m
is ∼2.5 (top-right), similar but not identical to the popular
recipeofdoublingwidthsacrossstages. Theremainingpa-
rameters(g,w ,w )increasewithcomplexity(bottom).
a 0
.borp
evitalumuc
40
[31.1|33.4] 400MF U 35 [30.7|32.6] 400MF C [28.3|30.3] 800MF U 30 [28.0|29.3] 800MF C [24.1|25.9] 3.2GF U 25 [24.0|25.2] 3.2GF C 0.2 0.4 0.8 1.6 3.2 6.4
flops (B)
rorre
RegNetX U 200
RegNetX C 150 100 50 0 0.2 0.4 0.8 1.6 3.2 6.4
flops (B)
)M( smarap
RegNetX U
RegNetX C
Figure 13. We refine RegNetX using various constraints (see text). Theconstrainedvariant(C)isbestacrossallflopregimes
whilebeingmoreefficientintermsofparametersandactivations.
1.0
0.8
0.6
0.4
0.2
0.0
32 34 36 38
error
.borp
evitalumuc
1.0
0.8
0.6
[30.7|32.6] b=1,g 320.4
[30.5|33.3] b 1,g 320.2
[33.2|35.5] b 1,g=1 0.0
30 35 40 45
error
.borp
evitalumuc
1.0
0.8
0.6
[30.7|32.6] 400MF r=224
[31.2|34.1] 400MF r 4480.4
[28.0|29.3] 800MF r=2240.2
[28.2|30.8] 800MF r 448 0.0
30 31 32 33 34
error
.borp
evitalumuc
[30.7|32.6] RegNetX
[29.8|31.3] RegNetY
Figure14.WeevaluateRegNetXwithalternatedesignchoices.
Left:Invertedbottleneck(1 ≤b≤1)degradesresultsanddepth-
8
wiseconv(g = 1)isevenworse. Middle: Varyingresolutionr
harmsresults.Right:RegNetY(Y=X+SE)improvestheEDF.
Complexityanalysis. Inadditiontoflopsandparameters,
weanalyzenetworkactivations,whichwedefineasthesize
oftheoutputtensorsofallconvlayers(welistcomplexity
measuresofcommonconvoperatorsinFigure12,top-left). Whilenotacommonmeasureofnetworkcomplexity,acti- vationscanheavilyaffectruntimeonmemory-boundhard-
wareaccelerators(e.g.,GPUs,TPUs),forexample,seeFig-
ure12(top). InFigure12(bottom),weobservethatforthe
bestmodelsinthepopulation,activationsincreasewiththe
square-rootofflops, parametersincreaselinearly, andrun-
time is best modeled using both a linear and a square-root
termduetoitsdependenceonbothflopsandactivations.
RegNetXconstrained. Usingthesefindings,werefinethe
RegNetXdesignspace. First,basedonFigure11(top),we
setb = 1,d ≤ 40,andw ≥ 2. Second,welimitparam-
m
eters and activations, following Figure 12 (bottom). This
yieldsfast,low-parameter,low-memorymodelswithoutaf-
fectingaccuracy.InFigure13,wetestRegNetXwiththeses
constraintsandobservethattheconstrainedversionissupe-
rioracrossallflopregimes. Weusethisversionin§5,and
furtherlimitdepthto12≤d≤28(seealsoAppendixD).
Alternate design choices. Modern mobile networks often
employ the inverted bottleneck (b < 1) proposed in [25]
alongwithdepthwiseconv[1](g = 1). InFigure14(left),
we observe that the inverted bottleneck degrades the EDF
slightlyanddepthwiseconvperformsevenworserelativeto
b = 1andg ≥ 1(seeappendixforfurtheranalysis). Next,
motivated by [29] who found that scaling the input image
resolutioncanbehelpful,wetestvaryingresolutioninFig-
ure14(middle).Contraryto[29],wefindthatforRegNetX
afixedresolutionof224×224isbest,evenathigherflops.
SE. Finally, we evaluate RegNetX with the popular
Squeeze-and-Excitation (SE) op [10] (we abbreviate X+SE
asYandrefertotheresultingdesignspaceasRegNetY).In
Figure14(right),weseethatRegNetYyieldsgoodgains.
7

1024 RegNetX-200MF 1024 RegNetX-400MF 1024 RegNetX-600MF 1024 RegNetX-800MF 1024 RegNetY-200MF 1024 RegNetY-400MF 1024 RegNetY-600MF 1024 RegNetY-800MF
| 512       | 512 |     | 512 |     | 512 | 512       |     | 512 |     | 512 |     | 512 |     |
| --------- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
| 256       | 256 |     | 256 |     | 256 | 256       |     | 256 |     | 256 |     | 256 |     |
| htdiw 128 | 128 |     | 128 |     | 128 | htdiw 128 |     | 128 |     | 128 |     | 128 |     |
d i = [ 1 , 1 , 4 , 7 ] d i = [ 1 , 2 , 7 , 1 2 ] d i = [ 1 , 3 , 5 , 7 ] d i = [ 1 , 3 , 7 , 5 ] d i = [ 1 , 1 , 4 , 7 ] d i = [ 1 , 3 , 6 , 6 ] d i = [ 1 , 3 , 7 , 4 ] d i = [ 1 , 3 , 8 , 2 ]
64 w i = [ 2 4 , 5 6 , 1 5 2 , 3 6 8 ] 6 4 w i = [ 3 2 , 6 4 , 1 6 0 , 3 8 4 ] 6 4 w i = [ 4 8 , 9 6 , 2 4 0 , 5 2 8 ] 6 4 w i = [ 6 4 , 1 2 8 , 2 8 8 , 6 7 2 ] 64 w i = [ 2 4 , 5 6 , 1 5 2 , 3 6 8 ] 6 4 w i = [ 4 8 , 1 0 4 , 2 0 8 , 4 4 0 ] 6 4 w i = [ 4 8 , 1 1 2 , 2 5 6 , 6 0 8 ] 6 4 w i = [ 6 4 , 1 2 8 , 3 2 0 , 7 6 8 ]
32 g w = = 8 , 3   b 6 , =   w 1 , =   e 2 = 4 3 ,  0 w . 8 % =2.5 3 2 g w = = 1 6 2 , 4   b ,   w = 1 = ,   e 2 4 = ,  2 w 7 .2 = % 2.5 3 2 g w = = 2 4 3 , 7   b ,   w = 1 = ,   e 4 8 = ,  2 w 5 .5 = % 2.2 3 2 g w = = 1 6 3 , 6   b ,   w = 1 = ,   e 5 6 = ,  2 w 4 .8 = % 2.3 32 g w = = 8 , 3   b 6 , =   w 1 , =   e 2 = 4 2 ,  9 w . 5 % =2.5 3 2 g w = = 8 , 2   b 8 , =   w 1 , =  e 4 = 8 2 ,  5 w . 8 % = 2.1 3 2 g w = = 1 6 3 , 3   b ,   w = 1 = ,   e 4 8 = ,  2 w 4 .4 = % 2.3 3 2 g w = = 1 6 3 , 9   b ,   w = 1 = ,   e 5 6 = ,  2 w 3 .5 = % 2.4
160 a 0 m 160 a 0 m 160 a 0 m 160 a 0 m 160 a 0 m 160 a 0 m 160 a 0 m 160 a 0 m
2 4 6 8 10 12 3 6 9 12 15 18 21 2 4 6 8 10 12 14 2 4 6 8 10 12 14 2 4 6 8 10 12 2 4 6 8 10 12 14 2 4 6 8 10 12 14 2 4 6 8 10 12
2048 RegNetX-1.6GF 2048 RegNetX-3.2GF 2048 RegNetX-4.0GF 2048 RegNetX-6.4GF 2048 RegNetY-1.6GF 2048 RegNetY-3.2GF 2048 RegNetY-4.0GF 2048 RegNetY-6.4GF
| 1024  | 1024 |     | 1024 |     | 1024 | 1024  |     | 1024 |     | 1024 |     | 1024 |     |
| ----- | ---- | --- | ---- | --- | ---- | ----- | --- | ---- | --- | ---- | --- | ---- | --- |
| 512   | 512  |     | 512  |     | 512  | 512   |     | 512  |     | 512  |     | 512  |     |
| htdiw |      |     |      |     |      | htdiw |     |      |     |      |     |      |     |
| 256   | 256  |     | 256  |     | 256  | 256   |     | 256  |     | 256  |     | 256  |     |
128 d w i i = = [ [ 2 7 , 2 4 , , 1 1 6 0 8 , , 2 4 ] 0 8 , 9 1 2 ] 1 2 8 d w i i = = [ [ 2 9 , 6 6 , , 1 1 9 5 2 , , 2 4 ] 3 2 , 1 0 0 8 ] 1 2 8 d w i i = = [ [ 2 8 , 0 5 , , 2 1 4 4 0 , , 2 5 ] 6 0 , 1 3 6 0 ] 1 2 8 d w i i = = [ [ 2 1 , 6 4 8 , , 1 3 0 9 , 2 1 , ] 7 8 4 , 1 6 2 4 ] 128 d w i i = = [ [ 2 4 , 8 6 , , 1 1 2 7 0 , , 2 3 ] 3 6 , 8 8 8 ] 1 2 8 d w i i = = [ [ 2 7 , 2 5 , , 2 1 1 3 6 , , 1 5 ] 7 6 , 1 5 1 2 ] 1 2 8 d w i i = = [ [ 2 1 , 2 6 8 , , 1 1 2 9 , 2 2 , ] 5 1 2 , 1 0 8 8 ] 1 2 8 d w i i = = [ [ 2 1 , 4 7 4 , , 1 2 4 8 , 8 2 , ] 5 7 6 , 1 2 9 6 ]
64 g = 2 4 ,   b = 1 ,   e = 2 2 .9 % 6 4 g = 4 8 ,   b = 1 ,   e = 2 1 .6 % 6 4 g = 4 0 ,   b = 1 ,   e = 2 1 .3 % 6 4 g = 5 6 ,   b = 1 ,  e = 2 0 . 7 % 64 g = 2 4 ,   b = 1 ,   e = 2 2 .0 % 6 4 g = 2 4 ,   b = 1 ,   e = 2 0 .7 % 6 4 g = 6 4 ,   b = 1 ,  e = 2 0 .5 % 6 4 g = 7 2 ,   b = 1 ,  e = 1 9 . 9 %
w a = 3 4 ,   w 0 = 8 0 ,  w m = 2.2 w a = 2 6 ,   w 0 = 8 8 ,  w m = 2 .2 w a = 3 9 ,   w 0 = 9 6 ,  w m = 2 .4 w a = 6 1 ,   w 0 = 1 8 4 ,  w m = 2 .1 w a = 2 1 ,   w 0 = 4 8 ,  w m = 2.6 w a = 4 3 ,   w 0 = 8 0 ,  w m = 2 .7 w a = 3 1 ,   w 0 = 9 6 ,  w m = 2 . 2 w a = 3 3 ,   w 0 = 1 1 2 ,  w m = 2 .3
320 2 4 6 8 10121416 320 3 6 9 1215182124 320 3 6 9 12 15 18 21 320 2 4 6 8 10121416 320 3 6 91215182124 320 3 6 9 12 15 18 320 3 6 9 12 15 18 21 320 3 6 9 1215182124
| 4096 | 4096 |     | 4096 |     | 4096 | 4096 |     | 4096 |     | 4096 |     | 4096 |     |
| ---- | ---- | --- | ---- | --- | ---- | ---- | --- | ---- | --- | ---- | --- | ---- | --- |
2048 RegNetX-8.0GF 2048 RegNetX-12GF 2048 RegNetX-16GF 2048 RegNetX-32GF 2048 RegNetY-8.0GF 2048 RegNetY-12GF 2048 RegNetY-16GF 2048 RegNetY-32GF
| htdiw 1024 | 1024 |     | 1024 |     | 1024 | htdiw 1024 |     | 1024 |     | 1024 |     | 1024 |     |
| ---------- | ---- | --- | ---- | --- | ---- | ---------- | --- | ---- | --- | ---- | --- | ---- | --- |
| 512        | 512  |     | 512  |     | 512  | 512        |     | 512  |     | 512  |     | 512  |     |
256 d i = [ 2 , 5 , 1 5 , 1 ] 2 5 6 d i = [ 2 , 5 , 1 1 , 1 ] 2 5 6 d i = [ 2 , 6 , 1 3 , 1 ] 2 5 6 d i = [ 2 , 7 , 1 3 , 1 ] 256 d i = [ 2 , 4 , 1 0 , 1 ] 2 5 6 d i = [ 2 , 5 , 1 1 , 1 ] 2 5 6 d i = [ 2 , 4 , 1 1 , 1 ] 2 5 6 d i = [ 2 , 5 , 1 2 , 1 ]
w g i = = 1 [ 2 8 0 0 , ,   b 2 4 = 0 1 , 7 ,   2 e 0 = , 1 2 9 0 2 .5 0 % ] w g i = = 1 [ 1 2 2 2 , 4   b , 4 = 4 1 8 , ,   8 e 9 = 6 2 , 2 0 2 .3 4 % 0 ] w g i = = 1 [ 2 2 8 5 , 6   b , 5 = 1 1 2 , ,   8 e 9 = 6 2 , 2 0 0 .0 4 % 8 ] w g i = = 1 [ 6 3 8 3 , 6   b , 6 = 7 1 2 , ,   1 e 3 = 4 1 4 9 , 2 .5 5 % 2 0 ] w g i = = 5 [ 6 1 , 6   b 8 , = 4 1 4 , 8  e , 8 = 9 1 6 9 , 2 . 9 0 % 1 6 ] w g i = = 1 [ 1 2 2 2 , 4   b , 4 = 4 1 8 , ,   8 e 9 = 6 1 , 2 9 2 .5 4 % 0 ] w g i = = 1 [ 1 2 2 2 , 4   b , 4 = 4 1 8 , ,   1 e 2 = 3 1 2 9 , 3 . 5 0 % 2 4 ] w g i = = 2 [ 3 2 2 3 , 2   b , 6 = 9 1 6 , ,   1 e 3 = 9 1 2 9 , 3 . 0 7 % 1 2 ]
128 w a = 5 0 ,   w 0 = 8 0 ,   w m = 2 .9 1 2 8 w a = 7 3 ,   w 0 = 1 6 8 ,  w m = 2 .4 1 2 8 w a = 5 6 ,   w 0 = 2 1 6 ,  w m = 2 .1 1 2 8 w a = 7 0 ,   w 0 = 3 2 0 ,  w m = 2 . 0 128 w a = 7 7 ,   w 0 = 1 9 2 ,  w m = 2 .2 1 2 8 w a = 7 3 ,   w 0 = 1 6 8 ,  w m = 2 .4 1 2 8 w a = 1 0 6 ,   w 0 = 2 0 0 ,  w m = 2 .5 1 2 8 w a = 1 1 6 ,   w 0 = 2 3 2 ,  w m = 2 .5
640 3 6 9 12 15 18 21 640 2 4 6 81012141618 640 3 6 9 12 15 18 21 640 3 6 9 12 15 18 21 640 2 4 6 8 10121416 640 2 4 6 81012141618 640 2 4 6 8 10121416 640 2 4 6 81012141618
block index block index block index block index block index block index block index block index
flops params acts batch infer train error flops params acts batch infer train error
|     |     |         |      |      |              |     |     | (B) | (M) (M) | size | (ms) | (hr) | (top-1) |
| --- | --- | ------- | ---- | ---- | ------------ | --- | --- | --- | ------- | ---- | ---- | ---- | ------- |
|     | (B) | (M) (M) | size | (ms) | (hr) (top-1) |     |     |     |         |      |      |      |         |
REGNETX-200MF 0.2 2.7 2.2 1024 10 2.8 31.1±0.09 REGNETY-200MF 0.2 3.2 2.2 1024 11 3.1 29.6±0.11
REGNETX-400MF 0.4 5.2 3.1 1024 15 3.9 27.3±0.15 REGNETY-400MF 0.4 4.3 3.9 1024 19 5.1 25.9±0.16
REGNETX-600MF 0.6 6.2 4.0 1024 17 4.4 25.9±0.03 REGNETY-600MF 0.6 6.1 4.3 1024 19 5.2 24.5±0.07
REGNETX-800MF 0.8 7.3 5.1 1024 21 5.7 24.8±0.09 REGNETY-800MF 0.8 6.3 5.2 1024 22 6.0 23.7±0.03
REGNETX-1.6GF 1.6 9.2 7.9 1024 33 8.7 23.0±0.13 REGNETY-1.6GF 1.6 11.2 8.0 1024 39 10.1 22.0±0.08
REGNETX-3.2GF 3.2 15.3 11.4 512 57 14.3 21.7±0.08 REGNETY-3.2GF 3.2 19.4 11.3 512 67 16.5 21.0±0.05
REGNETX-4.0GF 4.0 22.1 12.2 512 69 17.1 21.4±0.19 REGNETY-4.0GF 4.0 20.6 12.3 512 68 16.8 20.6±0.08
REGNETX-6.4GF 6.5 26.2 16.4 512 92 23.5 20.8±0.07 REGNETY-6.4GF 6.4 30.6 16.4 512 104 26.1 20.1±0.04
REGNETX-8.0GF 8.0 39.6 14.1 512 94 22.6 20.7±0.07 REGNETY-8.0GF 8.0 39.2 18.0 512 113 28.1 20.1±0.09
REGNETX-12GF 12.1 46.1 21.4 512 137 32.9 20.3±0.04 REGNETY-12GF 12.1 51.8 21.4 512 150 36.0 19.7±0.06
REGNETX-16GF 15.9 54.3 25.5 512 168 39.7 20.0±0.11 REGNETY-16GF 15.9 83.6 23.0 512 189 45.6 19.6±0.16
REGNETX-32GF 31.7 107.8 36.3 256 318 76.9 19.5±0.12 REGNETY-32GF 32.3 145.0 30.3 256 319 76.0 19.0±0.12
Figure15.Top REGNETX models. Wemeasureinferencetime Figure16.Top REGNETY models(Y=X+SE).Thebenchmark-
for 64 images on an NVIDIA V100 GPU; train time is for 100 ingsetupandthefigureformatisthesameasinFigure15.
| epochs on | 8 GPUs with | the batch | size listed. |     | Network diagram |     |     |     |     |     |     |     |     |
| --------- | ----------- | --------- | ------------ | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
legendscontainallinformationrequiredtoimplementthemodels. 5.1.State-of-the-ArtComparison: MobileRegime
5.ComparisontoExistingNetworks
Muchoftherecentworkonnetworkdesignhasfocused
|     |     |     |     |     |     | on the mobile | regime | (∼600MF). |     | In  | Table | 2, we compare |     |
| --- | --- | --- | --- | --- | --- | ------------- | ------ | --------- | --- | --- | ----- | ------------- | --- |
We now compare top models from the RegNetX and models at 600MF to existing mobile networks.
REGNET
RegNetYdesignspacesatvariouscomplexitiestothestate-
|            |             |         |        |            |        | Weobservethat |     | REGNETS | aresurprisinglyeffectiveinthis |     |     |     |     |
| ---------- | ----------- | ------- | ------ | ---------- | ------ | ------------- | --- | ------- | ------------------------------ | --- | --- | --- | --- |
| of-the-art | on ImageNet | [3]. We | denote | individual | models |               |     |         |                                |     |     |     |     |
regimeconsideringthesubstantialbodyofworkonfinding
usingsmallcaps,e.g.REGNETX.Wealsosuffixthemodels
|     |     |     |     |     |     | better mobile | networks |     | via both | manual | design | [9, | 25, 19] |
| --- | --- | --- | --- | --- | --- | ------------- | -------- | --- | -------- | ------ | ------ | --- | ------- |
withtheflopregime,e.g.400MF.Foreachflopregime,we
|     |     |     |     |     |     | andNAS | [35,23,17,18]. |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------ | -------------- | --- | --- | --- | --- | --- | --- |
pickthebestmodelfrom25randomsettingsoftheRegNet
|                  |     |                              |     |     |     | We emphasize |     | that | REGNET | models | use | our basic | 100 |
| ---------------- | --- | ---------------------------- | --- | --- | --- | ------------ | --- | ---- | ------ | ------ | --- | --------- | --- |
| parameters(d,g,w | ,w  | ,w ),andre-trainthetopmodel5 |     |     |     |              |     |      |        |        |     |           |     |
m a 0 epoch schedule with no regularization except weight de-
timesat100epochstoobtainrobusterrorestimates.
|              |         |     |         |     |               | cay, while | most | mobile | networks |     | use longer | schedules |     |
| ------------ | ------- | --- | ------- | --- | ------------- | ---------- | ---- | ------ | -------- | --- | ---------- | --------- | --- |
| Resultingtop | REGNETX | and | REGNETY |     | modelsforeach |            |      |        |          |     |            |           |     |
withvariousenhancements,suchasdeepsupervision[16],
| flop regime | are shown | in Figures | 15  | and 16, | respectively. |     |     |     |     |     |     |     |     |
| ----------- | --------- | ---------- | --- | ------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Cutout[4],DropPath[14],AutoAugment[2],andsoon.As
Inadditiontothesimplelinearstructureandthetrendswe
such,wehopeourstrongresultsobtainedwithashorttrain-
| analyzedin§4,weobserveaninterestingpattern. |     |     |     |     | Namely, |              |         |              |     |     |           |      |        |
| ------------------------------------------- | --- | --- | --- | --- | ------- | ------------ | ------- | ------------ | --- | --- | --------- | ---- | ------ |
|                                             |     |     |     |     |         | ing schedule | without | enhancements |     |     | can serve | as a | simple |
thehigherflopmodelshavealargenumberofblocksinthe
baselineforfuturework.
| third stage | and a small | number | of blocks | in  | the last stage. |     |     |     |     |     |     |     |     |
| ----------- | ----------- | ------ | --------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
This is similar to the design of standard RESNET models. flops(B) params(M) top-1error
|     |     |     |     |     |     | MOBILENET[9] |     |     | 0.57 |     | 4.2 | 29.4 |     |
| --- | --- | --- | --- | --- | --- | ------------ | --- | --- | ---- | --- | --- | ---- | --- |
Moreover,weobservethatthegroupwidthgincreaseswith
|     |     |     |     |     |     | MOBILENET-V2[25] |     |     | 0.59 |     | 6.9 | 25.3 |     |
| --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | ---- | --- | --- | ---- | --- |
complexity,butdepthdsaturatesforlargemodels.
|     |     |     |     |     |     | SHUFFLENET[33] |     |     | 0.52 |     | -   | 26.3 |     |
| --- | --- | --- | --- | --- | --- | -------------- | --- | --- | ---- | --- | --- | ---- | --- |
Ourgoalistoperformfaircomparisonsandprovidesim- SHUFFLENET-V2[19] 0.59 - 25.1
|             |                   |            |     |              |                 | NASNET-A[35]    |     |     | 0.56 |     | 5.3 | 26.0 |     |
| ----------- | ----------------- | ---------- | --- | ------------ | --------------- | --------------- | --- | --- | ---- | --- | --- | ---- | --- |
| ple and     | easy-to-reproduce | baselines. |     | We           | note that along |                 |     |     |      |     |     |      |     |
|             |                   |            |     |              |                 | AMOEBANET-C[23] |     |     | 0.57 |     | 6.4 | 24.3 |     |
| with better | architectures,    | much       | of  | the recently | reported        |                 |     |     |      |     |     |      |     |
|             |                   |            |     |              |                 | PNASNET-5[17]   |     |     | 0.59 |     | 5.1 | 25.8 |     |
gainsinnetworkperformancearebasedonenhancementsto DARTS[18] 0.57 4.7 26.7
thetrainingsetupandregularizationscheme(seeTable7). REGNETX-600MF 0.60 6.2 25.9±0.03
|     |     |     |     |     |     | REGNETY-600MF |     |     | 0.60 |     | 6.1 | 24.5±0.07 |     |
| --- | --- | --- | --- | --- | --- | ------------- | --- | --- | ---- | --- | --- | --------- | --- |
Asourfocusisonevaluatingnetworkarchitectures,weper-
Table2.Mobileregime.Wecompareexistingmodelsusingorig-
formcarefullycontrolledexperimentsunderthesametrain-
inallyreportederrorstoRegNetmodelstrainedinabasicsetup.
| ingsetup. | Inparticular,toprovidefaircomparisonstoclas- |     |     |     |     |            |        |        |         |              |     |      |         |
| --------- | -------------------------------------------- | --- | --- | --- | --- | ---------- | ------ | ------ | ------- | ------------ | --- | ---- | ------- |
|           |                                              |     |     |     |     | Our simple | RegNet | models | achieve | surprisingly |     | good | results |
sicwork,wedonotuseanytraining-timeenhancements.
giventheeffortfocusedonthisregimeinthepastfewyears.
8

| 25        |     |     | ResNet  |     | ResNet  |          | EfficientNet |     | EfficientNet | EfficientNet |
| --------- | --- | --- | ------- | --- | ------- | -------- | ------------ | --- | ------------ | ------------ |
| 24        |     |     | ResNeXt |     | ResNeXt | 26       | RegNetX      |     | RegNetX      | RegNetX      |
|           |     |     | RegNetX |     | RegNetX |          | RegNetY      |     | RegNetY      | RegNetY      |
| rorre 23  |     |     |         |     |         | rorre 24 |              |     |              |              |
| 22 ResNet |     |     |         |     |         | 22       |              |     |              |              |
ResNeXt
| 21 RegNetX |     |     |     |     |     | 20  |     |     |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.8 1.6 3.2 6.4 12.8 8 16 32 64 8 16 32 0.4 0.8 1.6 3.2 6.4 12.8 4 8 16 32 64 4 8 16 32 64 128
flops (B) params (M) activations (M) flops (B) params (M) activations (M)
Figure 17. ResNe(X)t comparisons. REGNETX models versus Figure18.EFFICIENTNETcomparisons. REGNETsoutperform
RESNE(X)T-(50,101,152)undervariouscomplexitymetrics.As thestateoftheart,especiallywhenconsideringactivations.
allmodelsusetheidenticalcomponentsandtrainingsettings,all
|     |     |     |     |     |     |     | flops | params | acts batch infer | train top-1error |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------ | ---------------- | ---------------- |
observedgainsarefromthedesignoftheRegNetXdesignspace. (B) (M) (M) size (ms) (hr) ours±std [orig]
|     |     |     |     |     |     | EFFICIENTNET-B0 |     | 0.4 5.3 | 6.7 256 34 | 11.7 24.9±0.03[23.7] |
| --- | --- | --- | --- | --- | --- | --------------- | --- | ------- | ---------- | -------------------- |
flops params acts infer train top-1error REGNETY-400MF 0.4 4.3 3.9 1024 19 5.1 25.9±0.16
|     |     |     |          |      |                 | EFFICIENTNET-B1 |     | 0.7 7.8 | 10.9 256 52 | 15.6 24.1±0.16[21.2] |
| --- | --- | --- | -------- | ---- | --------------- | --------------- | --- | ------- | ----------- | -------------------- |
|     | (B) | (M) | (M) (ms) | (hr) | ours±std [orig] |                 |     |         |             |                      |
RESNET-50 4.1 22.6 11.1 53 12.2 23.2±0.09[23.9] REGNETY-600MF 0.6 6.1 4.3 1024 19 5.2 24.5±0.07
|               |     |      |         |      |           | EFFICIENTNET-B2 |     | 1.0 9.2 | 13.8 256 68 | 18.4 23.4±0.06[20.2] |
| ------------- | --- | ---- | ------- | ---- | --------- | --------------- | --- | ------- | ----------- | -------------------- |
| REGNETX-3.2GF | 3.2 | 15.3 | 11.4 57 | 14.3 | 21.7±0.08 |                 |     |         |             |                      |
RESNEXT-50 4.2 25.0 14.4 78 18.0 21.9±0.10[22.2] REGNETY-800MF 0.8 6.3 5.2 1024 22 6.0 23.7±0.03
RESNET-101 7.8 44.6 16.2 90 20.4 21.4±0.11[22.0] EFFICIENTNET-B3 1.8 12.0 23.8 256 114 32.1 22.5±0.05[18.9]
REGNETX-6.4GF 6.5 26.2 16.4 92 23.5 20.8±0.07 REGNETY-1.6GF 1.6 11.2 8.0 1024 39 10.1 22.0±0.08
RESNEXT-101 8.0 44.2 21.2 137 31.8 20.7±0.08[21.2] EFFICIENTNET-B4 4.2 19.0 48.5 128 240 65.1 21.2±0.06[17.4]
RESNET-152 11.5 60.2 22.6 130 29.2 20.9±0.12[21.6] REGNETY-4.0GF 4.0 20.6 12.3 512 68 16.8 20.6±0.08
REGNETX-12GF 12.1 46.1 21.4 137 32.9 20.3±0.04 EFFICIENTNET-B5 9.9 30.0 98.9 64 504 135.1 21.5±0.11[16.7]
(a)Comparisonsgroupedbyactivations. REGNETY-8.0GF 8.0 39.2 18.0 512 113 28.1 20.1±0.09
RESNET-50 4.1 22.6 11.1 53 12.2 23.2±0.09[23.9] Table4. EFFICIENTNET comparisonsusingourstandardtrain-
| RESNEXT-50    | 4.2 | 25.0 | 14.4 78 | 18.0 | 21.9±0.10[22.2] |               |       |            |                    |         |
| ------------- | --- | ---- | ------- | ---- | --------------- | ------------- | ----- | ---------- | ------------------ | ------- |
|               |     |      |         |      |                 | ing schedule. | Under | comparable | training settings, | REGNETY |
| REGNETX-4.0GF | 4.0 | 22.1 | 12.2 69 | 17.1 | 21.4±0.19       |               |       |            |                    |         |
RESNET-101 7.8 44.6 16.2 90 20.4 21.4±0.11[22.0] outperforms EFFICIENTNET for most flop regimes. Moreover,
RESNEXT-101 8.0 44.2 21.2 137 31.8 20.7±0.08[21.2] REGNETmodelsareconsiderablyfaster,e.g.,REGNETX-F8000
| REGNETX-8.0GF | 8.0 | 39.6 | 14.1 94 | 22.6 | 20.7±0.07 |     |     |     |     |     |
| ------------- | --- | ---- | ------- | ---- | --------- | --- | --- | --- | --- | --- |
RESNET-152 11.5 60.2 22.6 130 29.2 20.9±0.12[21.6] isabout5×fasterthan EFFICIENTNET-B5. Notethatoriginally
| RESNEXT-152 | 11.7 | 60.0 | 29.7 197 | 45.7 | 20.4±0.06[21.1] |     |     |     |     |     |
| ----------- | ---- | ---- | -------- | ---- | --------------- | --- | --- | --- | --- | --- |
reportederrorsforEFFICIENTNET(showngrayedout),aremuch
| REGNETX-12GF | 12.1 | 46.1 | 21.4 137 | 32.9 | 20.3±0.04 |     |     |     |     |     |
| ------------ | ---- | ---- | -------- | ---- | --------- | --- | --- | --- | --- | --- |
(b)Comparisonsgroupedbyflops. lowerbutuselongerandenhancedtrainingschedules,seeTable7.
| Table3.RESNE(X)Tcomparisons. |     |     | (a)Groupedbyactivations, |     |     |                                 |     |     |            |     |
| ---------------------------- | --- | --- | ------------------------ | --- | --- | ------------------------------- | --- | --- | ---------- | --- |
|                              |     |     |                          |     |     | 5.3.State-of-the-ArtComparison: |     |     | FullRegime |     |
REGNETXshowconsiderablegains(notethatforeachgroupGPU
| inferenceandtrainingtimesaresimilar). |     |     |     | (b) REGNETX | models |                        |     |     |              |            |
| ------------------------------------- | --- | --- | --- | ----------- | ------ | ---------------------- | --- | --- | ------------ | ---------- |
|                                       |     |     |     |             |        | Wefocusourcomparisonon |     |     | EFFICIENTNET | [29],which |
outperformRESNE(X)Tmodelsunderfixedflopsaswell.
isrepresentativeofthestateoftheartandhasreportedim-
pressivegainsusingacombinationofNASandaninterest-
| 5.2.StandardBaselinesComparison: |     |     |     | ResNe(X)t |     |     |     |     |     |     |
| -------------------------------- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
ingmodelscalingruleacrosscomplexityregimes.
Next,wecompareREGNETXtostandardRESNET[8]and
|     |     |     |     |     |     | To enable | direct | comparisons, | and to isolate | gains due |
| --- | --- | --- | --- | --- | --- | --------- | ------ | ------------ | -------------- | --------- |
RESNEXT[31]models.Allofthemodelsinthisexperiment toimprovementssolelyofthenetworkarchitecture,weopt
come from the exact same design space, the former being toreproducetheexact modelsbutusingour
EFFICIENTNET
manuallydesigned,thelatterbeingobtainedthroughdesign standard training setup, with a 100 epoch schedule and no
space design. For fair comparisons, we compare REGNET regularizationexceptweightdecay(effectoflongersched-
| and | modelsunderthesametrainingsetup(our |     |     |     |     |     |     |     |     |     |
| --- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
RESNE(X)T ule and stronger regularization are shown in Table 7). We
standard REGNET training setup). We note thatthis results optimizeonlylrandwd,seeFigure22inappendix. Thisis
inimprovedRESNE(X)Tbaselinesandhighlightstheimpor- thesamesetupasREGNETandenablesfaircomparisons.
tanceofcarefullycontrollingthetrainingsetup. ResultsareshowninFigure18andTable4.Atlowflops,
ComparisonsareshowninFigure17andTable3. Over- outperforms the REGNETY. At intermediate
EFFICIENTNET
| all, we see | that | models, | by  | optimizing | the net- |     |     |     |     |     |
| ----------- | ---- | ------- | --- | ---------- | -------- | --- | --- | --- | --- | --- |
REGNETX flops, REGNETY outperforms EFFICIENTNET, and at higher
work structure alone, provide considerable improvements flopsbothREGNETXandREGNETYperformbetter.
underallcomplexitymetrics.WeemphasizethatgoodREG-
WealsoobservethatforEFFICIENTNET,activationsscale
NET models are available across a wide range of compute linearlywithflops(duetothescalingofbothresolutionand
regimes, including in low-compute regimes where good depth),comparedtoactivationsscalingwiththesquare-root
RESNE(X)Tmodelsarenotavailable.
|     |     |     |     |     |     | offlopsforREGNETs. |     | ThisleadstoslowGPUtrainingand |     |     |
| --- | --- | --- | --- | --- | --- | ------------------ | --- | ----------------------------- | --- | --- |
Table 3a shows comparisons grouped by activations inferencetimesfor EFFICIENTNET. E.g., REGNETX-8000 is
(whichcanstronglyinfluenceruntimeonacceleratorssuch
5×fasterthanEFFICIENTNET-B5,whilehavinglowererror.
| as GPUs).        | This setting | is of | particular | interest | to the re-   |     |     |     |     |     |
| ---------------- | ------------ | ----- | ---------- | -------- | ------------ | --- | --- | --- | --- | --- |
| search community | where        | model | training   | time     | is a bottle- |     |     |     |     |     |
6.Conclusion
| neck and | will likely have | more | real-world | use | cases in the |     |     |     |     |     |
| -------- | ---------------- | ---- | ---------- | --- | ------------ | --- | --- | --- | --- | --- |
future,especiallyasacceleratorsgainmoreuseatinference Inthiswork,wepresentanewnetworkdesignparadigm.
time(e.g.,inself-drivingcars). REGNETXmodelsarequite Ourresultssuggestthatdesigningnetworkdesignspacesis
effectivegivenafixedinferenceortrainingtimebudget. apromisingavenueforfutureresearch.
9

flops params acts infer train error 30 12 d 28 .borp evitalumuc 1.0 .borp evitalumuc 1.0
|               | (B) | (M) (M) (ms) | (hr) (top-1)   | 28       | d=20 |     |     |     |     |
| ------------- | --- | ------------ | -------------- | -------- | ---- | --- | --- | --- | --- |
|               |     |              |                |          |      | 0.8 |     | 0.8 |     |
| RESNET-50     | 4.1 | 22.6 11.1 53 | 12.2 35.0±0.20 | rorre 26 |      | 0.6 |     | 0.6 |     |
| REGNETX-3.2GF | 3.2 | 15.3 11.4 57 | 14.3 33.6±0.25 |          |      |     |     |     |     |
|               |     |              |                | 24       |      | 0.4 |     | 0.4 |     |
RESNEXT-50 4.2 25.0 14.4 78 18.0 33.5±0.10 [21.0|21.7] 3 stage0.2 [21.0|21.2] b=1/2
|     |     |     |     | 22  |     | 0.2 |     |     | [20.7|21.0] b=1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- |
RESNET-101 7.8 44.6 16.2 90 20.4 33.2±0.24 20 [20.7|21.0] 4 stage
REGNETX-6.4GF 6.5 26.2 16.4 92 23.5 32.6±0.15 0.2 0.4 0 .8 1 .6 3.2 6.4 0.0 21.0 21.5 22.0 22.5 23.0 23.5 0.0 20.8 21.0 21.2 21.4 21.6
|             |      |               |                |        | f lo ps ( B )  |            | error |       | error          |
| ----------- | ---- | ------------- | -------------- | ------ | -------------- | ---------- | ----- | ----- | -------------- |
| RESNEXT-101 | 8.0  | 44.2 21.2 137 | 31.8 32.1±0.30 |        |                |            |       | Left: |                |
|             |      |               |                | Figure | 19. Additional | ablations. |       | Fixed | depth networks |
| RESNET-152  | 11.5 | 60.2 22.6 130 | 29.2 32.2±0.22 |        |                |            |       |       |                |
REGNETX-12GF 12.1 46.1 21.4 137 32.9 32.0±0.27 (d = 20)areeffectiveacrossflopregimes. Middle: Threestage
(a)Comparisonsgroupedbyactivations. networksperformpoorlyathighflops. Right:Invertedbottleneck
RESNET-50 4.1 22.6 11.1 53 12.2 35.0±0.20 (b<1)isalsoineffectiveathighflops.Seetextformorecontext.
| RESNEXT-50    | 4.2 | 25.0 14.4 78 | 18.0 33.5±0.10 |     |     |     |     |     |     |
| ------------- | --- | ------------ | -------------- | --- | --- | --- | --- | --- | --- |
| REGNETX-4.0GF | 4.0 | 22.1 12.2 69 | 17.1 33.2±0.20 |     |     |     |     |     |     |
RESNET-101 7.8 44.6 16.2 90 20.4 33.2±0.24 .borp evitalumuc 1.0 36 ReLU g 134 36 ReLU g=1
|             |     |               |                |     |     | 34  |     | Swish g 1 | Swish g=1 |
| ----------- | --- | ------------- | -------------- | --- | --- | --- | --- | --------- | --------- |
| RESNEXT-101 | 8.0 | 44.2 21.2 137 | 31.8 32.1±0.30 | 0.8 |     | 32  |     | 32        |           |
REGNETX-8.0GF 8.0 39.6 14.1 94 22.6 32.5±0.18 0.6 rorre 30 rorre 30
[29.8|31.3] 400MF ReLU
| RESNET-152 | 11.5 | 60.2 22.6 130 | 29.2 32.2±0.22 | 0.4 |                                      | 28        |     | 28  |     |
| ---------- | ---- | ------------- | -------------- | --- | ------------------------------------ | --------- | --- | --- | --- |
|            |      |               |                |     | [ 2 8 . 7 | 3 0 . 4 ]   4 0 0 M F  S | w i sh 26 |     | 26  |     |
RESNEXT-152 11.7 60.0 29.7 197 45.7 31.5±0.26 0.2 [ 2 2 . 1 | 2 2 . 7 ]   6 .4 G F  R e L U 24 24
| REGNETX-12GF | 12.1 | 46.1 21.4 137 | 32.9 32.0±0.27 |     | [22.6|23.0] 6.4GF Swish |     |             |                    |                     |
| ------------ | ---- | ------------- | -------------- | --- | ----------------------- | --- | ----------- | ------------------ | ------------------- |
|              |      |               |                | 0.0 |                         | 22  | 0.2 0.4 0.8 | 1.6 3.2 6.4 22 0.2 | 0.4 0.8 1.6 3.2 6.4 |
(b)Comparisonsgroupedbyflops. 22 24 26 error 28 30 32 34 flops (B) flops (B)
Table5.RESNE(X)TcomparisonsonImageNetV2. Figure20.Swishvs.ReLU.Left:RegNetYperformsbetterwith
|     |     |     |     | SwishthanReLUat400MFbutworseat6.4GF.Middle: |     |     |     |     | Results |
| --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | ------- |
flops params acts batch infer train error acrosswiderflopregimesshowsimilartrends.Right:If,however,
(B) (M) (M) size (ms) (hr) (top-1) gisrestrictedtobe1(depthwiseconv),Swishismuchbetter.
| EFFICIENTNET-B0 | 0.4 5.3 | 6.7 256  | 34 11.7 37.1±0.22 |     |     |     |     |     |     |
| --------------- | ------- | -------- | ----------------- | --- | --- | --- | --- | --- | --- |
| REGNETY-400MF   | 0.4 4.3 | 3.9 1024 | 19 5.1 38.3±0.26  |     |     |     |     |     |     |
EFFICIENTNET-B1 0.7 7.8 10.9 256 52 15.6 36.4±0.10 AppendixB:AdditionalAblations
| REGNETY-600MF   | 0.6 6.1 | 4.3 1024 | 19 5.2 36.9±0.17  |     |     |     |     |     |     |
| --------------- | ------- | -------- | ----------------- | --- | --- | --- | --- | --- | --- |
| EFFICIENTNET-B2 | 1.0 9.2 | 13.8 256 | 68 18.4 35.3±0.25 |     |     |     |     |     |     |
Inthissectionweperformadditionalablationstofurther
| REGNETY-800MF | 0.8 6.3 | 5.2 1024 | 22 6.0 35.7±0.40 |     |     |     |     |     |     |
| ------------- | ------- | -------- | ---------------- | --- | --- | --- | --- | --- | --- |
EFFICIENTNET-B3 1.8 12.0 23.8 256 114 32.1 34.4±0.27 supportorsupplementtheresultsofthemaintext.
| REGNETY-1.6GF | 1.6 11.2 | 8.0 1024 | 39 10.1 33.9±0.19 |     |     |     |     |     |     |
| ------------- | -------- | -------- | ----------------- | --- | --- | --- | --- | --- | --- |
EFFICIENTNET-B4 4.2 19.0 48.5 128 240 65.1 32.5±0.23 Fixeddepth. In§5weobservedthatthedepthsofourtop
REGNETY-4.0GF 4.0 20.6 12.3 512 68 16.8 32.3±0.28 modelsarefairlystable(∼20blocks). InFigure19(left)we
| EFFICIENTNET-B5 | 9.9 30.0 | 98.9 64 504 | 135.1 31.5±0.17 |     |     |     |     |     |     |
| --------------- | -------- | ----------- | --------------- | --- | --- | --- | --- | --- | --- |
REGNETY-8.0GF 8.0 39.2 18.0 512 113 28.1 31.3±0.08 compare using fixed depth (d = 20) across flop regimes.
|     |     |     |     | To  | compare to our | best | results, | we trained | each model for |
| --- | --- | --- | --- | --- | -------------- | ---- | -------- | ---------- | -------------- |
Table6.EFFICIENTNETcomparisonsonImageNetV2.
|     |     |     |     | 100epochs. | Surprisingly,wefindthatfixed-depthnetworks |     |     |     |     |
| --- | --- | --- | --- | ---------- | ------------------------------------------ | --- | --- | --- | --- |
canmatchtheperformanceofvariabledepthnetworksfor
AppendixA:TestSetEvaluation
|     |     |     |     | allflopregimes,inboththeaverageandbestcase. |     |     |     |     | Indeed, |
| --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | ------- |
InthemainpaperweperformallexperimentsontheIm- thesefixeddepthnetworksmatchourbestresultsin§5.
| ageNet[3]validationset. |     | Hereweevaluateourmodelson |     |     |     |     |     |     |     |
| ----------------------- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- |
Fewerstages.In§5weobservedthatthetopREGNETmod-
theImageNetV2[24]testset(originaltestsetunavailable). elsathighflopshavefewblocksinthefourthstage(oneor
Evaluation setup. To study generalization of models de- two).Hencewetested3stagenetworksat6.4GF,trainedfor
velopedonImageNet,theauthorsof[24]collectanewtest 100epochseach.InFigure19(middle),weshowtheresults
set following the original procedure (ImageNetV2). They and observe that the three stage networks perform consid-
find that the overall model ranks are preserved on the new erably worse. We note, however, that additional changes
testset. Theabsoluteerrors,however,increase. Werepeat (e.g.,inthestemorhead)maybenecessaryforthreestage
thecomparisonsfrom§5ontheImageNetV2testset. networkstoperformwell(leftforfuturework).
RESNE(X)T comparisons. We compare to RESNE(X)T InvertedBottleneck. In§4weobservedthatusingthein-
modelsinTable5. Weobservethatwhilemodelranksare vertedbottleneck(b < 1)degradesperformance. Sinceour
generallyconsistent,thegapbetweenthemdecreases. Nev- results were in alow-compute regime, in Figure 19 (right)
ertheless, REGNETX models still compare favorably, and we re-test at 6.4GF and 100 epochs. Surprisingly, we find
providegoodmodelsacrossflopregimes,includinginlow- thatinthisregimeb<1degradesresultsfurther.
| compute regimes                                  | where | good RESNE(X)T | models are not |       |                 |           |        |            |                  |
| ------------------------------------------------ | ----- | -------------- | -------------- | ----- | --------------- | --------- | ------ | ---------- | ---------------- |
|                                                  |       |                |                | Swish | vs. ReLU        | Many      | recent | methods    | employ the       |
| available. BestresultscanbeachievedusingREGNETY. |       |                |                |       |                 |           |        |            |                  |
|                                                  |       |                |                | Swish | [22] activation | function, |        | e.g. [29]. | In Figure 20, we |
EFFICIENTNET comparisons. We compare to EFFICIENT- studyRegNetYwithSwishandReLU.WefindthatSwish
NET models in Table 6. As before, we observe that the outperformsReLUatlowflops,butReLUisbetterathigh
modelranksaregenerallyconsistentbutthegapdecreases. flops. Interestingly, if g is restricted to be 1 (depthwise
Overall, the results confirm that the REGNET models per- conv), Swish performs much better than ReLU. This sug-
formcomparablytostate-of-the-artEFFICIENTNETwhilebe- geststhatdepthwiseconvandSwishinteractfavorably, al-
ingupto5×fasteronGPUs. thoughtheunderlyingreasonisnotatallclear.
10

100
80
60
40
3.0 2.5 2.0 1.5 1.0 0.5
log10(lr)
rorre
100
80
60
40
6.0 5.5 5.0 4.5 4.0 3.5 3.0
log10(wd)
rorre
100
80
60
40
8 7 6 5 4
log10(lr wd)
rorre
1
0 1
2
3 4
5
0.2 0.4 0.8 1.6 3.2
flops (B)
)rl(01gol
2
3 4
5
a g l o l od 6 b lr e = st 0.1 7
8
0.2 0.4 0.8 1.6 3.2
flops (B)
)dw(01gol
3
4 5
6
a g l o l od 7 b w e d s = t 5105 8
9
0.2 0.4 0.8 1.6 3.2
flops (B)
)dw
rl(01gol
all good best wdlr=5106
1
0
1
2
3
4 5 5 10 50
epochs
)rl(01gol
2
3
4
5
a g l o l od 6
b lr e = st 0.1 7 8 5 10 50
epochs
)dw(01gol
3
4
5
6
a g l o l od 7
b w e d s = t 5105 8 9 5 10 50
epochs
)dw
rl(01gol
all good
best wdlr=5106
Figure21.Optimizationsettings.Fortheseresults,wegeneratea
populationofRegNetXmodelswhilealsorandomlyvaryingthe
initial learning rate (lr) and weight decay (wd) for each model.
Theseresultsuseabatchsizeof128andaretrainedon1GPU.
Top: Distribution of model error versus lr, wd, and also lr·wd
(at10epochsand400MF).Applyinganempiricalbootstrap, we
seethatcleartrendsemerge,especiallyforlrandlr·wd. Middle:
Werepeatthisexperimentbutacrossvariousflopregimes(trained
for10epochseach);thetrendsarestable. Bottom: Similarly,we
repeattheabovewhiletrainingforvariousnumberofepochs(in
the400MFregime),andobservethesametrends. Basedonthese
results, we use an lr = 0.1 and wd = 5·10−5 starting with §4
acrossalltrainingschedulesandflopregimes.
1
0 1
2 3
4
5
B0 B1 B2 B3 B4 B5 model
)rl(01gol
2
3 4
5 a g l o l od 6
b lr e = st 0.2 7
8
B0 B1 B2 B3 B4 B5 model
)dw(01gol
3
4 5
6 a g l o l od 7
b w e d s = t 1105 8
9
B0 B1 B2 B3 B4 B5 model
)dw
rl(01gol
flops(B) params(M) acts(M) epochs enhance error
EFFICIENTNET-B0 0.39 5.3 6.7 100 25.6
EFFICIENTNET-B0 0.39 5.3 6.7 250 25.0
EFFICIENTNET-B0 0.39 5.3 6.7 250 (cid:88) 24.4
EFFICIENTNET-B0[29] 0.39 5.3 6.7 350 (cid:88)(cid:88)(cid:88) 23.7
Table 7. Training enhancements to EFFICIENTNET-B0. Our
EFFICIENTNET-B0 reproduction with DropPath [14] and a 250
epochtrainingschedule(thirdrow),achievesresultsslightlyinfe-
riortooriginalresults(bottomrow),whichadditionallyusedRM-
SProp[30], AutoAugment[2], etc. Withouttheseenhancements
tothetrainingsetupresultsare∼2%lower(toprow),highlighting
theimportanceofcarefullycontrollingthetrainingsetup.
wi, ri, ri wi, ri, ri
⨁ ⨁ wi, ri, ri
1×1 1×1 3×3
1.0 wi/bi, ri, ri wi/bi, ri, ri (c) w V i, r b i, l r o i ck 0.8
3×3, gi 3×3 wi, ri, ri 0.6
wi/bi, ri, ri wi/bi, ri, ri ⨁ 0.4
1×1 1×1 3×3 0.2
(a) w X i, r b i, l r o i ck (b) w R i, r b i, l r o i ck (d) w V i R , ri b , r l i ock 0.0 40.0 42.5 4 e 5. r 0 ro 4 r 7.5 50.0 52.5
all good
best wdlr=2106
Figure22.WerepeatthesweepoverlrandwdforEFFICIENT-
NETtrainingeachmodelfor25epochs.Thelr(withreferenceto
abatchsizeof128)andwdisstableacrossregimes.Weusethese
valuesforallEFFICIENTNETexperimentsinthemaintext(adjust-
ingforbatchsizeaccordingly).SeeFigure21forcomparison.
AppendixC:OptimizationSettings
Ourbasictrainingsettingsfollow[21]asdiscussedin§3.
Totunethelearningratelr andweightdecaywdfor REG-
NET models, we perform a study, described in Figure 21.
Based on this, we set lr = 0.1 and wd = 5·10−5 for all
models in §4 and §5. To enable faster training of our fi-
nalmodelsat100epochs,weincreasethenumberofGPUs
to 8, while keeping the number of images per GPU fixed.
When scaling the batch size, we adjust lr using the linear
scalingruleandapply5epochgradualwarmup[6].
To enable fair comparisons, we repeat the same op-
timization for EFFICIENTNET in Figure 22. Interestingly,
learningrateandweightdecayareagainstableacrosscom-
plexity regimes. Finally, in Table 7 we report the sizable
effect of training enhancement on EFFICIENTNET-B0. The
gapmaybeevenlargerforlargermodels(seeTable4).
.borp
evitalumuc
[46.6|49.3] RegNetVR [46.0|49.2] RegNetV
[41.9|44.3] RegNetR
[38.2|41.0] RegNetX
Figure23.Blocktypesusedinourgeneralizationexperiments(see
§3.4andFigure10).Left:Blockdiagrams.Right:Comparisonof
RegNet with the four block types. The X block performs best.
Interestingly,fortheVblock,residualconnectionsgivenogain.
AppendixD:ImplementationDetails
Weconcludewithadditionalimplementationdetails.
Groupwidthcompatibility. Whensamplingwidthswand
groupswidthsgforourmodels,wemayendupwithincom-
patiblevalues(i.e.wnotdivisiblebyg).Toaddressthis,we
employasimplestrategy. Namely,wesetg = w ifg > w
androundwtobedivisiblebygotherwise. Thefinalwcan
beatmost1/3differentfromtheoriginalw(proofomitted).
For models with bottlenecks, we apply this strategy to the
bottleneckwidthinstead(andadjustwidthsaccordingly).
Group width ranges. As discussed in §4, we notice the
general trend that the group widths of good models are
larger in higher compute regimes. To account for this, we
graduallyadjustthegroupwidthrangesforhighercompute
regimes.Forexample,insteadofsamplingg≤32,at3.2GF
weuse16≤g≤64andallowanygdivisibleby8.
Block types. In §3, we showed that the RegNet design
space generalizes to different block types. We describe
theseadditionalblocktypes,showninFigure23,next:
1. Rblock: sameastheXblockexceptwithoutgroups,
2. Vblock: abasicblockwithonlyasingle3×3conv,
3. VRblock: sameasVblockplusresidualconnections.
Wenotethatgoodparametervaluesmaydifferacrossblock
types. E.g.,incontrasttotheXblock,fortheRblockusing
b>1isbetterthanb=1. Ourapproachisrobusttothis.
Y block details. To obtain the Y block, we add the SE op
afterthe3×3convoftheXblock,andweuseanSEreduc-
tion ratio of 1/4. We experimented with these choices but
foundthattheyperformedcomparably(notshown).
11

| References       |     |              |                                  |     |     |     |     | [20] H.Pham,M.Y.Guan,B.Zoph,Q.V.Le,andJ.Dean.       |     |     |     |     | Ef- |
| ---------------- | --- | ------------ | -------------------------------- | --- | --- | --- | --- | --------------------------------------------------- | --- | --- | --- | --- | --- |
|                  |     |              |                                  |     |     |     |     | ficientneuralarchitecturesearchviaparametersharing. |     |     |     |     | In  |
| [1] F.Chollet.   |     | Xception:    | Deeplearningwithdepthwisesepara- |     |     |     |     | ICML,2018.                                          |     | 2   |     |     |     |
| bleconvolutions. |     | InCVPR,2017. |                                  |     | 7   |     |     |                                                     |     |     |     |     |     |
[21] I.Radosavovic,J.Johnson,S.Xie,W.-Y.Lo,andP.Dolla´r.
[2] E.D.Cubuk,B.Zoph,D.Mane,V.Vasudevan,andQ.V.Le.
|                        |     |          |            |              |          |         |            | Onnetworkdesignspacesforvisualrecognition. |            |                        |     | InICCV,         |     |
| ---------------------- | --- | -------- | ---------- | ------------ | -------- | ------- | ---------- | ------------------------------------------ | ---------- | ---------------------- | --- | --------------- | --- |
| AutoAugment:           |     | Learning |            | augmentation | policies |         | from data. | 2019.                                      | 1,2,3,4,11 |                        |     |                 |     |
| arXiv:1805.09501,2018. |     |          | 8,11       |              |          |         |            |                                            |            |                        |     |                 |     |
|                        |     |          |            |              |          |         |            | [22] P.Ramachandran,B.Zoph,andQ.V.Le.      |            |                        |     | Searchingforac- |     |
| [3] J. Deng,           | W.  | Dong,    | R. Socher, | L.-J.        | Li, K.   | Li, and | L. Fei-    |                                            |            |                        |     |                 |     |
|                        |     |          |            |              |          |         |            | tivationfunctions.                         |            | arXiv:1710.05941,2017. |     | 10              |     |
Fei.Imagenet:Alarge-scalehierarchicalimagedatabase.In [23] E.Real,A.Aggarwal,Y.Huang,andQ.V.Le. Regularized
CVPR,2009. 2,3,8,10 evolutionforimageclassifierarchitecturesearch. InAAAI,
| [4] T.  | DeVries | and           | G. W. | Taylor. | Improved |      | regular- |                                                |     |     |     |     |        |
| ------- | ------- | ------------- | ----- | ------- | -------- | ---- | -------- | ---------------------------------------------- | --- | --- | --- | --- | ------ |
|         |         |               |       |         |          |      |          | 2019.                                          | 2,8 |     |     |     |        |
| ization | of      | convolutional |       | neural  | networks | with | cutout.  |                                                |     |     |     |     |        |
|         |         |               |       |         |          |      |          | [24] B.Recht,R.Roelofs,L.Schmidt,andV.Shankar. |     |     |     |     | Doima- |
arXiv:1708.04552,2017. 8 genetclassifiersgeneralizetoimagenet? arXiv:1902.10811,
| [5] B.EfronandR.J.Tibshirani. |                |     |     | Anintroductiontotheboot- |     |     |     | 2019.           | 2,10      |        |              |          |     |
| ----------------------------- | -------------- | --- | --- | ------------------------ | --- | --- | --- | --------------- | --------- | ------ | ------------ | -------- | --- |
| strap.                        | CRCpress,1994. |     | 3   |                          |     |     |     |                 |           |        |              |          |     |
|                               |                |     |     |                          |     |     |     | [25] M.Sandler, | A.Howard, | M.Zhu, | A.Zhmoginov, | andL.-C. |     |
[6] P. Goyal, P. Dolla´r, R. Girshick, P. Noordhuis, Chen. Mobilenetv2: Inverted residuals and linear bottle-
L. Wesolowski, A. Kyrola, A. Tulloch, Y. Jia, and K. He. necks. InCVPR,2018. 2,7,8
Accurate,largeminibatchsgd: Trainingimagenetin1hour. [26] K. Simonyan and A. Zisserman. Very deep convolutional
| arXiv:1706.02677,2017. |        |        | 11      |        |      |         |           |                                         |     |     |     |              |     |
| ---------------------- | ------ | ------ | ------- | ------ | ---- | ------- | --------- | --------------------------------------- | --- | --- | --- | ------------ | --- |
|                        |        |        |         |        |      |         |           | networksforlarge-scaleimagerecognition. |     |     |     | InICLR,2015. |     |
| [7] K.                 | He, X. | Zhang, | S. Ren, | and J. | Sun. | Delving | deep into | 1,2                                     |     |     |     |              |     |
rectifiers:Surpassinghuman-levelperformanceonimagenet [27] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. Reed,
classification. InICCV,2015. 2 D.Anguelov, D.Erhan, V.Vanhoucke, andA.Rabinovich.
[8] K.He,X.Zhang,S.Ren,andJ.Sun. Deepresiduallearning Goingdeeperwithconvolutions. InCVPR,2015. 2
forimagerecognition. InCVPR,2016. 1,2,3,9 [28] C.Szegedy,V.Vanhoucke,S.Ioffe,J.Shlens,andZ.Wojna.
Rethinkingtheinceptionarchitectureforcomputervision.In
[9] A.G.Howard,M.Zhu,B.Chen,D.Kalenichenko,W.Wang,
|                                 |     |     |     |     |     |             |       | CVPR,2016. |     | 2   |     |     |     |
| ------------------------------- | --- | --- | --- | --- | --- | ----------- | ----- | ---------- | --- | --- | --- | --- | --- |
| T.Weyand,M.Andreetto,andH.Adam. |     |     |     |     |     | Mobilenets: | Effi- |            |     |     |     |     |     |
cientconvolutionalneuralnetworksformobilevisionappli- [29] M.TanandQ.V.Le.Efficientnet:Rethinkingmodelscaling
cations. arXiv:1704.04861,2017. 2,8 forconvolutionalneuralnetworks. ICML,2019. 1,2,7,9,
10,11
| [10] J. Hu, | L. Shen, | and | G. Sun. | Squeeze-and-excitation |     |     | net- |     |     |     |     |     |     |
| ----------- | -------- | --- | ------- | ---------------------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
works. InCVPR,2018. 7 [30] T. Tieleman and G. Hinton. Lecture 6.5-rmsprop: Divide
[11] G.Huang,Z.Liu,L.VanDerMaaten,andK.Q.Weinberger. the gradient by a running average of its recent magnitude.
|                                        |     |     |     |     |     |              |     | Coursera:Neuralnetworksformachinelearning,2012. |     |     |     |            | 11  |
| -------------------------------------- | --- | --- | --- | --- | --- | ------------ | --- | ----------------------------------------------- | --- | --- | --- | ---------- | --- |
| Denselyconnectedconvolutionalnetworks. |     |     |     |     |     | InCVPR,2017. |     |                                                 |     |     |     |            |     |
|                                        |     |     |     |     |     |              |     | [31] S.Xie,R.Girshick,P.Dolla´r,Z.Tu,andK.He.   |     |     |     | Aggregated |     |
2
residualtransformationsfordeepneuralnetworks.InCVPR,
| [12] S.IoffeandC.Szegedy.                              |             |     | Batchnormalization: |     |               | Accelerating |          |                                 |       |     |                       |     |     |
| ------------------------------------------------------ | ----------- | --- | ------------------- | --- | ------------- | ------------ | -------- | ------------------------------- | ----- | --- | --------------------- | --- | --- |
| deepnetworktrainingbyreducinginternalcovariateshift.In |             |     |                     |     |               |              |          | 2017.                           | 2,4,9 |     |                       |     |     |
|                                                        |             |     |                     |     |               |              |          | [32] S.ZagoruykoandN.Komodakis. |       |     | Wideresidualnetworks. |     |     |
| ICML,2015.                                             |             | 4   |                     |     |               |              |          |                                 |       |     |                       |     |     |
|                                                        |             |     |                     |     |               |              |          | InBMVC,2016.                    |       | 2   |                       |     |     |
| [13] A.                                                | Krizhevsky, | I.  | Sutskever,          | and | G. E. Hinton. |              | Imagenet |                                 |       |     |                       |     |     |
classification with deep convolutional neural networks. In [33] X. Zhang, X. Zhou, M. Lin, and J. Sun. Shufflenet: An
extremelyefficientconvolutionalneuralnetworkformobile
| NIPS,2012.                              |          | 1,2       |          |                   |            |                 |             |                                                       |               |                                   |     |                    |     |
| --------------------------------------- | -------- | --------- | -------- | ----------------- | ---------- | --------------- | ----------- | ----------------------------------------------------- | ------------- | --------------------------------- | --- | ------------------ | --- |
|                                         |          |           |          |                   |            |                 |             | devices.                                              | InCVPR,2018.  | 8                                 |     |                    |     |
| [14] G.                                 | Larsson, | M. Maire, | and      | G. Shakhnarovich. |            |                 | Fractalnet: |                                                       |               |                                   |     |                    |     |
|                                         |          |           |          |                   |            |                 |             | [34] B.ZophandQ.V.Le.                                 |               | Neuralarchitecturesearchwithrein- |     |                    |     |
| Ultra-deep                              |          | neural    | networks | without           | residuals. |                 | In ICLR,    |                                                       |               |                                   |     |                    |     |
| 2017.                                   | 8,11     |           |          |                   |            |                 |             | forcementlearning.                                    |               | InICLR,2017.                      | 1   |                    |     |
|                                         |          |           |          |                   |            |                 |             | [35] B. Zoph,                                         | V. Vasudevan, | J. Shlens,                        | and | Q. V. Le. Learning |     |
| [15] Y.                                 | LeCun,   | B. Boser, | J. S.    | Denker,           | D.         | Henderson,      | R. E.       |                                                       |               |                                   |     |                    |     |
|                                         |          |           |          |                   |            |                 |             | transferablearchitecturesforscalableimagerecognition. |               |                                   |     |                    | In  |
| Howard,                                 | W.       | Hubbard,  | and      | L. D.             | Jackel.    | Backpropagation |             |                                                       |               |                                   |     |                    |     |
|                                         |          |           |          |                   |            |                 |             | CVPR,2018.                                            |               | 2,8                               |     |                    |     |
| appliedtohandwrittenzipcoderecognition. |          |           |          |                   |            | Neuralcompu-    |             |                                                       |               |                                   |     |                    |     |
| tation,1989.                            |          | 1         |          |                   |            |                 |             |                                                       |               |                                   |     |                    |     |
[16] C.-Y.Lee,S.Xie,P.Gallagher,Z.Zhang,andZ.Tu.Deeply-
| supervisednets. |     | InAISTATS,2015. |     |     | 8   |     |     |     |     |     |     |     |     |
| --------------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
[17] C.Liu,B.Zoph,M.Neumann,J.Shlens,W.Hua,L.-J.Li,
| L.Fei-Fei,A.Yuille,J.Huang,andK.Murphy.               |          |           |              |              |        |                | Progressive |     |     |     |     |     |     |
| ----------------------------------------------------- | -------- | --------- | ------------ | ------------ | ------ | -------------- | ----------- | --- | --- | --- | --- | --- | --- |
| neuralarchitecturesearch.                             |          |           |              | InECCV,2018. |        | 2,8            |             |     |     |     |     |     |     |
| [18] H.                                               | Liu, K.  | Simonyan, | and          | Y. Yang.     | Darts: | Differentiable |             |     |     |     |     |     |     |
| architecturesearch.                                   |          |           | InICLR,2019. |              | 1,2,8  |                |             |     |     |     |     |     |     |
| [19] N.Ma,                                            | X.Zhang, |           | H.-T.Zheng,  | andJ.Sun.    |        | Shufflenetv2:  |             |     |     |     |     |     |     |
| Practicalguidelinesforefficientcnnarchitecturedesign. |          |           |              |              |        |                | In          |     |     |     |     |     |     |
| ECCV,2018.                                            |          | 8         |              |              |        |                |             |     |     |     |     |     |     |
12