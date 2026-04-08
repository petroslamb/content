| Visualizing | the | Loss Landscape |     | of Neural | Nets |
| ----------- | --- | -------------- | --- | --------- | ---- |
HaoLi1,ZhengXu1,GavinTaylor2,ChristophStuder3,TomGoldstein1
1UniversityofMaryland,CollegePark2UnitedStatesNavalAcademy3CornellUniversity
{haoli,xuzh,tomg}@cs.umd.edu,taylor@usna.edu,studer@cornell.edu
Abstract
8102 voN 7  ]GL.sc[  3v31990.2171:viXra
Neuralnetworktrainingreliesonourabilitytofind“good”minimizersofhighly
| non-convex | loss functions. | It is well-known | that certain | network | architecture |
| ---------- | --------------- | ---------------- | ------------ | ------- | ------------ |
designs(e.g.,skipconnections)producelossfunctionsthattraineasier,andwell-
chosentrainingparameters(batchsize,learningrate,optimizer)produceminimiz-
| ers that                                                  | generalize better. | However, the reasons | for these | differences,   | and their |
| --------------------------------------------------------- | ------------------ | -------------------- | --------- | -------------- | --------- |
| effectsontheunderlyinglosslandscape,arenotwellunderstood. |                    |                      |           | Inthispaper,we |           |
explorethestructureofneurallossfunctions,andtheeffectoflosslandscapeson
| generalization,usingarangeofvisualizationmethods. |     |     | First,weintroduceasimple |     |     |
| ------------------------------------------------- | --- | --- | ------------------------ | --- | --- |
“filternormalization”methodthathelpsusvisualizelossfunctioncurvatureand
| makemeaningfulside-by-sidecomparisonsbetweenlossfunctions. |     |     |     |     | Then,using |
| ---------------------------------------------------------- | --- | --- | --- | --- | ---------- |
avarietyofvisualizations,weexplorehownetworkarchitectureaffectstheloss
landscape,andhowtrainingparametersaffecttheshapeofminimizers.
1 Introduction
Training neural networks requires minimizing a high-dimensional non-convex loss function – a
task that is hard in theory, but sometimes easy in practice. Despite the NP-hardness of training
generalneurallossfunctions[2],simplegradientmethodsoftenfindglobalminimizers(parameter
configurationswithzeroornear-zerotrainingloss),evenwhendataandlabelsarerandomizedbefore
training[42]. However,thisgoodbehaviorisnotuniversal;thetrainabilityofneuralnetsishighly
dependentonnetworkarchitecturedesignchoices,thechoiceofoptimizer,variableinitialization,and
avarietyofotherconsiderations. Unfortunately,theeffectofeachofthesechoicesonthestructureof
theunderlyinglosssurfaceisunclear. Becauseoftheprohibitivecostoflossfunctionevaluations
(whichrequiresloopingoverallthedatapointsinthetrainingset),studiesinthisfieldhaveremained
predominantlytheoretical.
| (a) withoutskipconnections |     |     | (b) | withskipconnections |     |
| -------------------------- | --- | --- | --- | ------------------- | --- |
Figure 1: The loss surfaces of ResNet-56 with/without skip connections. The proposed filter
normalizationschemeisusedtoenablecomparisonsofsharpness/flatnessbetweenthetwofigures.
32ndConferenceonNeuralInformationProcessingSystems(NIPS2018),Montréal,Canada.

Visualizationshavethepotentialtohelpusanswerseveralimportantquestionsaboutwhyneural
networkswork. Inparticular,whyareweabletominimizehighlynon-convexneurallossfunctions?
Andwhydotheresultingminimageneralize? Toclarifythesequestions, weusehigh-resolution
visualizations to provide an empirical characterization of neural loss functions, and explore how
differentnetworkarchitecturechoicesaffectthelosslandscape. Furthermore,weexplorehowthe
non-convex structure of neural loss functions relates to their trainability, and how the geometry
ofneuralminimizers(i.e.,theirsharpness/flatness,andtheirsurroundinglandscape),affectstheir
generalizationproperties.
Todothisinameaningfulway,weproposeasimple“filternormalization”schemethatenablesusto
doside-by-sidecomparisonsofdifferentminimafoundduringtraining. Wethenusevisualizationsto
exploresharpness/flatnessofminimizersfoundbydifferentmethods,aswellastheeffectofnetwork
architecturechoices(useofskipconnections,numberoffilters,networkdepth)onthelosslandscape.
Ourgoalistounderstandhowlossfunctiongeometryaffectsgeneralizationinneuralnets.
1.1 Contributions
Westudymethodsforproducingmeaningfullossfunctionvisualizations. Then,usingthesevisualiza-
tionmethods,weexplorehowlosslandscapegeometryaffectsgeneralizationerrorandtrainability.
Morespecifically,weaddressthefollowingissues:
• We reveal faults in a number of visualization methods for loss functions, and show that
simplevisualizationstrategiesfailtoaccuratelycapturethelocalgeometry(sharpnessor
flatness)oflossfunctionminimizers.
• Wepresentasimplevisualizationmethodbasedon“filternormalization.” Thesharpnessof
minimizerscorrelateswellwithgeneralizationerrorwhenthisnormalizationisused,even
when making comparisons across disparate network architectures and training methods.
Thisenablesside-by-sidecomparisonsofdifferentminimizers1.
• Weobservethat,whennetworksbecomesufficientlydeep,neurallosslandscapesquickly
transitionfrombeingnearlyconvextobeinghighlychaotic. Thistransitionfromconvexto
chaoticbehaviorcoincideswithadramaticdropingeneralizationerror,andultimatelytoa
lackoftrainability.
• We observe that skip connections promote flat minimizers and prevent the transition to
chaotic behavior, which helps explain why skip connections are necessary for training
extremelydeepnetworks.
• Wequantitativelymeasurenon-convexitybycalculatingthesmallest(mostnegative)eigen-
valuesoftheHessianaroundlocalminima,andvisualizingtheresultsasaheatmap.
• WestudythevisualizationofSGDoptimizationtrajectories. Weexplainthedifficulties
thatarisewhenvisualizingthesetrajectories, andshowthatoptimizationtrajectorieslie
inanextremelylowdimensionalspace. Thislowdimensionalitycanbeexplainedbythe
presenceoflarge,nearlyconvexregionsinthelosslandscape,suchasthoseobservedinour
2-dimensionalvisualizations.
2 TheoreticalBackground
Numeroustheoreticalstudieshavebeendoneonourabilitytooptimizeneurallossfunction[5,4].
Theoreticalresultsusuallymakerestrictiveassumptionsaboutthesampledistributions,non-linearity
of the architecture, or loss functions [16, 31, 40, 36, 9, 39]. For restricted network classes, such
as those with a single hidden layer, globally optimal or near-optimal solutions can be found by
commonoptimizationmethods[35,26,38]. Fornetworkswithspecificstructures,therelikelyexists
amonotonicallydecreasingpathfromaninitializationtoaglobalminimum[32,15]. Swirszczetal.
[37]showcounterexamplesthatachieve“bad”localminimafortoyproblems.
Severalworkshaveaddressedtherelationshipbetweensharpness/flatnessoflocalminimaandtheir
generalizationability.HochreiterandSchmidhuber[18]defined“flatness”asthesizeoftheconnected
region around the minimum where the training loss remains low. Keskar et al. [24] characterize
1Codeandplotsareavailableathttps://github.com/tomgoldstein/loss-landscape
2

flatnessusingeigenvaluesoftheHessian,andpropose(cid:15)-sharpnessasanapproximation,whichlooks
atthemaximumlossinaneighborhoodofaminimum. Dinhetal.[7],Neyshaburetal.[30]show
thatthesequantitativemeasureofsharpnessarenotinvarianttosymmetriesinthenetwork,andare
thusnotsufficienttodeterminegeneralizationability. Chaudharietal.[3]usedlocalentropyasa
measureofsharpness,whichisinvarianttothesimpletransformationin[7],butdifficulttoaccurately
compute. DziugaiteandRoy[8]connectsharpnesstoPAC-Bayesboundsforgeneralization.
3 TheBasicsofLossFunctionVisualization
Neuralnetworksaretrainedonacorpusoffeaturevectors(e.g.,images){x }andaccompanying
i
labels {y } by minimizing a loss of the form L(θ) = 1 (cid:80)m (cid:96)(x ,y ;θ), where θ denotes the
i m i=1 i i
parameters(weights)oftheneuralnetwork,thefunction(cid:96)(x ,y ;θ)measureshowwelltheneural
i i
networkwithparametersθpredictsthelabelofadatasample,andmisthenumberofdatasamples.
Neuralnetscontainmanyparameters,andsotheirlossfunctionsliveinaveryhigh-dimensional
space.Unfortunately,visualizationsareonlypossibleusinglow-dimensional1D(line)or2D(surface)
plots. Severalmethodsexistforclosingthisdimensionalitygap.
1-Dimensional Linear Interpolation One simple and lightweight way to plot loss functions is
tochoosetwosetsofparametersθ andθ(cid:48),andplotthevaluesofthelossfunctionalongtheline
connectingthesetwopoints. Wecanparameterizethislinebychoosingascalarparameterα,and
definingtheweightedaverageθ(α)=(1−α)θ+αθ(cid:48).Finally,weplotthefunctionf(α)=L(θ(α)).
ThisstrategywastakenbyGoodfellowetal.[13],whostudiedthelosssurfacealongthelinebetween
arandominitialguess,andanearbyminimizerobtainedbystochasticgradientdescent. Thismethod
hasbeenwidelyusedtostudythe“sharpness”and“flatness”ofdifferentminima,andthedependence
ofsharpnessonbatch-size[24,7]. SmithandTopin[34]usethesametechniquetoshowdifferent
minimaandthe“peaks”betweenthem,whileImetal.[21]plotthelinebetweenminimaobtained
viadifferentoptimizers.
The1Dlinearinterpolationmethodsuffersfromseveralweaknesses. First,itisdifficulttovisualize
non-convexities using 1D plots. Indeed, Goodfellow et al. [13] found that loss functions appear
tolacklocalminimaalongtheminimizationtrajectory. Wewillseelater,using2Dmethods,that
somelossfunctionshaveextremenon-convexities,andthatthesenon-convexitiescorrelatewiththe
differenceingeneralizationbetweendifferentnetworkarchitectures. Second,thismethoddoesnot
considerbatchnormalization[22]orinvariancesymmetriesinthenetwork. Forthisreason,thevisual
sharpnesscomparisonsproducedby1Dinterpolationplotsmaybemisleading; thisissuewillbe
exploredindepthinSection5.
Contour Plots & Random Directions To use this approach, one chooses a center point θ∗ in
the graph, and chooses two direction vectors, δ and η. One then plots a function of the form
f(α)=L(θ∗+αδ)inthe1D(line)case,or
f(α,β)=L(θ∗+αδ+βη) (1)
in the 2D (surface) case2. This approach was used in [13] to explore the trajectories of different
minimizationmethods. Itwasalsousedin[21]toshowthatdifferentoptimizationalgorithmsfind
differentlocalminimawithinthe2Dprojectedspace. Becauseofthecomputationalburdenof2D
plotting,thesemethodsgenerallyresultinlow-resolutionplotsofsmallregionsthathavenotcaptured
thecomplexnon-convexityoflosssurfaces. Below,weusehigh-resolutionvisualizationsoverlarge
slicesofweightspacetovisualizehownetworkdesignaffectsnon-convexstructure.
4 ProposedVisualization: Filter-WiseNormalization
Thisstudyreliesheavilyonplotsoftheform(1)producedusingrandomdirectionvectors,δandη,
eachsampledfromarandomGaussiandistributionwithappropriatescaling(describedbelow). While
the“randomdirections”approachtoplottingissimple,itfailstocapturetheintrinsicgeometryofloss
surfaces,andcannotbeusedtocomparethegeometryoftwodifferentminimizersortwodifferent
2When making 2D plots in this paper, batch normalization parameters are held constant, i.e., random
directionsarenotappliedtobatchnormalizationparameters.
3

networks. Thisisbecauseofthescaleinvarianceinnetworkweights. WhenReLUnon-linearities
areused,thenetworkremainsunchangedifwe(forexample)multiplytheweightsinonelayerofa
networkby10,anddividethenextlayerby10. Thisinvarianceisevenmoreprominentwhenbatch
normalizationisused. Inthiscase,thesize(i.e.,norm)ofafilterisirrelevantbecausetheoutputof
eachlayerisre-scaledduringbatchnormalization. Forthisreason,anetwork’sbehaviorremains
unchangedifwere-scaletheweights. Note,thisscaleinvarianceappliesonlytorectifiednetworks.
Scaleinvariancepreventsusfrommakingmeaningfulcomparisonsbetweenplots,unlessspecial
precautionsaretaken. Aneuralnetworkwithlargeweightsmayappeartohaveasmoothandslowly
varying loss function; perturbing the weights by one unit will have very little effect on network
performance if the weights live on a scale much larger than one. However, if the weights are
much smaller than one, then that same unit perturbation may have a catastrophic effect, making
thelossfunctionappearquitesensitivetoweightperturbations. Keepinmindthatneuralnetsare
scaleinvariant;ifthesmall-parameterandlarge-parameternetworksinthisexampleareequivalent
(becauseoneissimplyarescalingoftheother),thenanyapparentdifferencesinthelossfunctionare
merelyanartifactofscaleinvariance. ThisscaleinvariancewasexploitedbyDinhetal.[7]tobuild
pairsofequivalentnetworksthathavedifferentapparentsharpness.
Toremovethisscalingeffect,weplotlossfunctionsusingfilter-wisenormalizeddirections. Toobtain
suchdirectionsforanetworkwithparametersθ,webeginbyproducingarandomGaussiandirection
vectordwithdimensionscompatiblewithθ. Then,wenormalizeeachfilterindtohavethesame
normofthecorrespondingfilterinθ.Inotherwords,wemakethereplacementd ← di,j (cid:107)θ (cid:107),
i,j (cid:107)di,j(cid:107) i,j
whered representsthejthfilter(notthejthweight)oftheithlayerofd,and(cid:107)·(cid:107)denotesthe
i,j
Frobeniusnorm.Notethatthefilter-wisenormalizationisdifferentfromthatof[21],whichnormalize
thedirectionwithoutconsideringthenormofindividualfilters. Notethatfilternormalizationisnot
limitedtoconvolutional(Conv)layersbutalsoappliestofullyconnected(FC)layers. TheFClayer
isequivalenttoaConvlayerwitha1×1outputfeaturemapandthefiltercorrespondstotheweights
thatgenerateoneneuron.
Docontourplotsoftheform(1)capturethenaturaldistancescaleoflosssurfaceswhenthedirections
δ andη arefilternormalized? WeanswerthisquestiontotheaffirmativeinSection5byshowing
thatthesharpnessoffilter-normalizedplotscorrelateswellwithgeneralizationerror, whileplots
withoutfilternormalizationcanbeverymisleading. InAppendixA.2,wealsocomparefilter-wise
normalizationtolayer-wisenormalization(andnonormalization),andshowthatfilternormalization
producessuperiorcorrelationbetweensharpnessandgeneralizationerror.
5 TheSharpvsFlatDilemma
Section 4 introduces the concept of filter normalization, and provides an intuitive justification
for its use. In this section, we address the issue of whether sharp minimizers generalize better
thanflatminimizers. Indoingso,wewillseethatthesharpnessofminimizerscorrelateswellwith
generalizationerrorwhenfilternormalizationisused.Thisenablesside-by-sidecomparisonsbetween
plots. Incontrast,thesharpnessofnon-normalizedplotsmayappeardistortedandunpredictable.
Itiswidelythoughtthatsmall-batchSGDproduces“flat”minimizersthatgeneralizewell,whilelarge
batchesproduce“sharp”minimawithpoorgeneralization[3,24,18]. Thisclaimisdisputedthough,
withDinhetal.[7],Kawaguchietal.[23]arguingthatgeneralizationisnotdirectlyrelatedtothe
curvatureoflosssurfaces,andsomeauthorsproposingspecializedtrainingmethodsthatachievegood
performancewithlargebatchsizes[19,14,6]. Here,weexplorethedifferencebetweensharpand
flatminimizers. Webeginbydiscussingdifficultiesthatarisewhenperformingsuchavisualization,
andhowpropernormalizationcanpreventsuchplotsfromproducingdistortedresults.
WetrainaCIFAR-10classifierusinga9-layerVGGnetwork[33]withbatchnormalizationfora
fixednumberofepochs. Weusetwobatchsizes: alargebatchsizeof8192(16.4%ofthetraining
dataofCIFAR-10),andasmallbatchsizeof128. Letθsandθl indicatethesolutionsobtainedby
runningSGDusingsmallandlargebatchsizes,respectively3. Usingthelinearinterpolationapproach
3Inthissection,weconsiderthe“runningmean”and“runningvariance”astrainableparametersandinclude
theminθ.NotethattheoriginalstudybyGoodfellowetal.[13]doesnotconsiderbatchnormalization.These
parametersarenotincludedinθinfuturesections,astheyareonlyneededwheninterpolatingbetweentwo
minimizers.
4

| 5   | 100 |     | 51e5   |     |     |
| --- | --- | --- | ------ | --- | --- |
|     |     | 160 | bs=128 |     |     |
bs=128
| 4   | 80  | sthgiew fo mron-2L 140 | bs=8192 |     | bs=8192 |
| --- | --- | ---------------------- | ------- | --- | ------- |
4
| 3    | 60 ycaruccA | 120 |     |     |     |
| ---- | ----------- | --- | --- | --- | --- |
| ssoL |             |     | 3   |     |     |
100
| 2   | 40  |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
2
80
| 1   | 20  |     | 1   |     |     |
| --- | --- | --- | --- | --- | --- |
60
|     |     | 0 50 100 150 | 200 250 300 |     |     |
| --- | --- | ------------ | ----------- | --- | --- |
0 0.50 0.250.00 0.25 0.50 0.75 1.00 1.25 1.50 0 Epochs 0 0.2 0.1 0.0 0.1 0.2
| (a) 7.37% | 11.07% | (b) (cid:107)θ(cid:107) ,WD=0 |     | (c) WD=0 |     |
| --------- | ------ | ----------------------------- | --- | -------- | --- |
2
| 5   | 100 | 60                 | 51e5    |     |         |
| --- | --- | ------------------ | ------- | --- | ------- |
|     |     |                    | bs=128  |     | bs=128  |
|     |     | 55                 | bs=8192 |     |         |
| 4   | 80  | sthgiew fo mron-2L | 4       |     | bs=8192 |
50
ycaruccA
| 3    | 60  | 45  | 3   |     |     |
| ---- | --- | --- | --- | --- | --- |
| ssoL |     | 40  |     |     |     |
| 2    | 40  | 35  | 2   |     |     |
30
| 1   | 20  |     | 1   |     |     |
| --- | --- | --- | --- | --- | --- |
25
| 0   | 0   | 0 50 100 150 | 200 250 300 0 |     |     |
| --- | --- | ------------ | ------------- | --- | --- |
0.50 0.250.00 0.25 0.50 0.75 1.00 1.25 1.50 Epochs 0.010 0.005 0.000 0.005 0.010
| (d) 6.0% | 10.19% | (e) (cid:107)θ(cid:107) 2 ,WD=5e-4 |     | (f) WD=5e-4 |     |
| -------- | ------ | ---------------------------------- | --- | ----------- | --- |
Figure2: (a)and(d)arethe1DlinearinterpolationofVGG-9solutionsobtainedbysmall-batchand
large-batchtrainingmethods. Thebluelinesarelossvaluesandtheredlinesareaccuracies. The
solidlinesaretrainingcurvesandthedashedlinesarefortesting. Smallbatchisatabscissa0,and
largebatchisatabscissa1. Thecorrespondingtesterrorsareshownbelow. (b)and(e)showsthe
changeofweightsnorm(cid:107)θ(cid:107) 2 duringtraining. Whenweightdecayisdisabled,theweightnormgrows
steadilyduringtrainingwithoutconstraints(c)and(f)aretheweighthistograms,whichverifythat
small-batchmethodsproducemorelargeweightswithzeroweightdecayandmoresmallweights
withnon-zeroweightdecay.
[13],weplotthelossvaluesonbothtrainingandtestingdatasetsofCIFAR-10,alongadirection
containingthetwosolutions,i.e.,f(α)=L(θs+α(θl−θs)).
Figure2(a)showslinearinterpolationplotswithθs atx-axislocation0, andθl atlocation1. As
observedby[24],wecanclearlyseethatthesmall-batchsolutionisquitewide,whilethelarge-batch
solution is sharp. However, this sharpness balance can be flipped simply by turning on weight
decay[25]. Figure2(d)showresultsofthesameexperiment,exceptthistimewithanon-zeroweight
decayparameter. Thistime,thelargebatchminimizerisconsiderablyflatterthanthesharpsmall
batch minimizer. However, we see that small batches generalize better in all experiments; there
isnoapparentcorrelationbetweensharpnessandgeneralization. Wewillseethatthesesharpness
comparisonsareextremelymisleading,andfailtocapturetheendogenouspropertiesoftheminima.
Theapparentdifferencesinsharpnesscanbeexplainedbyexaminingtheweightsofeachminimizer.
HistogramsofthenetworkweightsareshownforeachexperimentinFigure2(c)and(f). Wesee
that, whenalargebatchisusedwithzeroweightdecay, theresultingweightstendtobesmaller
thaninthesmallbatchcase. Wereversethiseffectbyaddingweightdecay;inthiscasethelarge
batchminimizerhasmuchlargerweightsthanthesmallbatchminimizer. Thisdifferenceinscale
occursforasimplereason: Asmallerbatchsizeresultsinmoreweightupdatesperepochthana
largebatchsize,andsotheshrinkingeffectofweightdecay(whichimposesapenaltyonthenormof
theweights)ismorepronounced. Theevolutionoftheweightnormsduringtrainingisdepictedin
Figure2(b)and(e). Figure2isnotvisualizingtheendogenoussharpnessofminimizers,butrather
justthe(irrelevant)weightscaling. Thescalingofweightsinthesenetworksisirrelevantbecause
batchnormalizationre-scalestheoutputstohaveunitvariance. However,smallweightsstillappear
moresensitivetoperturbations,andproducesharperlookingminimizers.
Filter Normalized Plots We repeat the experiment in Figure 2, but this time we plot the loss
functionneareachminimizerseparatelyusingrandomfilter-normalizeddirections. Thisremovesthe
apparentdifferencesingeometrycausedbythescalingdepictedinFigure2(c)and(f). Theresults,
presentedinFigure3,stillshowdifferencesinsharpnessbetweensmallbatchandlargebatchminima,
howeverthesedifferencesaremuchmoresubtlethanitwouldappearintheun-normalizedplots. For
comparison,sampleun-normalizedplotsandlayer-normalizedplotsareshowninSectionA.2of
5

| 5      |     | 100 5     |     | 100 5     |     |     | 100 5     |     | 100      |
| ------ | --- | --------- | --- | --------- | --- | --- | --------- | --- | -------- |
| 4      |     | 80 4      |     | 80 4      |     |     | 80 4      |     | 80       |
|        |     | ycaruccA  |     | ycaruccA  |     |     | ycaruccA  |     | ycaruccA |
| ssoL 3 |     | 60 ssoL 3 |     | 60 ssoL 3 |     |     | 60 ssoL 3 |     | 60       |
| 2      |     | 40 2      |     | 40 2      |     |     | 40 2      |     | 40       |
| 1      |     | 20 1      |     | 20 1      |     |     | 20 1      |     | 20       |
01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0
(a) 0.0,128,7.37% (b) 0.0,8192,11.07% (c) 5e-4,128,6.00% (d) 5e-4,8192,10.19%
| 1 . 0 0                                            | 8 .1 0          |                             |     |         |     |     |         |                 |     |
| -------------------------------------------------- | --------------- | --------------------------- | --- | ------- | --- | --- | ------- | --------------- | --- |
| 9. 6988 0... 161 0 7000 6000 0 . 1. 0 0 0 0 01 0 0 | 0 6 .6 0 0 7 .6 | 0 0 8.96 .0190.0600 1 . 0 0 |     | 1 . 0 0 |     |     | 1 . 0 0 | 8 .9 6 .01 00 0 |     |
0 . 7 5 . 7 6 6 6 . 4 . 1 0 0 3 .6 00 0 0 . 7 5 7 . 1 0 0 0 . 7 5 1 0 0 3 .1 0 0 0 . 7 5 9 9.6.801.00 760 .06000 6 . 1 0 0 9 . 6 00
|     | 2 . 6 0 0 |     |     |     | 3 . |     |     |     | 8   |
| --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
0 . 5 0 0 . 6 0 0 0 . 5 0 5 .10 0 43 0 . 5 0 00 1 . 1 0 0 0 .600 0 . 5 0 8.10 0 4 .1 0 0 3 . 6 0 0 2 .6 . 1 0 0
0 . 2 5 0 . 2 5 0 ..66 0 0 00 8.6 0 . 2 5 5.6 3.6 00 0 . 2 5 0 0 6. 6
|     |     | 7.100 | 00 00 3.100 2 .1 0 0 . 1 0 0 2.600 | 0 0 9.600 |     |     |     | 1 0 0 | 0 . 1 0 0 0 0 |
| --- | --- | ----- | ---------------------------------- | --------- | --- | --- | --- | ----- | ------------- |
0 . 0 0 6 .600 0. 5.600 0 . 0 0 6.1 5.600 4 .1 0.6 7.6008.1 0 0 0 . 0 0 0.10 0 0 . 0 0 1 . 5 .600
0 . 2 5 1 0 0 0 . 2 5 00 1. 1 0 1 .60 0 0 . 2 5 0 . 2 5 1 . 6 0 0 0 . 6 0 0
|     |     |     | 6 .6 0 0 0 |     |     | . 6 0 0 |     | 4 .6 0 0 2 . 1 0 0 | 3 .1 00 |
| --- | --- | --- | ---------- | --- | --- | ------- | --- | ------------------ | ------- |
0 . 5 0 2 . 1 0 1 . 1 0 0 .6 0 0 0 . 5 0 9 . 1 0 0 0 . 5 0 5 5 2 . 10 1 0 0 . 5 0 5 . 1 0 0 9 . 10 0
0 . 7 5 9 . 6 98 0 .. 160 0 87 .. 5.1 00 0 1 99.6..8610.10000 00 0 0 . 7 5 0 . 7 5 6 .60 6.10 0 . 60 0 .1 0 0 4.1 0 0 2 . 6 0 0 . 7 5 8 .6 0 0 7 .1 0 0
| 0 00 16 0000 4 . 6 0 0 | 3 . 1 0 0 | 8   |     | 7.1 0 0 0 | 0 4 . 6 | 3.60 0 4. 1 | 0 0 600 |     |     |
| ---------------------- | --------- | --- | --- | --------- | ------- | ----------- | ------- | --- | --- |
1 . 0 0 1 .0 0 0 . )7 5 0.5. 0 7 0 .1 . 0 21 0 5 0 . 08 0 07 .2 5 0 .7 50 0 .7 5 1.00 1 . 0 0 (1.0f0)0.075.00.5,0 0 . 12 5 0 . 0 0 0 . 2 51 0. 05070%.75 1.00 1 . 0 0 1(.0 0 0 . 7 5 0 .5 -0 0 0 40, . 2 5 102.00 ,0.2 5 6.00 . 5 0 %0 . 7 5 4 . 1.00 1 . 0 0 h1 . 00 05.75e 0 . 5 0 08 . 2 5 09 . 0 0 0 .2 510 0 . 5 0 90.75%1.00
( e 0 0 , 2 , . 3 % 8 9 2 , 1 . g ) 5 e 8 0 ( ) - 4 , 1 2 , . 1
Figure3: The1Dand2DvisualizationofsolutionsobtainedusingSGDwithdifferentweightdecay
andbatchsize. Thetitleofeachsubfigurecontainstheweightdecay,batchsize,andtesterror.
theAppendix. Wealsovisualizetheseresultsusingtworandomdirectionsandcontourplots. The
weights obtained with small batch size and non-zero weight decay have wider contours than the
sharperlargebatchminimizers. ResultsforResNet-56appearinFigure15oftheAppendix. Using
thefilter-normalizedplotsinFigure3,wecanmakeside-by-sidecomparisonsbetweenminimizers,
andweseethatnowsharpnesscorrelateswellwithgeneralizationerror. Largebatchesproduced
visuallysharperminima(althoughnotdramaticallyso)withhighertesterror.
6 WhatMakesNeuralNetworksTrainable? Insightsonthe(Non)Convexity
StructureofLossSurfaces
Ourabilitytofindglobalminimizerstoneurallossfunctionsisnotuniversal; itseemsthatsome
neuralarchitecturesareeasiertominimizethanothers. Forexample,usingskipconnections,the
authorsof[17]trainedextremelydeeparchitectures,whilecomparablearchitectureswithoutskip
connectionsarenottrainable. Furthermore,ourabilitytotrainseemstodependstronglyontheinitial
parametersfromwhichtrainingstarts. Usingvisualizationmethods,wedoanempiricalstudyof
neural architectures to explore why the non-convexity of loss functions seems to be problematic
insomesituations,butnotinothers. Weaimtoprovideinsightintothefollowingquestions: Do
lossfunctionshavesignificantnon-convexityatall? Ifprominentnon-convexitiesexist, whyare
theynotproblematicinallsituations? Whyaresomearchitectureseasytotrain,andwhyareresults
sosensitivetotheinitialization? Wewillseethatdifferentarchitectureshaveextremedifferences
in non-convexity structure that answer these questions, and that these differences correlate with
generalizationerror.
| (a)      | ResNet-110,noskipconnections |                                                            |     |     | (b) | DenseNet,121layers |     |     |     |
| -------- | ---------------------------- | ---------------------------------------------------------- | --- | --- | --- | ------------------ | --- | --- | --- |
| Figure4: |                              | ThelosssurfacesofResNet-110-noshortandDenseNetforCIFAR-10. |     |     |     |                    |     |     |     |
6

0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1(.00a)0 8.60 . 9 0 7 .1 R5 00 6.600 e 5 0 .10 . 0 5 3 s0 .100 1 N 9 .10 . 0 60 1 0 0 .6 4 0 . . 2 0 e 1 5 00 0 t .10 - 2 0 0 . . 1 02 0 7 0 0 . 3 1 9 . 0 . 6 6 0 0 0 0 . 0 2 6 0 . 0 0 6 0 0 0 6 , 0 . . 2 7 1 . 0 5 6 0 0 7 0 5 4 8 .6 . . 0 1 6 0 0 . 0 0 0 0 .35070%.75 1.00 0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1( 7.600 . 6 88 7 . . 0 7 1 8 6 8 00 5 7 .. 0. . 9 6 .. 61 01 97 b0 0 .61 0 6 .00 0 .. 0 6 0 61 7 00 00 00 000 . 0 1 000 0 ) 6 0 5 . .1 6 0 0 0 0 0 .7 4.600 6.100 5R 3.6 3 0 . 0 e 6 0 0 . 0 5s0N 5.600 2 0 0 . 6 6 . . 6 . 2 0 761 e 0 0 0 5 ..0 . 0 87 3 1 160 0 .. . 00 9 686 1 0 0 t 0 . 0. 0 0 1 10 0 0 0 0 9 -0 0 0 .6 .0 0 5 1 0 0 7 . 6788 2 1 ..... . 1 0 6616 1 6 0 0 0000 0 00000 0 0, 1 .2 .6 5 00 5 6.60 . 0 0 4 .8 . 4 5 1 . 0 0 6 0 0 5 0 9 .100 0 5 % . . 1 7 0 5 4 5 . 0 6 .0660 5 60. . 17. 1 0 5 60. 0. 1 6 00 0 0 0 0 0 0 1.00 0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 ( 8 1 .6 .c 0 6 0 . 0 1 0 00 ) 9.968 7 8 9 5 . . 9 .6 0 . 6 6 1. . 6 0 . 0 . 6 6 1 0 0 10 0 00 00 00 0 0 R. 0 0 0 0 75 6.10 e 00s.50 4 N 1 . .1 1 00 0 0. 7 0 6 .1 0 0 5 0 0 .1 0e 0 3 . 0 . 2 6 1 . 5 0 6 t 0 0 0 .1 0 - 00 3 01 . . 6 0 0 98778 2 0 0 1 ..... . 1 16161 1 .6 00000 0 0 00000 0 6 0 . 0 1 0 00 .2,5 4.6 2. 0 6 5 0 0 0 0..507 5.6 6 00 5 5. 9 .1 . 6 6 1 5 0 . 0 1 . 0 0 01 0 0 0 0 0 . 0 7% 4 5 67 5 8 . .. . 6 . 16 6 1 0 00 0 5 0 0 0 0 5 0 7 . 65 0 176.6 . .. 60 6 . 61 . 5 .1 .1 1060 0 0 00 0 0000 0 00 00 1 0 .00
( 0 0 0 0 1 1 0 0 0 . . . . . . . . . d 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1).00 9.10 8 R 0 .1 7 0 9. . 6 0 9 0 1 00 8. . 6 0 . 0 6 0 7 0 e 0 5 09.10 s 0 N0 5 . .600 50e 1.600 t0.-25 4 2 .600 3 00 .6 . 2 0 0 . 6 0 0 1 5 0 .10 . . 0 - 6 0 1 0 0 0 99 0 0 . N .16 0. 00 60 00 0 0 2 . . 2 60 S5 0 1.100 3.100 , 4.10 0 0 .580 6. . 100 10.785 7.60 % 0 1.00 (e 0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 ) 0 5 0 5 0 0 5 0 5 1.00R 9 0e .1 .7 00 5sN0 8 .5 5 . .10 6 6 0 e . 0 6 0 0 5 0 0 .10 t 56 0.. 4 61 4 . - 6 0 00 0 . 0 0 1 0 5 . 0 25 . 0 6 2 5 2. 0 6.1 0 0 0 7 00 . 6 1 . 0 6 6 .1 0 0 3 0 0 0 6 0 . 0 1 . . - 6 4 0 1 0 . .6 1 0 0 0 0 0 0 05 5 N 0 . . 6 1 15 1 0 . 0.4 5 1 6 . 0 0. 6 . 6 0 0 5 6 0 0 0 0 0 . 0 0 0 6 S. 0 0 2 0 5, 5 3.6 . 7 0 6 7 0 .6 0 3 .610 . . 0 6 10 060 6 .100 0 . 000 5 0 5 0 3 9 3 . . 1 1 . 0 6 0 0 0 0 5 0 . 4 4 .6. . 0 6 1 0 3 5 8 . 01 . 0 00 4 . 0 1 7 0. 0 0 6 4. 5 0 1 0 00 7 5 . 0 1 1 0 . 0 60 6 0 6..1600 7 % . 0 1 0 6 0 1 .100 0 .00 (f 0 0 0 0 1 1 0 0 0 . . . . . . . . . ) 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1.0R0 e0 5. . 6 s7 00 5N 4 4 . . 6 6 0 0 0 5 0 0 . e 6 . 6 5 . 0 6 0 0 0 6 7 t 0 . . 6 1 6 . 0 - 0 7 1 0 0 0 .1 0 8 0 4 1 0 . . 1 6 . 0 0 2 9 0 5 0 0 . 5 . 1 1 1 2.1 1 0 0 .6 0 0 2 0 0 4 . 0 6 0 . 0 1 0 0 00 0 1 .0 .10. 0 0 - 6 3 00 0 .1 4 6 N 0 . 8 6 . 8.100 0 . 1 0 1 0 0 0 0 0 0 . 7. 3 2 6 . S 0 60 0 0 5 5 9.60. 6 6 . 0 , 6000 5 0 .1 0 0 .1 0 50 6 5. . 6 1 6 0 0 0 9.600 0 6 . . 0 5 10 . . 6 4 0 7 0 5 0 41%.00
Figure5: 2DvisualizationofthelosssurfaceofResNetandResNet-noshortwithdifferentdepth.
Experimental Setup To understand the effects of network architecture on non-convexity, we
trainedanumberofnetworks,andplottedthelandscapearoundtheobtainedminimizersusingthe
filter-normalizedrandomdirectionmethoddescribedinSection4. Weconsiderthreeclassesofneural
networks: 1)ResNets[17]thatareoptimizedforperformanceonCIFAR-10. WeconsiderResNet-
20/56/110,whereeachnameislabeledwiththenumberoflayersithas. 2)“VGG-like”networks
thatdonotcontainshortcut/skipconnections. Weproducedthesenetworkssimplybyremovingthe
shortcutconnectionsfromResNets. WecallthesenetworksResNet-20/56/110-noshort. 3)“Wide”
ResNetsthathavemorefiltersperlayerthantheCIFAR-10optimizednetworks. Allmodelsare
trainedontheCIFAR-10datasetusingSGDwithNesterovmomentum,batch-size128,and0.0005
weightdecayfor300epochs. Thelearningratewasinitializedat0.1,anddecreasedbyafactorof
10atepochs150,225and275. DeeperexperimentalVGG-likenetworks(e.g.,ResNet-56-noshort,
asdescribedbelow)requiredasmallerinitiallearningrateof0.01. Highresolution2Dplotsofthe
minimizersfordifferentneuralnetworksareshowninFigure5andFigure6. Resultsareshown
ascontourplotsratherthansurfaceplotsbecausethismakesitextremelyeasytoseenon-convex
structuresandevaluatesharpness. ForsurfaceplotsofResNet-56,seeFigure1. Notethatthecenter
ofeachplotcorrespondstotheminimizer, andthetwoaxesparameterizetworandomdirections
withfilter-wisenormalizationasin(1). Wemakeseveralobservationsbelowabouthowarchitecture
affectsthelosslandscape.
TheEffectofNetworkDepth FromFigure5,weseethatnetworkdepthhasadramaticeffecton
thelosssurfacesofneuralnetworkswhenskipconnectionsarenotused. ThenetworkResNet-20-
noshorthasafairlybenignlandscapedominatedbyaregionwithconvexcontoursinthecenter,and
nodramaticnon-convexity. Thisisn’ttoosurprising: theoriginalVGGnetworksforImageNethad
19layersandcouldbetrainedeffectively[33]. However,asnetworkdepthincreases,thelosssurface
oftheVGG-likenetsspontaneouslytransitionsfrom(nearly)convextochaotic. ResNet-56-noshort
hasdramaticnon-convexitiesandlargeregionswherethegradientdirections(whicharenormalto
thecontoursdepictedintheplots)donotpointtowardstheminimizeratthecenter. Also,theloss
functionbecomesextremelylargeaswemoveinsomedirections. ResNet-110-noshortdisplayseven
moredramaticnon-convexities,andbecomesextremelysteepaswemoveinalldirectionsshown
intheplot. Furthermore,notethattheminimizersatthecenterofthedeepVGG-likenetsseemto
befairlysharp. InthecaseofResNet-56-noshort,theminimizerisalsofairlyill-conditioned,asthe
contoursneartheminimizerhavesignificanteccentricity.
ShortcutConnectionstotheRescue Shortcutconnectionshaveadramaticeffectofthegeometry
ofthelossfunctions. InFigure5,weseethatresidualconnectionspreventthetransitiontochaotic
behaviorasdepthincreases. Infact,thewidthandshapeofthe0.1-levelcontourisalmostidentical
forthe20-and110-layernetworks. Interestingly,theeffectofskipconnectionsseemstobemost
importantfordeepnetworks. Forthemoreshallownetworks(ResNet-20andResNet-20-noshort),the
effectofskipconnectionsisfairlyunnoticeable. Howeverresidualconnectionspreventtheexplosion
of non-convexity that occurs when networks get deep. This effect seems to apply to other kinds
7

0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1 7.600 . 6 88 7 . . 0 7 1 8 68 00 5 7 .. 0. . 9 6 .. 61 01 97 0 0 .61 0 6 .00 0 .. 0 6 0 61 7 00 00 00 000 . 0 ( 1 000 0 6 0 5 a . .1 6 0 0 0 0 0 .7 4.600 6.100 )5 3.6 3 0 . 0 6 k0 0 . 0 50= 5.600 2 0 0 . 6 6 . . 6 . 2 0 761 0 0 0 5 ..0 . 0 87 3 1 160 0 .. . 00 9 686 1 0 00 . 0. 0 0 1 1 1 0 0 0 0 0 9 0 0 0 .6 .0 0 1 , 0 0 7 . 6788 2 1 ..... . 1 0 6616 1 0 0 0000 0 5 00000 0 0 1 .2 . . 6 5 00 8 6.60 9 0 0 4 . . 4 5 1 . 0 0 6 0 % 0 5 0 .100 0 5. . 1 7 0 5 4 5 . 0 6 .0660 5 60. . 17. 1 0 5 60. 0. 1 6 00 0 0 0 0 0 0 1.00 0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1.0 8.1 5 0 0 .6 0 00 5 5 ( .1 . 0 15 0 0.60 b 0 0 0 7 2. 7 600 . ..61 7 6 00. 0 5) 0160.0 1 6 .6 0 0 0 0 0k.50=0.25 3 0 4. . .6 6 60 0 00 2 0 0 0.00, 0.10 3 5 0 .1 0 0 . 0 2.50 1.100 70.50% 56 .. 11 0 0 3 50 .6 . 0.06 0 7 6 0 . 06 5 0 4 0 .1 2 0 . 0 1 0 00 4.60 4 0 1 .1 . 0 0 0 0 0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1. 5 2 0 . . 6 6 5 0 4 0 0 . 3 0 1 0 2 . .1 6 0 0 . 0 0 3 6 4 0 3 0 .. 0 6 . 1 1 0 ( 0 0 3 0 0 0 . 1 1 . 0 6 0 00 0 c0.7)5 k0.50=0.2 0 5 .100 40.0,040.2.5340 0. . 6 5 00 0% 2.1 0 00 .7 2.6 5 0 1.1 0 0 2 2 0 3 . .1 6 .1 0 0 0 0 00 1.00 0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1 1.100 .0 2 1 . 1 0 . 1 6 . 0 6 0 0 0 0 ( 0 0.600 d0.75) 0k.50=0.2580.00, 0 3 .1 0 0 . 0 2.5930.50%0. 0 7 .600 5 2 1 .1 .6 0 0 2 0 0 1 . .1 6 00 00 1.00
0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1.00(e 9 0 . ) 1 .7 00 5k0 8 .5 5 . .10 6 6 0 . 0 6 0 0 5 0 0 = .1056 0.. 4 61 4 .6 0 00 0 . 0 0 1 0 5 . 0 2 . 0 6 2 5 2. 0 6.1 0 0 1 0 7 00 .1 . 0 6 6 .1 0 0 3 0 0 0 6 0 . 0 , 1 . . 6 4 0 1 0 . .6 1 0 0 0 0 0 0 05 50 1 . . 6 1 15 1 0 . 0.4 5 1 6 . 0 0. 6 . 6 0 0 5 6 0 0 0 0 0 . 3 0 0 06 . 0 0 2 0 5. 5 3.6 . 3 7 0 6 7 0 .6 0 3 .610 . . 0 6 0 060 6 .100 0 . 00 1 0 5 0 5 0 3 9 . . 1 1 . 0 6 00 % 0 0 5 0 4 4 .6. . 0 6 1 0 5 8 . 01 . 0 00 4 . 0 1 7 0. 0 0 6 4. 5 0 1 0 00 7 5 . 0 10 . 0 60 6 0 6..1600 7. 0 1 0 6 0 1 .100 0 .00 0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1.70 5 . . 5 01 6 . ( 1 0 0 0 556 0 6 . 0 0 .. 1 . 66 1 6 f 0 0 .00 01 0 000 0) 0 . 5 5 7 . . 1 6 6 5 0 . 0 0 6 0 0 k 0 0 6 . . 5 10 5 0 0 . 3 6 = . 0 1 0 00 6 0 .6 .2 0 1 3 0 . 5 . 6 6 0 2 0 4 0 0 .10 0, 0 0 2 . 2 0 . . 1 . 1 6 0 0 0 0 3 0 1 0 0 . 56 0 6 5.. . 0 116 6 .6 0 0 0 0.60 00 0 0000 . 0 25. 4 1 . .1 6 00 0 2 0 0 5 5 4 . .6 . . 1 5 1 6 0 0 0 0 0 4 0 0 .6 % 00 4.10 4 0 0 4 . . 6 6 4 . 0 0 0 . 5 7 0 . 1 60 50 0 5 . 0 100 55.61.66.071.0 7 06.0 8.10 68 0 . 0010. 0 600000 1 0 .00 0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1. 6.600 0 7 0 . 6 1 .600 0 ( 0 g0.75) 4 0k .6 . 00 50 1.1 = 00 0.25 1.6 3 0 .6 0 4 0 0 3 0 0 . . . 1 1 0 0 0 0, 0 0 0 2 .6 . 0 1 4 9 0 0 .1 0 0 0 . 0 2.5 2 5 . 6 6 6 . . 0 6 6 0 0 0 5 0 0 .10 90 0 .50 6 % .100 0 7. . 68 7 .01 5 000 7. 6. 1 8 600 0 .69 0 7 0. 7 . .1 1 0 6 0 00 0 1 0 0 .00 0 0 0 0 1 1 0 0 0 . . . . . . . . . 0 2 5 7 0 0 7 5 2 0 5 0 5 0 0 5 0 5 1.0 8 6 0 . . 6 6 0 0 ( 0 0 56..16 h 00 0 00 .75) 8 4 . .10 1 0 00 3.100 0k.5 7 1 0 . .6 6 00 00 5 7 2 5 6 . . = . 1 1 . 1 .60 60 0 0 0 0 00 0 00 .25 6 0 . . 1 1 0 1 0 8 0 .0 0 0 1.06 .0 000 0 2 , .600 80. 3 2. . 5 60 7 0 00. 5 5 .1 0 0 % 50.6060.10 0 0 . 6 4 7 7 . . . 6 1 6 0 0 5 0 0 0 0 1.00
Figure6: Wide-ResNet-56onCIFAR-10bothwithshortcutconnections(top)andwithout(bottom).
Thelabelk =2meanstwiceasmanyfiltersperlayer. Testerrorisreportedbeloweachfigure.
ofskipconnectionsaswell;Figure4showthelosslandscapeofDenseNet[20],whichshowsno
noticeablenon-convexity.
WideModelsvsThinModels Toseetheeffectofthenumberofconvolutionalfiltersperlayer,we
comparethenarrowCIFAR-optimizedResNets(ResNet-56)withWide-ResNets[41]bymultiplying
thenumberoffiltersperlayerbyk =2,4,and8. FromFigure6,weseethatthewidermodelshave
losslandscapeswithnonoticeablechaoticbehavior. Increasednetworkwidthresultedinflatminima
andwideregionsofapparentconvexity. Weseethatincreasedwidthpreventschaoticbehavior,and
skipconnectionsdramaticallywidenminimizers. Finally,notethatsharpnesscorrelatesextremely
wellwithtesterror.
Implications for Network Initialization One interesting property seen in Figure 5 is that loss
landscapes for all the networks considered seem to be partitioned into a well-defined region of
low loss value and convex contours, surrounded by a well-defined region of high loss value and
non-convexcontours. Thispartitioningofchaoticandconvexregionsmayexplaintheimportance
ofgoodinitializationstrategies,andalsotheeasytrainingbehaviorof“good”architectures. When
usingnormalizedrandominitializationstrategiessuchasthoseproposedbyGlorotandBengio[11],
typicalneuralnetworksattainaninitiallossvaluelessthan2.5. Thewellbehavedlosslandscapesin
Figure5(ResNets,andshallowVGG-likenets)aredominatedbylarge,flat,nearlyconvexattractors
thatrisetoalossvalueof4orgreater. Forsuchlandscapes,arandominitializationwilllikelyliein
the“well-behaved”lossregion,andtheoptimizationalgorithmmightnever“see”thepathological
non-convexitiesthatoccuronthehigh-losschaoticplateaus. Chaoticlosslandscapes(ResNet-56/110-
noshort)haveshallowerregionsofconvexitythatrisetolowerlossvalues. Forsufficientlydeep
networkswithshallowenoughattractors,theinitialiteratewilllikelylieinthechaoticregionwhere
thegradientsareuninformative. Inthiscase,thegradients“shatter”[1],andtrainingisimpossible.
SGDwasunabletotraina156layernetworkwithoutskipconnections(evenwithverylowlearning
rates),whichaddsweighttothishypothesis.
LandscapeGeometryAffectsGeneralization BothFigures5and6showthatlandscapegeometry
has a dramatic effect on generalization. First, note that visually flatter minimizers consistently
correspond to lower test error, which further strengthens our assertion that filter normalization
is a natural way to visualize loss function geometry. Second, we notice that chaotic landscapes
(deepnetworkswithoutskipconnections)resultinworsetrainingandtesterror,whilemoreconvex
landscapeshavelowererrorvalues. Infact,themostconvexlandscapes(Wide-ResNetsinthetop
rowofFigure6),generalizethebestofall,andshownonoticeablechaoticbehavior.
A note of caution: Are we really seeing convexity? We are viewing the loss surface under a
dramaticdimensionalityreduction,andweneedtobecarefulhowweinterprettheseplots. Oneway
tomeasurethelevelofconvexityinalossfunctionistocomputetheprinciplecurvatures,whichare
simplyeigenvaluesoftheHessian. Atrulyconvexfunctionhasnon-negativecurvatures(apositive
8

semi-definiteHessian),whileanon-convexfunctionhasnegativecurvatures. Itcanbeshownthatthe
principlecurvaturesofadimensionalityreducedplot(withrandomGaussiandirections)areweighted
averagesoftheprinciplecurvaturesofthefull-dimensionalsurface(wheretheweightsareChi-square
randomvariables).
Thishasseveralconsequences. Firstofall,ifnon-convexityispresentinthedimensionalityreduced
plot,thennon-convexitymustbepresentinthefull-dimensionalsurfaceaswell. However,apparent
convexityinthelow-dimensionalsurfacedoesnotmeanthehigh-dimensionalfunctionistrulyconvex.
Ratheritmeansthatthepositivecurvaturesaredominant(moreformally,themeancurvature,or
averageeigenvalue,ispositive).
Whilethisanalysisisreassuring,onemaystillwonderifthereissignificant“hidden”non-convexity
that these visualizations fail to capture. To answer this question, we calculate the minimum and
maximumeigenvaluesoftheHessian,λ andλ .4Figure7mapstheratio|λ /λ |across
min max min max
thelosssurfacesstudiedabove(usingthesameminimizerandthesamerandomdirections).Bluecolor
indicatesamoreconvexregion(near-zeronegativeeigenvaluesrelativetothepositiveeigenvalues),
whileyellowindicatessignificantlevelsofnegativecurvature. Weseethattheconvex-lookingregions
inoursurfaceplotsdoindeedcorrespondtoregionswithinsignificantnegativeeigenvalues(i.e.,there
arenotmajornon-convexfeaturesthattheplotmissed),whilechaoticregionscontainlargenegative
curvatures. Forconvex-lookingsurfaceslikeDenseNet,thenegativeeigenvaluesremainextremely
small(lessthan1%thesizeofthepositivecurvatures)overalargeregionoftheplot.
0.5 0.5 0.5
0.4 0.4 0.4
0.3 0.3 0.3
0.2 0.2 0.2
0.1 0.1 0.1
0.0 0.0 0.0
(a) Resnet-56 (b) Resnet-56-noshort (c) DenseNet-121
Figure 7: For each point in the filter-normalized surface plots, we calculate the maximum and
minimumeigenvalueoftheHessian,andmaptheratioofthesetwo.
7 VisualizingOptimizationPaths
Finally,weexploremethodsforvisualizingthetrajectoriesofdifferentoptimizers.Forthisapplication,
randomdirectionsareineffective.Wewillprovideatheoreticalexplanationforwhyrandomdirections
fail,andexploremethodsforeffectivelyplottingtrajectoriesontopoflossfunctioncontours.
Severalauthorshaveobservedthatrandomdirectionsfailtocapturethevariationinoptimization
trajectories,including[10,29,28,27]. ExamplefailedvisualizationsaredepictedinFigure8. In
Figure8(a),weseetheiteratesofSGDprojectedontotheplanedefinedbytworandomdirections.
Almostnoneofthemotioniscaptured(noticethesuper-zoomed-inaxesandtheseeminglyrandom
walk). Thisproblemwasnoticedby[13],whothenvisualizedtrajectoriesusingonedirectionthat
pointsfrominitializationtosolution,andonerandomdirection.ThisapproachisshowninFigure8(b).
AsseeninFigure8(c),therandomaxiscapturesalmostnovariation,leadingtothe(misleading)
appearanceofastraightlinepath.
7.1 WhyRandomDirectionsFail: Low-DimensionalOptimizationTrajectories
It is well-known that two random vectors in a high dimensional space will be nearly orthogonal
withhighprobability. Infact,theexpectedcosinesimilaritybetweenGaussianrandomvectorsinn
(cid:112)
dimensionsisroughly 2/(πn)([12],Lemma5).
4WecomputetheseusinganimplicitlyrestartedLanczosmethodthatrequiresonlyHessian-vectorproducts
(whicharecalculateddirectlyusingautomaticdifferentiation),anddoesnotrequireanexplicitrepresentationof
theHessianoritsfactorization.
9

|     |     |     |     |     |     |     |     |     |     |     |     | 9.600 | 9.100 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----- | --- |
9.600
100.000
6.100
100.000
6.100
7.600
10.000
7.600
7.100
6.600
9.100
4.100
8.600
9.600
|     |     |     |     |     |     |     |     |     |     |     |     | 10.000 | 3.100 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | ----- | --- |
5.600
8.100
9.600
6.100
9.100
8.600
2.600
2.100
|     |     |     |     |     |     |     |     |     |     |     |     | 4.100 | 5.100 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----- | --- |
8.100
|     |     |     |     |     |     |     |     |     |     |     |     | 4.600 | 2.600 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----- | --- |
1.600
1.100
5.100
9.100
|     |     |     |     |     |     |     |     |     |     |     |     | 8.100 | 2.100 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----- | --- |
0.600
0.100
0.100
7.600
6.600
|     |     | 0 . 0 0 2 | 0   |     |     | 1 . 0 0 | 7.10 0  |        |     | 7.100 | 1 . 0 0 | 1e3 |     |     |
| --- | --- | --------- | --- | --- | --- | ------- | ------- | ------ | --- | ----- | ------- | --- | --- | --- |
|     |     |           |     |     |     |         | 100.000 | 6 .100 |     |       |         |     |     |     |
|     |     | 0 . 0 0 1 | 5   |     |     | 0 . 7 5 |         | 4.100  |     | 5.100 | 0 . 7 5 |     |     |     |
10.0
|     |     | 0 . 0 0 1 | 0   |     |     | 0 . 5 0 | 00 00                              | 3              | 1 00       | 0 0                                 | 0 . 5 0 |     |     |     |
| --- | --- | --------- | --- | --- | --- | ------- | ---------------------------------- | -------------- | ---------- | ----------------------------------- | ------- | --- | --- | --- |
|     |     |           |     |     |     |         | 1 0 . 0 3 .6                       | .1 0 0         | 5.100 4 .  |                                     |         |     |     |     |
|     |     | 0 . 0 0 0 | 5   |     |     | 0 . 2 5 | 9.690. 0 1 068 00 01 00 6.6005.100 | 2.1            |            |                                     | 0 . 2 5 |     |     |     |
|     |     |           |     |     |     |         | 8 . 7. . 6 0 0 0.1 00              | 00             |            |                                     |         |     |     |     |
|     |     | 0 . 0 0 0 | 0   |     |     | 0 . 0 0 |                                    | 1.6 00         | 2.600      |                                     | 0 . 0 0 |     |     |     |
|     |     |           |     |     |     |         | 0.6 00                             |                |            | 3.600 6.10 0                        |         |     |     |     |
|     |     | 0 . 0 0 0 | 5   |     |     | 0 . 2 5 |                                    | 1.1 00 6.1 0 0 |            | 6.600 7.600 8.100 8.600 9.100 9.600 | 0 . 2 5 |     |     |     |
|     |     |           |     |     |     |         | 2. 6 0                             |                | 3.100      |                                     |         |     |     |     |
|     |     | 0 . 0 0 1 | 0   |     |     | 0 . 5 0 | 4 0                                |                | 7.100 4 .6 |                                     | 0 . 5 0 |     |     |     |
.6 0 0 .60 0 9 . 1 008.600 8.100 00 100.000
|     |     | 0 . 0 0 1 | 5   |     |     | 0 . 7 5 |     | 5   |     |     | 0 . 7 5 |     |     |     |
| --- | --- | --------- | --- | --- | --- | ------- | --- | --- | --- | --- | ------- | --- | --- | --- |
5.60 0
|     |     | 0.0020 |     |     |     | 1.00 |     |     | 7.6000.50 |     | 1.00 |     |     |     |
| --- | --- | ------ | --- | --- | --- | ---- | --- | --- | --------- | --- | ---- | --- | --- | --- |
0.0010 (a) 0.0005 Tworandomdirections 0.0000 0.0005 0.0010 0.0015 0.0020 (b) 0.50 Randomdirectionfory-axis 0.25 0.00 0.25 0.75 1 .00 1.25 1.50 0.50 (c) 0.25 Enlargedversion(b) 0.00 0.25 0.50 0.75 1.00 1.25 1.50
Figure8: Ineffectivevisualizationsofoptimizertrajectories. Thesevisualizationssufferfromthe
orthogonalityofrandomdirectionsinhighdimensions.
Thisisproblematicwhenoptimizationtrajectorieslieinextremelylowdimensionalspaces. Inthis
case,arandomlychosenvectorwilllieorthogonaltothelow-rankspacecontainingtheoptimization
path,andaprojectionontoarandomdirectionwillcapturealmostnovariation. Figure8(b)suggests
thatoptimizationtrajectoriesarelow-dimensionalbecausetherandomdirectioncapturesordersof
magnitudelessvariationthanthevectorthatpointsalongtheoptimizationpath. Below,weusePCA
directionstodirectlyvalidatethislowdimensionality,andalsotoproduceeffectivevisualizations.
7.2 EffectiveTrajectoryPlottingusingPCADirections
Tocapturevariationintrajectories,weneedtousenon-random(andcarefullychosen)directions.
Here,wesuggestanapproachbasedonPCAthatallowsustomeasurehowmuchvariationwe’ve
captured;wealsoprovideplotsofthesetrajectoriesalongthecontoursofthelosssurface.
Letθ denotemodelparametersatepochi,andthefinalparametersafternepochsoftrainingare
i
denotedθ .Givenntrainingepochs,wecanapplyPCAtothematrixM =[θ −θ ;··· ;θ −θ ],
|     |     |     | n   |     |     |     |     |     |     |     |     | 0   | n n−1 n |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- |
and then select the two most explanatory directions. Optimizer trajectories (blue dots) and loss
surfacesalongPCAdirectionsareshowninFigure9. Epochswherethelearningratewasdecreased
areshownasreddots. Oneachaxis,wemeasuretheamountofvariationinthedescentpathcaptured
bythatPCAdirection.
Atearlystagesoftraining,thepathstendtomoveperpendiculartothecontoursofthelosssurface,
i.e.,alongthegradientdirectionsasonewouldexpectfromnon-stochasticgradientdescent. The
stochasticitybecomesfairlypronouncedinseveralplotsduringthelaterstagesoftraining. Thisis
particularlytrueoftheplotsthatuseweightdecayandsmallbatches(whichleadstomoregradient
|     |     | % 40.51 :tnenopmoc ACP dn2 | 7.6007.100 7.600 |                                          | % 33.6 :tnenopmoc ACP dn2 8 223 ... 16 10 00 0 00 | 2.600  |                 |     | % 74.71 :tnenopmoc ACP dn2 | 100.000 |             | 100.000 % 30.31 :tnenopmoc ACP dn2 15 |       |     |
| --- | --- | -------------------------- | ---------------- | ---------------------------------------- | ------------------------------------------------- | ------ | --------------- | --- | -------------------------- | ------- | ----------- | ------------------------------------- | ----- | --- |
|     |     | 20                         | 4.100            | 100.000                                  | 6                                                 |        |                 |     | 20                         |         |             |                                       |       |     |
|     |     |                            | 2.1              | 3 5 .6 6.6 01 .006000                    |                                                   | 1. 1 0 |                 |     |                            | 3.600   | 4.600 6.100 | 1 0                                   |       |     |
|     |     |                            | 0 0              | . 1 0 0 3.600 87..11000099..16000010.000 | 4                                                 | 0      | 3.6004.1005.100 |     | 8.6006.6004.100            |         |             |                                       | 7.600 |     |
10 2.600 1.600 1.100 0. 60 2 0 .6 00 10 3.600 5 2.1001.600 6 .100 .88 9 1.. . 161 9 000. 00600010.000
|     |     |     | 0.100 0 |     |     |     | 2.100 3.100 00 |     |     | 1.100 |     |     | 4. 4 .0605 0.105 7 66 .0 06 00 |     |
| --- | --- | --- | ------- | --- | --- | --- | -------------- | --- | --- | ----- | --- | --- | ------------------------------ | --- |
0 0 0.100 4.600 6.6 7.6008.100 0 0 0 0.600 0 3 2 .3. 61. 0100 00 0. 0 0 0
|     |     |          |            |         |              |     | 5.600 6.100 7.1 0 0 | 8.9 6 . 1 0 .9 0 0.60000 | 0.100 |                       | 1.600 5.1008.100 |     | 0.100 1 .10 0 6 0                  |     |
| --- | --- | -------- | ---------- | ------- | ------------ | --- | ------------------- | ------------------------ | ----- | --------------------- | ---------------- | --- | ---------------------------------- | --- |
|     |     |          |            |         | 2            |     |                     | 1 0                      |       |                       | 10.000           | 5   | 0.60 0                             |     |
|     |     | 10 8.600 | 4.6005.100 |         | 4            |     |                     |                          | 10    | 2.1002.6 0 0 3.10 0   |                  |     |                                    |     |
|     |     |          |            |         | 1 . 6        |     |                     |                          |       | 160000 .10790..660000 | 100.000          | 1 0 |                                    |     |
|     |     | 20       |            | 100.000 | 6 4.100 0 0  |     |                     |                          | 20    | 57 .. 9               |                  |     | 5.140.06340 3..16 .1 000 00 20.600 |     |
|     |     |          |            |         | 85 3 . 6 0 0 |     |                     |                          |       |                       |                  | 15  | 0                                  |     |
5 0 5 10 15 20 25 30 0 5 10 15 20 25 30 35 5 0 5 10 15 20 25 30 0 10 20 30 40
1st PCA component: 24.57 % (a) SGD,WD=5e-4 1st PCA component: 87.78 % 1st PCA component: 32.80 % (b) Adam,WD=5e-4 1st PCA component: 71.74 %
15
% 40.11 :tnenopmoc ACP dn2 3.600 % 27.8 :tnenopmoc ACP dn2 10.0 % 65.9 :tnenopmoc ACP dn2 100 2.600 % 52.9 :tnenopmoc ACP dn2 9.100 9.600
40 5.100 4.6004.100 7.5 3.1003.6004.100 4.600 10 2.100 3 . 1 00 8 8 . . 1 6 0 0 0
|     |     |     |     |     |     |     | 2.100 2.600 |     | 50  |     |     |     | 1.100 6 7 7 . 6 0 0 0 |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --------------------- | --- |
20 5.600 5.0 1.100 0.600 1. 6 0 0 2.6003.6004.1040.60055.1.60 6. 6.10 00 . 1 0 0
|     |     |     |                                             | 6.100           | 2.5                                 | 0.600             |     |                    |       |                                       | 5.100       | 3.100 5 | 0.100 00 0 0               |     |
| --- | --- | --- | ------------------------------------------- | --------------- | ----------------------------------- | ----------------- | --- | ------------------ | ----- | ------------------------------------- | ----------- | ------- | -------------------------- | --- |
|     |     |     | 0.1000.6001.100 1.600 2.1002.600 3.1003.600 | 4.600 6 . 6 0 0 |                                     |                   |     |                    | 0     | 0.1000.6001.100 1.6002.100 3.1003.600 | 4.600 4.100 | 3.600   |                            |     |
|     |     | 0   |                                             | 4.100           | 0 . 0                               | 0.100             |     |                    |       | 2.600 4.1004.600                      |             | 0       |                            |     |
|     |     |     |                                             | 7 . 1 0 0       | 2 . 5                               |                   |     |                    | 50    |                                       |             |         |                            |     |
|     |     | 20  |                                             | 7.600           |                                     |                   |     |                    |       |                                       |             | 5       |                            |     |
|     |     |     |                                             | 8 . 1 0 0       | 5 . 0                               |                   |     |                    | 100   |                                       |             |         |                            |     |
|     |     |     | 0.100                                       | 8 . 6           | 7 . 5                               | 3...0616.1        |     |                    | 0.100 |                                       |             | 10      | 3.6030.1002.621 0.1. 60000 |     |
|     |     | 40  |                                             | 0 0             | 8.71.0760.0165600...66100000005.443 | 1 000000000 1.600 |     | 3.10 3 0 .6004.100 |       |                                       |             |         | 0                          |     |
20 0 20 40 60 80 100 120 140 10.05 0 5 10 15 20 25 15050 0 50 100 150 200 250 300 350 400 1510 0 10 20 30 40 50
1st PCA component: 73.65 % 1st PCA component: 81.87 % 1st PCA component: 77.97 % 1st PCA component: 80.31 %
|     |     |     |     | (c) SGD,WD=0 |     |     |     |     |     |     | (d) | Adam,WD=0 |     |     |
| --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- |
Figure9: ProjectedlearningtrajectoriesusenormalizedPCAdirectionsforVGG-9. Theleftplotin
eachsubfigureusesbatchsize128,andtherightoneusesbatchsize8192.
10
|     |     |     |     |     |     |     |     |     |     |     |     |     | 1.600 2.600 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- |
0.600
5.600
|     |     |     |     |     |     |     |     |     |     |     |     | 1.100 | 5.100 8.100 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----------- | --- |
8.600
3.600 7.100
4.600
| 3.600 | 3.100 |     |     |     |     |     |     |     |     |     |     |     |     | 5.600 |
| ----- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
5.100
4.100
3.100
8.600
9.100 9.600
9.600
9.100
8.600
6.600
7.100
7.600
8.100
3.600
7.600
7.100
4.600
8.600
8.100
6.100
9.100
100.000
8.600
7.100
|     |     |     |     |     |     |     |     |     |     |     |     | 100.000 | 9.600 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | ----- | --- |
6.600

noise,andamoreradicaldeparturefromdeterministicgradientdirections). Whenweightdecayand
smallbatchesareused,weseethepathturnnearlyparalleltothecontoursand“orbit”thesolution
whenthestepsizeislarge. Whenthestepsizeisdropped(atthereddot),theeffectivenoiseinthe
systemdecreases,andweseeakinkinthepathasthetrajectoryfallsintothenearestlocalminimizer.
Finally,wecandirectlyobservethatthedescentpathisverylowdimensional: between40%and
90%ofthevariationinthedescentpathsliesinaspaceofonly2dimensions. Theoptimization
trajectoriesinFigure9appeartobedominatedbymovementinthedirectionofanearbyattractor.
ThislowdimensionalityiscompatiblewiththeobservationsinSection6,whereweobservedthat
non-chaoticlandscapesaredominatedbywide,nearlyconvexminimizers.
8 Conclusion
Wepresentedavisualizationtechniquethatprovidesinsightsintotheconsequencesofavarietyof
choicesfacingtheneuralnetworkpractitioner,includingnetworkarchitecture,optimizerselection,
andbatchsize. Neuralnetworkshaveadvanceddramaticallyinrecentyears,largelyonthebackof
anecdotalknowledgeandtheoreticalresultswithcomplexassumptions. Forprogresstocontinue
tobemade,amoregeneralunderstandingofthestructureofneuralnetworksisneeded. Ourhope
isthateffectivevisualization,whencoupledwithcontinuedadvancesintheory,canresultinfaster
training,simplermodels,andbettergeneralization.
Acknowledgements
Li,Xu,andGoldsteinweresupportedbytheOfficeofNavalResearch(N00014-17-1-2078),DARPA
LifelongLearningMachines(FA8650-18-2-7833),theDARPAYFAprogram(D18AP00055),and
theSloanFoundation. TaylorwassupportedbytheONR(N0001418WX01582),andtheDODHPC
ModernizationProgram. StuderwassupportedinpartbyXilinx,Inc. andbytheUSNationalScience
Foundation(NSF)undergrantsECCS-1408006,CCF-1535897,CCF-1652065,CNS-1717559,and
ECCS-1824379.
References
[1] DavidBalduzzi,MarcusFrean,LennoxLeary,JPLewis,KurtWan-DuoMa,andBrianMcWilliams. The
shatteredgradientsproblem:Ifresnetsaretheanswer,thenwhatisthequestion? InICML,2017.
[2] AvrimBlumandRonaldLRivest. Traininga3-nodeneuralnetworkisnp-complete. InNIPS,1989.
[3] PratikChaudhari,AnnaChoromanska,StefanoSoatto,andYannLeCun. Entropy-sgd:Biasinggradient
descentintowidevalleys. InICLR,2017.
[4] AnnaChoromanska,MikaelHenaff,MichaelMathieu,GérardBenArous,andYannLeCun. Theloss
surfacesofmultilayernetworks. InAISTATS,2015.
[5] YannNDauphin,RazvanPascanu,CaglarGulcehre,KyunghyunCho,SuryaGanguli,andYoshuaBengio.
Identifyingandattackingthesaddlepointprobleminhigh-dimensionalnon-convexoptimization. InNIPS,
2014.
[6] SohamDe,AbhayYadav,DavidJacobs,andTomGoldstein. Automatedinferencewithadaptivebatches.
InAISTATS,2017.
[7] LaurentDinh,RazvanPascanu,SamyBengio,andYoshuaBengio. Sharpminimacangeneralizefordeep
nets. InICML,2017.
[8] GintareKarolinaDziugaiteandDanielMRoy. Computingnonvacuousgeneralizationboundsfordeep
(stochastic)neuralnetworkswithmanymoreparametersthantrainingdata. InUAI,2017.
[9] CDanielFreemanandJoanBruna. Topologyandgeometryofhalf-rectifiednetworkoptimization. In
ICLR,2017.
[10] MarcusGallagherandTomDowns. Visualizationoflearninginmultilayerperceptronnetworksusing
principalcomponentanalysis. IEEETransactionsonSystems,Man,andCybernetics,PartB(Cybernetics),
33(1):28–34,2003.
11

[11] Xavier Glorot and Yoshua Bengio. Understanding the difficulty of training deep feedforward neural
networks. InAISTATS,2010.
[12] TomGoldsteinandChristophStuder. Phasemax:Convexphaseretrievalviabasispursuit. arXivpreprint
arXiv:1610.07531,2016.
[13] Ian J Goodfellow, Oriol Vinyals, and Andrew M Saxe. Qualitatively characterizing neural network
optimizationproblems. InICLR,2015.
[14] PriyaGoyal,PiotrDollár,RossGirshick,PieterNoordhuis,LukaszWesolowski,AapoKyrola,Andrew
Tulloch,YangqingJia,andKaimingHe.Accurate,largeminibatchsgd:Trainingimagenetin1hour.arXiv
preprintarXiv:1706.02677,2017.
[15] BenjaminDHaeffeleandRenéVidal. Globaloptimalityinneuralnetworktraining. InCVPR,2017.
[16] MoritzHardtandTengyuMa. Identitymattersindeeplearning. InICLR,2017.
[17] KaimingHe,XiangyuZhang,ShaoqingRen,andJianSun.DeepResidualLearningforImageRecognition.
InCVPR,2016.
[18] SeppHochreiterandJürgenSchmidhuber. Flatminima. NeuralComputation,9(1):1–42,1997.
[19] EladHoffer,ItayHubara,andDanielSoudry. Trainlonger,generalizebetter:closingthegeneralization
gapinlargebatchtrainingofneuralnetworks. NIPS,2017.
[20] GaoHuang,ZhuangLiu,KilianQWeinberger,andLaurensvanderMaaten. Denselyconnectedconvolu-
tionalnetworks. InCVPR,2017.
[21] DanielJiwoongIm,MichaelTao,andKristinBranson.Anempiricalanalysisofdeepnetworklosssurfaces.
arXivpreprintarXiv:1612.04010,2016.
[22] Sergey Ioffe and Christian Szegedy. Batch Normalization: Accelerating Deep Network Training by
ReducingInternalCovariateShift. InICML,2015.
[23] KenjiKawaguchi,LesliePackKaelbling,andYoshuaBengio. Generalizationindeeplearning. arXiv
preprintarXiv:1710.05468,2017.
[24] NitishShirishKeskar,DheevatsaMudigere,JorgeNocedal,MikhailSmelyanskiy,andPingTakPeterTang.
Onlarge-batchtrainingfordeeplearning:Generalizationgapandsharpminima. InICLR,2017.
[25] AndersKroghandJohnAHertz. Asimpleweightdecaycanimprovegeneralization. InNIPS,1992.
[26] YuanzhiLiandYangYuan. Convergenceanalysisoftwo-layerneuralnetworkswithreluactivation. arXiv
preprintarXiv:1705.09886,2017.
[27] QianliLiaoandTomasoPoggio. Theoryofdeeplearningii: Landscapeoftheempiricalriskindeep
learning. arXivpreprintarXiv:1703.09833,2017.
[28] ZacharyCLipton. Stuckinawhat?adventuresinweightspace. InICLRWorkshop,2016.
[29] ElianaLorch. Visualizingdeepnetworktrainingtrajectorieswithpca. InICMLWorkshoponVisualization
forDeepLearning,2016.
[30] BehnamNeyshabur,SrinadhBhojanapalli,DavidMcAllester,andNatiSrebro. Exploringgeneralizationin
deeplearning. InNIPS,2017.
[31] QuynhNguyenandMatthiasHein. Thelosssurfaceofdeepandwideneuralnetworks. InICML,2017.
[32] ItaySafranandOhadShamir. Onthequalityoftheinitialbasininoverspecifiedneuralnetworks. InICML,
2016.
[33] KarenSimonyanandAndrewZisserman. VeryDeepConvolutionalNetworksforLarge-ScaleImage
Recognition. InICLR,2015.
[34] LeslieNSmithandNicholayTopin. Exploringlossfunctiontopologywithcyclicallearningrates. arXiv
preprintarXiv:1702.04283,2017.
[35] Mahdi Soltanolkotabi, Adel Javanmard, and Jason D Lee. Theoretical insights into the optimization
landscapeofover-parameterizedshallowneuralnetworks. arXivpreprintarXiv:1707.04926,2017.
12

[36] DanielSoudryandEladHoffer. Exponentiallyvanishingsub-optimallocalminimainmultilayerneural
networks. arXivpreprintarXiv:1702.05777,2017.
[37] GrzegorzSwirszcz,WojciechMarianCzarnecki,andRazvanPascanu. Localminimaintrainingofdeep
networks. arXivpreprintarXiv:1611.06310,2016.
[38] Yuandong Tian. An analytical formula of population gradient for two-layered relu network and its
applicationsinconvergenceandcriticalpointanalysis. InICML,2017.
[39] BoXie,YingyuLiang,andLeSong. Diverseneuralnetworklearnstruetargetfunctions. InAISTATS,
2017.
[40] ChulheeYun,SuvritSra,andAliJadbabaie. Globaloptimalityconditionsfordeepneuralnetworks. In
ICLR,2017.
[41] SergeyZagoruykoandNikosKomodakis. Wideresidualnetworks. InBMVC,2016.
[42] ChiyuanZhang,SamyBengio,MoritzHardt,BenjaminRecht,andOriolVinyals. Understandingdeep
learningrequiresrethinkinggeneralization. InICLR,2017.
13

|     | Visualizing |     | the Loss | Landscape |     | of Neural | Nets |     |
| --- | ----------- | --- | -------- | --------- | --- | --------- | ---- | --- |
A ComparisonofLossSurfaces
A.1 TheChangeofWeightsNormduringTraining
Figure10showsthechangeofweightsnormduringtrainingintermsofepochsanditerations.
| 160 |        | 60  |     | bs=128 | 400 |             | 60  | bs=128 |
| --- | ------ | --- | --- | ------ | --- | ----------- | --- | ------ |
|     | bs=128 | 55  |     |        |     | b s = 1 2 8 | 55  |        |
sthgiew fo mron-2L 140 bs=8192 sthgiew fo mron-2L bs=8192 sthgiew fo mron-2L 350 b s = 8 1 92 sthgiew fo mron-2L bs=8192
|     |     | 50  |            |         |        |     | 50   |                        |
| --- | --- | --- | ---------- | ------- | ------ | --- | ---- | ---------------------- |
|     |     | 45  |            |         | 300    |     | 45   |                        |
| 120 |     |     |            |         | 250    |     |      |                        |
|     |     | 40  |            |         |        |     | 40   |                        |
| 100 |     |     |            |         | 200    |     | 35   |                        |
|     |     | 35  |            |         | 150    |     |      |                        |
| 80  |     | 30  |            |         |        |     | 30   |                        |
|     |     |     |            |         | 100    |     | 25   |                        |
| 60  |     | 25  |            |         |        |     |      |                        |
|     |     | 0   | 50 100 150 | 200 250 | 300 50 |     | 20 0 | 50 100 150 200 250 300 |
0 50 100 Epochs 150 200 250 300 Epochs 0 50 100 Epochs 150 200 250 300 Epochs
(a) SGD,WD=0,epoch (b) SGD,WD=5e-4,epoch (c) Adam,WD=0,epoch (d) Adam,WD=5e-4,epoch
| 160                    |         | 60                 |     | bs=128  | 400                    |              | 60                 | bs=128  |
| ---------------------- | ------- | ------------------ | --- | ------- | ---------------------- | ------------ | ------------------ | ------- |
|                        | bs=128  | 55                 |     | bs=8192 |                        | b s = 1 2 8  | 55                 | bs=8192 |
| sthgiew fo mron-2L 140 | bs=8192 | sthgiew fo mron-2L |     |         | sthgiew fo mron-2L 350 | b s = 8 1 92 | sthgiew fo mron-2L |         |
|                        |         | 50                 |     |         |                        |              | 50                 |         |
| 120                    |         | 45                 |     |         | 300                    |              | 45                 |         |
250
|     |     | 40  |     |     |     |     | 40  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 |     |     |     |     | 200 |     | 35  |     |
|     |     | 35  |     |     | 150 |     |     |     |
| 80  |     | 30  |     |     |     |     | 30  |     |
|     |     |     |     |     | 100 |     | 25  |     |
| 60  |     | 25  |     |     |     |     |     |     |
0.0 0.2 0.4 0.6 0.8 1.0 1.2 0.0 0.2 0.4 0.6 0.8 1.0 1.2 50 0.0 0.2 0.4 0.6 0.8 1.0 1.2 20 0.0 0.2 0.4 0.6 0.8 1.0 1.2
|     | Iterations | 1e5 | Iterations |     | 1e5 | Iterations | 1e5 | Iterations 1e5 |
| --- | ---------- | --- | ---------- | --- | --- | ---------- | --- | -------------- |
(e) SGD,WD=0,iter (f) SGD,WD=5e-4,iter (g) Adam,WD=0,iter (h) Adam,WD=5e-4,iter
Figure10: ThechangeofweightsnormduringtrainingforVGG-9. Whenweightdecayisdisabled,
theweightnormgrowssteadilyduringtrainingwithoutconstraints. Whennonzeroweightdecayis
adopted,theweightnormdecreasesrapidlyatthebeginningandbecomesstableuntilthelearning
rateisdecayed. Sinceweuseafixednumberofepochsfordifferentbatchsizes,thedifferencein
weightnormchangebetweenlarge-batchandsmall-batchtrainingismainlycausedbythelarger
numberofupdateswhenasmallbatchisused. Asshowninthesecondrow,thechangesofweight
normareatthesamepaceforbothsmallandlargebatchtrainingintermsofiterations.
A.2 ComparisionofNormalizationMethods
Herewecompareseveralnormalizationmethodsforagivenrandomnormaldirectiond. Letθ denotethe
i
| weightsoflayeriandθ |     | representthej-thfilterinthei-thlayer. |     |     |     |     |     |     |
| ------------------- | --- | ------------------------------------- | --- | --- | --- | --- | --- | --- |
i,j
• NoNormalizationInthiscase,thedirectiondisaddedtotheweightsdirectlywithoutprocessing.
• FilterNormalizationThedirectiondisnormalizedsothatthedirectionforeachfilterhasthesame
normasthecorrespondingfilterinθ,
d
|     |     |     |     | d   | ← i,j      | (cid:107)θ (cid:107). |     |     |
| --- | --- | --- | --- | --- | ---------- | --------------------- | --- | --- |
|     |     |     |     | i,j | (cid:107)d | (cid:107) i,j         |     |     |
i,j
Thisistheapproachadvocatedinthisarticle,andisusedextensivelyforplottinglosssurfaces.
• LayerNormalizationThedirectiondisnormalizedinthelayerlevelsothatthedirectionforeach
layerhasthesamenormasthecorrespondinglayerofθ,
d
|     |     |     |     |     | d ← i                  | (cid:107)θ (cid:107). |     |     |
| --- | --- | --- | --- | --- | ---------------------- | --------------------- | --- | --- |
|     |     |     |     |     | i (cid:107)d (cid:107) | i                     |     |     |
i
Figure11showsthe1Dplotswithoutnormalization.Oneissuewiththenon-normalizedplotsisthatthex-axis
rangemustbechosencarefully. Figure12showsenlargedplotswith[−0.2,0.2]astherangeforthex-axis.
Withoutnormalization,theplotsfailtoshowconsistencybetweenflatnessandgeneralizationerror.Herewe
comparefilternormalizationwithlayernormalization.Wefindfilternormalizationismoreaccuratethanlayer
normalization.OnefailingcaseforlayernormalizationisshowninFigure13,whereFigure13(g)isflatterthan
Figure13(c),butwithworsegeneralizationerror.
14

| 5    | 100 5         | 100 5         | 100 5         | 100         |
| ---- | ------------- | ------------- | ------------- | ----------- |
| 4    | 80 4          | 80 4          | 80 4          | 80          |
| 3    | 60 ycaruccA 3 | 60 ycaruccA 3 | 60 ycaruccA 3 | 60 ycaruccA |
| ssoL | ssoL          | ssoL          | ssoL          |             |
| 2    | 40 2          | 40 2          | 40 2          | 40          |
| 1    | 20 1          | 20 1          | 20 1          | 20          |
01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0
(a) SGD,128,7.37% (b) SGD,8192,11.07% (c) Adam,128,7.44% (d) Adam,8192,10.91%
| 5   | 100 5 | 100 5 | 100 5 | 100 |
| --- | ----- | ----- | ----- | --- |
| 4   | 80 4  | 80 4  | 80 4  | 80  |
ssoL 3 60 ycaruccA ssoL 3 60 ycaruccA ssoL 3 60 ycaruccA ssoL 3 60 ycaruccA
| 2   | 40 2 | 40 2 | 40 2 | 40  |
| --- | ---- | ---- | ---- | --- |
| 1   | 20 1 | 20 1 | 20 1 | 20  |
01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0
(e) SGD,128,6.00% (f) SGD,8192,10.19% (g) Adam,128,7.80% (h) Adam,8192,9.52%
Figure11: 1DlossplotsforVGG-9withoutnormalization. Thefirstrowhasnoweightdecayand
thesecondrowusesweightdecay0.0005.
| 5      | 100 5     | 100 5     | 100 5     | 100      |
| ------ | --------- | --------- | --------- | -------- |
| 4      | 80 4      | 80 4      | 80 4      | 80       |
|        | ycaruccA  | ycaruccA  | ycaruccA  | ycaruccA |
| ssoL 3 | 60 ssoL 3 | 60 ssoL 3 | 60 ssoL 3 | 60       |
| 2      | 40 2      | 40 2      | 40 2      | 40       |
| 1      | 20 1      | 20 1      | 20 1      | 20       |
00.200.150.100.050.000.050.100.150.20 0 00.200.150.100.050.000.050.100.150.20 0 00.200.150.100.050.000.050.100.150.20 0 00.200.150.100.050.000.050.100.150.20 0
(a) SGD,128,7.37% (b) SGD,8192,11.07% (c) Adam,128,7.44% (d) Adam,8192,10.91%
| 5    | 100 5         | 100 5         | 100 5         | 100         |
| ---- | ------------- | ------------- | ------------- | ----------- |
| 4    | 80 4          | 80 4          | 80 4          | 80          |
| 3    | 60 ycaruccA 3 | 60 ycaruccA 3 | 60 ycaruccA 3 | 60 ycaruccA |
| ssoL | ssoL          | ssoL          | ssoL          |             |
| 2    | 40 2          | 40 2          | 40 2          | 40          |
| 1    | 20 1          | 20 1          | 20 1          | 20          |
00.200.150.100.050.000.050.100.150.20 0 00.200.150.100.050.000.050.100.150.20 0 00.200.150.100.050.000.050.100.150.20 0 00.200.150.100.050.000.050.100.150.20 0
(e) SGD,128,6.00% (f) SGD,8192,10.19% (g) Adam,128,7.80% (h) Adam,8192,9.52%
Figure12: EnlargedFigure11. Therangeofthex-axisis[-0.2,0.2]insteadof[-1.0,1.0. Thefirst
rowhasnoweightdecayandthesecondrowusesweightdecay0.0005. Thepairs(a,e)and(c,g)
showthatsharpnessofminimadoesnotcorrelatewellwithtesterror.
| 5    | 100 5         | 100 5         | 100 5         | 100         |
| ---- | ------------- | ------------- | ------------- | ----------- |
| 4    | 80 4          | 80 4          | 80 4          | 80          |
| 3    | 60 ycaruccA 3 | 60 ycaruccA 3 | 60 ycaruccA 3 | 60 ycaruccA |
| ssoL | ssoL          | ssoL          | ssoL          |             |
| 2    | 40 2          | 40 2          | 40 2          | 40          |
| 1    | 20 1          | 20 1          | 20 1          | 20          |
01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0
(a) SGD,128,7.37% (b) SGD,8192,11.07% (c) Adam,128,7.44% (d) Adam,8192,10.91%
| 5      | 100 5     | 100 5     | 100 5     | 100      |
| ------ | --------- | --------- | --------- | -------- |
| 4      | 80 4      | 80 4      | 80 4      | 80       |
|        | ycaruccA  | ycaruccA  | ycaruccA  | ycaruccA |
| ssoL 3 | 60 ssoL 3 | 60 ssoL 3 | 60 ssoL 3 | 60       |
| 2      | 40 2      | 40 2      | 40 2      | 40       |
| 1      | 20 1      | 20 1      | 20 1      | 20       |
01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0
(e) SGD,128,6.00% (f) SGD,8192,10.19% (g) Adam,128,7.80% (h) Adam,8192,9.52%
Figure13: 1DlossplotsforVGG-9withlayernormalization. Thefirstrowhasnoweightdecayand
thesecondrowusesweightdecay5e-4.
15

A.3 Small-BatchvsLarge-BatchforResNet-56
SimilartotheobservationsmadeinSection5,the“sharpvsflatdilemma"alsoappliestoResNet-56asshownin
Figure14.ThegeneralizationerrorforeachsolutionisshowninTable1.The1Dand2Dvisualizationswith
filternormalizeddirectionsareshowninFigure15.
Table1: TesterrorsforResNet-56withdifferentoptimizer,batch-sizeandweight-decay.
|      |     |     |               |        | SGD         |      | Adam   |         |            |     |             |
| ---- | --- | --- | ------------- | ------ | ----------- | ---- | ------ | ------- | ---------- | --- | ----------- |
|      |     |     |               | bs=128 | bs=4096     |      | bs=128 | bs=4096 |            |     |             |
|      |     |     | WD=0          | 8.26   | 13.93       |      | 9.55   | 14.30   |            |     |             |
|      |     |     | WD=5e-4       | 5.89   | 10.59       |      | 7.67   | 12.36   |            |     |             |
| 5    |     |     | 100 5         |        | 100         | 5    |        | 100     | 5          |     | 100         |
| 4    |     |     | 80 4          |        | 80          | 4    |        | 80      | 4          |     | 80          |
| 3    |     |     | 60 ycaruccA 3 |        | 60 ycaruccA | 3    |        | 60      | ycaruccA 3 |     | 60 ycaruccA |
| ssoL |     |     | ssoL          |        |             | ssoL |        |         | ssoL       |     |             |
| 2    |     |     | 40 2          |        | 40          | 2    |        | 40      | 2          |     | 40          |
| 1    |     |     | 20 1          |        | 20          | 1    |        | 20      | 1          |     | 20          |
00.500.250.000.250.500.751.001.251.50 0 00.500.250.000.250.500.751.001.251.50 0 00.500.250.000.250.500.751.001.251.50 0 00.500.250.000.250.500.751.001.251.50 0
| (a) | SGD,WD=0 |     | (b) | SGD,WD=5e-4 |     | (c) | Adam,WD=0 |     | (d) | Adam,WD=5e-4 |     |
| --- | -------- | --- | --- | ----------- | --- | --- | --------- | --- | --- | ------------ | --- |
Figure14: 1Dlinearinterpolationofsolutionsobtainedbysmall-batchandlarge-batchmethodsfor
| ResNet-56. | Thebluelinesarelossvaluesandtheredlinesareerror. |     |           |     |          |        |     |     |          |     |          |
| ---------- | ------------------------------------------------ | --- | --------- | --- | -------- | ------ | --- | --- | -------- | --- | -------- |
| 5          |                                                  |     | 100 5     |     | 100      | 5      |     | 100 | 5        |     | 100      |
| 4          |                                                  |     | 80 4      |     | 80       | 4      |     | 80  | 4        |     | 80       |
|            |                                                  |     | ycaruccA  |     | ycaruccA |        |     |     | ycaruccA |     | ycaruccA |
| ssoL 3     |                                                  |     | 60 ssoL 3 |     | 60       | ssoL 3 |     | 60  | ssoL 3   |     | 60       |
| 2          |                                                  |     | 40 2      |     | 40       | 2      |     | 40  | 2        |     | 40       |
| 1          |                                                  |     | 20 1      |     | 20       | 1      |     | 20  | 1        |     | 20       |
01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0
(a) SGD,128,8.26% (b) SGD,4096,13.93% (c) Adam,128,9.55% (d) Adam,4096,14.30%
| 5      |     |     | 100 5     |     | 100      | 5      |     | 100 | 5        |     | 100      |
| ------ | --- | --- | --------- | --- | -------- | ------ | --- | --- | -------- | --- | -------- |
| 4      |     |     | 80 4      |     | 80       | 4      |     | 80  | 4        |     | 80       |
|        |     |     | ycaruccA  |     | ycaruccA |        |     |     | ycaruccA |     | ycaruccA |
| ssoL 3 |     |     | 60 ssoL 3 |     | 60       | ssoL 3 |     | 60  | ssoL 3   |     | 60       |
| 2      |     |     | 40 2      |     | 40       | 2      |     | 40  | 2        |     | 40       |
| 1      |     |     | 20 1      |     | 20       | 1      |     | 20  | 1        |     | 20       |
01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0
(e) SGD,128,5.89% (f) SGD,4096,10.59% (g) Adam,128,7.67% (h) Adam,4096,12.36%
| 1.00    |                                 |               | 1.00    |     |     | 1.00    |     |     | 1.00    |     |     |
| ------- | ------------------------------- | ------------- | ------- | --- | --- | ------- | --- | --- | ------- | --- | --- |
| 0 . 7 5 |                                 |               | 0 . 7 5 |     |     | 0 . 7 5 |     |     | 0 . 7 5 |     |     |
|         | 8 .1 0 0 7. 66 .07 1 0. 01 00 0 |               |         |     |     |         |     |     |         |     |     |
| 0 . 5 0 | 45                              | ..6 1 00 00 3 | 0 . 5 0 |     |     | 0 . 5 0 |     |     | 0 . 5 0 |     |     |
0 . 2 5 . 62 0 .60 8.600 0 . 2 5 9 0 . 2 5 9 9. 1.8 60. 060 00 0 0 . 2 5 6 . 6 0 0
|     | 0 . 1 0 0 | 00  |     | 8.100 5.6. 310 00 0 3 .600.60 20 . 011 0..66 0100.10000 . 1 0 0 |     |     | 1 .1 0 0 0 . 1 0 0 5 .100 |     |     | 8.600 3 . 446 ..0116 0.002600.002 10.. 0166 .0001 000 7 . 60 |     |
| --- | --------- | --- | --- | --------------------------------------------------------------- | --- | --- | ------------------------- | --- | --- | ------------------------------------------------------------ | --- |
0 . 0 0 5.600 1.600 0 . 0 0 5 .1 0 02 0 . 0 0 4.1450.0.660000 0.6 00 0 . 0 0 0 0
|     | 2   | 1 . 1 0 0 6.600 |     | 9 .6 0 0 44 .. 16 00 00 76..11 6.6 0 0070 .0608 0 .0600 |     |     | 6 1 0 0 2 3.63.10.60000 0 |     |     | 3 . 1 0 0 5 57. 1 .. 6 0 6 00 . 01 0 0 |     |
| --- | --- | --------------- | --- | ------------------------------------------------------- | --- | --- | ------------------------- | --- | --- | -------------------------------------- | --- |
0 . 2 5 .1 0 0 0 . 6 0 0 1 0 0 0 . 2 5 0 . 2 5 .1 60 .8706 ..0167000.1 000 1 0 . 6 00 2 . 0 . 2 5 8 . 1 0 0 1 0 0 9 .6 0 0
0 . 5 0 3 . 1 0 0 4 . 9 . 96 .0 1 0 0 0 0 . 5 0 0 . 5 0 0 . 5 0 9 . 1 0 0
| 0.75                                                 |                                |        | 0.75                                               |     |      | 0.75         |                                       |      | 0.75                 |                                      |     |
| ---------------------------------------------------- | ------------------------------ | ------ | -------------------------------------------------- | --- | ---- | ------------ | ------------------------------------- | ---- | -------------------- | ------------------------------------ | --- |
| 1.001.0(0i)0.75SG0.50D0,.25102.008,0.285.20.506%0.75 |                                |        | 1.0 01j.00)                                        |     |      | 1.00         |                                       |      | 1. 00                |                                      |     |
|                                                      |                                |        | 1.00 ( S0.75G0D.50,04.25009.006,0.21530..50930.7%5 |     | 1.00 | (1.0k0)0.7A5 | d0.5a0m0.25,10.02080.,2590..55050%.75 | 1.00 | ( l1.)00A0.75da0.m50 | ,0.24500.09060,.25140.50.300.75%1.00 |     |
| 1 . 0 0 7 8 8 7 0. .. 01 .61 6 0 0 0 00 00 0         | 3 . 6 0 0 5.600 9 . 1 0 9 0 .6 | 5 .100 | 5 .0660 60. 17. 0 60. 1 00 0 0 0 1 . 0 0           |     |      | 1 . 0 0      |                                       |      | 1 . 0 0              |                                      |     |
0 . 7 5 6 . 6 0 0 6.60 0 4 . 6 0 . 7 5 0 . 7 5 9 . 1 0 0 0 . 7 5 6 .6 0 0
|     | 6 . 761 ..0 87 160 .. 00 686 00 0. 0 10 0 0 0 0 |     |     | 0 0 4 . 6 0 0 | 4 . 1 0 0 |     | 9.1 9 . 6 0 0 0 6 . 1 0 0 9 . 6 0 0 |     |     | 6 . 1 0 0 3 . 1 00 5 . 1 0 0 |     |
| --- | ----------------------------------------------- | --- | --- | ------------- | --------- | --- | ----------------------------------- | --- | --- | ---------------------------- | --- |
0 . 5 0 5 . 6 3 . 1 0 2 . 1 0 0 4 . 6 0 0 5 . 1 0 0 0 . 5 0 1 0 0 5.1 0 . 5 0 0 0 7 . 6 0 4 . 6 0 0 . 5 0 .190. 100 0 8 9. 6 . 910 0.06 8 0 0 .1 00 0
0 . 2 5 0 0 5 .1 0 0 0 0 . 2 5 9. 6 .76.0710.06 00 0 . 2 5 0 8.6 00 0 . 2 5 8 0 7 .60
7.600 7 . 1 00 0 . 1 0 .100 . 60 0 0 . 1 0 0 3.600 0 7.10 0 .10 0 2 . 1 0 0 0 . 1 0 0 2.6 3 . 6 00 1 . 26 0. 60 0 0 .1 6 . 0 1 0 0 0 0 5. 6 0 0
0 . 0 0 4.600 0 . 0 0 5 . 6 00 3 0 6 0 0 0 . 0 0 3 0 . 6 00 00 6.6 00 0 . 0 0 4 . 10 0 2 . 1 6 . 10
0 . 2 5 3.6 0 0 . 2 5 4 . 1 1 . 1 0 0 1 . 62 0. 100 0 2 . 6 . 1 0 . 2 5 5 .6 00 1 .1 0 1 . 6 0 0 0 . 2 5 5.6 0 0 3 . 1 0 0 1 0 0 7 . 6 7 0. 01 0 0 0
0 0 . 6 0 0 1 0 0 1 .6 00 1 0 0 0 0 0 0 8 4 . 13 0 . 6 0 0 0 0 5 . 1 0 0 4 0 0 4 . 6 . 6
0 . 5 0 6 . 6 2 . 6 0 0 1 . 4 . 0 . 5 0 7 .6 00 8 .6 0 0 0 . 5 0 . 1 0 0 7 . 1 0 0 0 . 5 0 9 . 6 8 . 6 . 0 0 8 . 1 08 0. 6 0 7 0 . 6 0 0 0 0
0 . 7 5 7 0 0 6.100 0 . 7 5 9 . 6 0 0 00 8 .1 0 . 7 5 0 . 7 5 0 6 0 0 0 7 .6 07 0 . 1 0 0
| 88 .. 9 61 97 .00 .. 6 61 00 000 . 1 000 0 0 | 7 6788 ..... 1 6616 | 0 0000 00000 | 5 . 1 5 0. 6 0 0 0 |     |     |         |     |     |         |     |     |
| -------------------------------------------- | ------------------- | ------------ | ------------------ | --- | --- | ------- | --- | --- | ------- | --- | --- |
| 1 . 0 0                                      |                     |              | 1 . 0 0            |     |     | 1 . 0 0 |     |     | 1 . 0 0 |     |     |
1( . 0 m0 0) .7 5S 0 G. 50D 0 . 2 , 5 1 0 .0 2 0 8 0, .2 5 5 . 0 .8 5 0 9 0 % . 7 5 1.00 ( 1n.00)0S.75G 0 . D5 0 , 0 . 42 5 0 0 .90 0 6 ,0 . 2 5 1 0 0 . 5. 0 5 9 0 . 7 %5 1.00 (1.0o0)0.7A5 d 0 . 5 a0m 0 . 2 5 , 1 0 .0 20 8 0 . ,2 5 70. . 5 6 0 70%.75 1.00 ( p 1.0)0 A0.7 5 d a 0 . 5 m0 ,0 .2 5 4 0 0 . 0 90 6 0 ., 2 5 1 02 . 5 0 . 3 0 6 .7 5%1.00
Figure15: 1Dand2DvisualizationofResNet-56trainedwithdifferentoptimizer,batchsize,and
weightdecay. Thefirstandthirdrowuseszeroweightdecayandthesecondandfourthrowuses5e-4
weightdecay.
16

A.4 RepeatabilityoftheLossSurfaceVisualization
Dodifferentrandomdirectionsproducedramaticallydifferentplots?Weplotthe1DlosssurfaceofVGG-9with
10randomfilter-normalizeddirections.AsshowninFigure16,theplotsareverycloseinshape.Wealsorepeat
the2DlosssurfaceplotsmultipletimesforResNet-56-noshort,whichhasworsegeneralizationerror.Asshown
inFigure17,thereareapparentchangesinthelosssurfacefordifferentplots,however,thequalitativechoatic
behaviourisquiteconsistentacrossplots.
| 5    |     |     | 100         | 5   |     | 100         | 5   | 100 | 5          | 100         |
| ---- | --- | --- | ----------- | --- | --- | ----------- | --- | --- | ---------- | ----------- |
| 4    |     |     | 80          | 4   |     | 80          | 4   | 80  | 4          | 80          |
| 3    |     |     | 60 ycaruccA | 3   |     | 60 ycaruccA | 3   | 60  | ycaruccA 3 | 60 ycaruccA |
| ssoL |     |     | ssoL        |     |     | ssoL        |     |     | ssoL       |             |
| 2    |     |     | 40          | 2   |     | 40          | 2   | 40  | 2          | 40          |
| 1    |     |     | 20          | 1   |     | 20          | 1   | 20  | 1          | 20          |
01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0
(a) SGD,128,7.37% (b) SGD,8192,11.07% (c) Adam,128,7.44% (d) Adam,8192,10.91%
| 5      |     |     | 100      | 5   |     | 100      | 5   | 100 | 5        | 100      |
| ------ | --- | --- | -------- | --- | --- | -------- | --- | --- | -------- | -------- |
| 4      |     |     | 80       | 4   |     | 80       | 4   | 80  | 4        | 80       |
|        |     |     | ycaruccA |     |     | ycaruccA |     |     | ycaruccA | ycaruccA |
| ssoL 3 |     |     | 60 ssoL  | 3   |     | 60 ssoL  | 3   | 60  | ssoL 3   | 60       |
| 2      |     |     | 40       | 2   |     | 40       | 2   | 40  | 2        | 40       |
| 1      |     |     | 20       | 1   |     | 20       | 1   | 20  | 1        | 20       |
01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0 01.000.750.500.250.000.250.500.751.00 0
(e) SGD,128,6.00% (f) SGD,8192,10.19% (g) Adam,128,7.80% (h) Adam,8192,9.52%
Figure 16: Repeatability of the surface plots for VGG-9 with filter normalization. The shape of
minimaobtainedusing10differentrandomfilter-normalizeddirections.
| 1 . 0 0 |     | 4 .6 0 05 0.4 7 7 .6 .610 . 6 060 .100 000 | 5 . 6 6..1600 0 1 . 0 0 |     |     | 1 . 0 0 | 5 9 . 6 0 | 1 . | 0 0 |     |
| ------- | --- | ------------------------------------------ | ----------------------- | --- | --- | ------- | --------- | --- | --- | --- |
0 . 7 5 5 . 6 0 0 . 1 15 0 6 0 0. 6 0 0 0 0 5 4 .6. 6 0 01 00 4 0 0. 6 0 0 60 0 0 0 . 7 5 0 . 7 5 9 . 6 0 0 . 1 00 0 8 .6 0 0 . 7 5 9
00 5 .10 0 50 . 6 . 1 0 0 5 . 00 9 . 6 0 0 8 . 6 0 0 9 . 1 60 00 0 7 . 16 . 0 6 00 0 0 9 . 1 0 0 6. 6 0 . 6 0 0
0 . 5 0 9 .1 0 4 . 1 0 0 6 . 1 3.6 3 . 1 0 4. 1 0 . 5 0 9. 1 0 0 4 . 6 0 . 5 0 6 . 10 7 . 71 . 0 0 4 . 1 0 0 4 . 1 0 0 7 .60 0 5 5. . 61000 0 0 . 5 0 8 . 6 0 0 0 7 . 1 0 0 4 .6 0 0 0
6 . 6 0 0 5 . 6 0 0 0 0 5 . 1 0 0 0 .100 8.1 0 0 0 0 4 . 1 .01 00 5 . 1 0 0 8.100 0 7 . 1 90 .01006 7.6. 1 000 0 6 0 0 88 .. 196 0. 0 7 1 00 .0 6 00 0 9 . 1 0 0070. 6 0 4.60 5 .71 .. 0 610 00 600. 6 0 0 8.100
0 . 2 5 0 . 6 0 3 . 1 0 0 0 4 . 1 0 0 6 0 . 2 5 00 6 0 .0100 0 1. 600 3.6 6 0 0 0 . 2 5 0 . 2 5 5. 8 . 6 . 6 00 0 1 0.. 16 0 0 0 0 5.6 0 0 7 6 . 1 0 0
0 . 0 0 2 2. 6.1 0 00 1 0 .1 0 0 0 0 3 . 6 0 . 0 0 8 . 1 31 .1100 00.26 0 0 0 4 . 10 0 3 . 9 9 0 . 0 0 3 . 1 0 0 12 .. 16 00 00 7 . 60 0 7.60 9 .600 0 . 0 0 9 . 6 0 0 5 . 6 0 0 0 0 2 1 . 6 0 0 4 . 1 0 0 3 . 60 0 5 .1 00
0 4 .6 0 0 1 . 6 0 0 10 0 . 7 . 1 0 0 . .61 0 0 0 0 4 5 . 6 2.600 0 0 8 0 4 .1 3 . 60 0 .1 0 0
0 . 2 5 8 . 6 0 5 . 6 0 0 7 . 0 . 2 5 6 . 1 0 0 2 . 6 0 0 4 .6 00 4 .1 0 0 1 0 0 4 . 5 6 . 1.0 60 0 5 . 1 0 0 0 . 2 5 9. 6 8 9..1 6 8 0 .0 1 0 0 0 4 .1 0 3 . 88 6 . . .611 000 000 7 . 6 4 . 6 0 0 . 1 0 0 0 . 2 5 4.600 2 . 1 0 30 . 1 0 0 6 8 .690 . 60 0 0
| 0 . 5 0 | 56 0.. 61 00 0 0 | 0 0             | 7. 1 0 0 0 . 5 0        | 7                  | 00 7 .                                | 00 7 0.600 0 . 5 0 00 0 0 6 0 . 1              | 0 0 0 9 0 0 6.6 00                                                  | 0 . | 5 0 8 . 1 0 0 5 . 6 0 0 |     |
| ------- | ---------------- | --------------- | ----------------------- | ------------------ | ------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------- | --- | ----------------------- | --- |
|         | 5 .10            | 6 . 1 0 0 5 . 6 | 0                       | .6 00 6 . 6 0 0    | 5 .60 8 . 1 6 .6 6 . 01 0 06 .0 1 0 0 | 00                                             | 7 .0 1 0 0 6.10 0                                                   |     | 9 . 1 0 0 7 . 6 0 0     |     |
| 0 . 7 5 | 7 . 6            | 0 0 9           | . 6 0 0 8 . 1 0 0 . 7 5 | 8 .6 0 0 9 . 6 0 0 | 0 6 . 60 0 0                          | 0 8 .1 0 9.06 0 . 7 5 88. 6 . 1 0 7 0 .6 00 00 | 6 . 6 4 . 6 0 0 4 . 1 0 6 . 6 0 0                                   | 0 . | 7 5                     |     |
| 1 . 0 0 |                  |                 | 1 . 0 0                 |                    | 7 . 1 7 0 . 6 0 9 0 . 801 . 6 0       | 0 1 . 0 0                                      | 0 0 88 .. 61 00005 . 1 0 7 0.91.6098 00.. 0176 0 .08 6 0 0. 01 00 0 | 1 . | 0 0                     |     |
1.00 0 .7 5 0 .5 0 0 . 2 5 0 . 0 0 0 . 2 5 0 . 5 0 0 . 7 5 1 .00 1.00 0 . 75 0.5 0 0 . 2 5 0 . 0 0 0 . 2 5 0 .5 0 0 . 7 5 1.00 1. 0 0 0 . 7 5 0 . 5 0 0 . 2 5 0 . 0 0 0 . 2 5 0 . 5 0 0 . 7 5 1.00 1.0 0 0 . 7 5 0 . 5 0 0 . 2 5 0 . 0 0 0 .25 0 . 5 0 0 . 7 5 1 .00
Figure17: Repeatabilityofthe2DsurfaceplotsforResNet-56-noshort. Themodelistrainedwith
batchsize128,initiallearningrate0.1andweightdecay5e-4. Thefinaltraininglossis0.192,the
trainingerroris6.49andthetesterroris13.31.
A.5 ImplementationDetails
Computingresourcesforgeneratingthefigures OurPyTorchcodecanbeexecutedinamultipleGPU
workstationaswellasanHPCwithhundredsofGPUsusingmpi4py.Thecomputationtimedependsonthe
model’sinferencespeedonthetrainingset,theresolutionoftheplots,andthenumberofGPUs.Theresolution
forthe1DplotsinFigure3is401×401. Thedefaultresolutionsusedforthe2DcontoursinFigure3and
Figure5is51×51.Weusehigherresolutions(251×251)fortheResNet-56-noshortusedinFigure1toshow
moredetails.Forreference,a2DcontourplotofResNet-56witha(relativelylow)resolutionof51×51will
takeabout1houronaworkstationwith4GPUs(TitanXPascalor1080Ti).
BatchNormalizationparameters Inthe1Dlinearinterpolationmethods,theBatchNormalization(BN)
parametersincludingthe“runningmean”and“runningvariance”needtobeconsideredaspartofθ.Ifthese
parametersarenotconsidered,thenitisnotpossibletoreproducetheexactlossvaluesforbothminimizers.
Inthefilter-normalizedvisualization,therandomdirectionperturbsallweightsexceptbatchnormparameters.
Notethatthefilternormalizationprocessremovestheeffectofweightscaling,andsothebatchnormalization
canbeignored.
TheVGG-9architectureandparametersforAdam
VGG-9isacroppedversionofVGG-16,which
keepsthefirst7ConvlayersinVGG-16with2FClayers.ABNlayerisaddedaftereachconvlayerandthefirst
FClayer.WefindVGG-9isanefficientnetworkwithbetterperformancecomparingtoVGG-16onCIFAR-10.
Weusethedefaultvaluesforβ 1 ,β 2 and(cid:15)inAdamwiththesamelearningratescheduleasusedinSGD.
17

A.6 TrainingCurvesforVGG-9andResNets
ThelosscurvesfortrainingVGG-9usedinSection5areshowninFigure18.Figure19showsthelosscurves
anderrorcurvesofarchitecturesusedinSection6andTable2showsthefinalerrorandlossvalues.Thedefault
settingfortrainingisusingSGDwithNesterovmomentum,batch-size128,and0.0005weightdecayfor300
epochs. Thedefaultlearningratewasinitializedat0.1,anddecreasedbyafactorof10atepochs150,225
and275.
|      | CIFAR10, VGG-9, SGD |     | 40  | CIFAR10, VGG-9, SGD |      | CIFAR10, VGG-9, Adam | 40 CIFAR10, VGG-9, Adam |                   |
| ---- | ------------------- | --- | --- | ------------------- | ---- | -------------------- | ----------------------- | ----------------- |
| 2.00 |                     |     |     | bs=128, WD=0.0005   | 2.00 |                      |                         | bs=128, WD=0.0005 |
1.75 b b s s = = 1 1 2 2 8 8 , ,     W W D D = = 0 0 .0005 35 b s = 1 2 8 ,  W D = 0 1.75 b b s s = = 1 1 2 2 8 8 , ,     W W D D = = 0 0 .0005 35 bs=128, WD=0
|     |     | b s = 8 1 9 2 ,   W D = 0 .0005 |     | b s = 8 1 9 2 , W D = 0.0005 |     | b s = 8 1 9 2 ,   W D = 0 | .0005 | bs=8192, WD=0.0005 |
| --- | --- | ------------------------------- | --- | ---------------------------- | --- | ------------------------- | ----- | ------------------ |
1.50 b s = 8 1 9 2 ,   W D = 0 30 bs=8192, WD=0 1.50 b s = 8 1 9 2 ,   W D = 0 30 bs=8192, WD=0
| 1.25  |     |     | 25        |     | 1.25  |     | 25        |     |
| ----- | --- | --- | --------- | --- | ----- | --- | --------- | --- |
| ssoL  |     |     | )%( rorrE |     | ssoL  |     | )%( rorrE |     |
| 1.00  |     |     | 20        |     | 1.00  |     | 20        |     |
|       |     |     | 15        |     |       |     | 15        |     |
| 0.75  |     |     |           |     | 0.75  |     |           |     |
| 0.50  |     |     | 10        |     | 0.50  |     | 10        |     |
| 0.25  |     |     | 5         |     | 0.25  |     | 5         |     |
| 0.000 |     |     | 00        |     | 0.000 |     | 00        |     |
50 100 Epochs 150 200 250 300 50 100 Epochs 150 200 250 300 50 100 Epochs 150 200 250 300 50 100 Epochs 150 200 250 300
(a) SGD,lossvalues (b) SGD,errors (c) Adam,lossvalues (d) Adam,errors
Figure18: Trainingloss/errorcurvesforVGG-9withdifferentoptimizationmethods. Dashedlines
arefortesting,solidfortraining.
|     |     |     | 40  |     |     |     | 40  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
2.00 R e s N e t - 2 0 ResNet-20 2.00 R e s N e t - 2 0 _ n o s h o r t ResNet-20_noshort
1.75 R e s N e t - 5 6 35 R e s N e t - 5 6 1.75 R e s N e t - 5 6 _ n o s h o r t 35 ResNet-56_noshort
|                    |     | ResNet-110 | 30           | R e s N e | t - 1 10           | ResNet-110_noshort | 30           | ResNet-110_noshort |
| ------------------ | --- | ---------- | ------------ | --------- | ------------------ | ------------------ | ------------ | ------------------ |
| 1.50               |     |            |              |           | 1.50               |                    |              |                    |
| ssol gniniarT 1.25 |     |            | )%( rorrE 25 |           | ssol gniniarT 1.25 |                    | )%( rorrE 25 |                    |
| 1.00               |     |            | 20           |           | 1.00               |                    | 20           |                    |
| 0.75               |     |            | 15           |           | 0.75               |                    | 15           |                    |
| 0.50               |     |            | 10           |           | 0.50               |                    | 10           |                    |
| 0.25               |     |            | 5            |           | 0.25               |                    | 5            |                    |
0.000 00 50 100 150 200 250 300 0.000 00 50 100 150 200 250 300
50 100 Epochs 150 200 250 300 Epochs 50 100 Epochs 150 200 250 300 Epochs
(a) ResNet-CIFAR (b) ResNet-CIFAR (c) ResNet-CIFAR-noshort (d) ResNet-CIFAR-noshort
|     |         |                                                                | Figure19: | Convergencecurvesfordifferentarchitectures. |       |               |           |     |
| --- | ------- | -------------------------------------------------------------- | --------- | ------------------------------------------- | ----- | ------------- | --------- | --- |
|     | Table2: | LossvaluesanderrorsfordifferentarchitecturestrainedonCIFAR-10. |           |                                             |       |               |           |     |
|     |         |                                                                |           | initLR TrainingLoss                         |       | TrainingError | TestError |     |
|     |         | ResNet-20                                                      |           | 0.1                                         | 0.017 | 0.286         | 7.37      |     |
|     |         | ResNet-20-noshort                                              |           | 0.1                                         | 0.025 | 0.560         | 8.18      |     |
|     |         | ResNet-56                                                      |           | 0.1                                         | 0.004 | 0.052         | 5.89      |     |
|     |         | ResNet-56-noshort                                              |           | 0.1                                         | 0.192 | 6.494         | 13.31     |     |
|     |         | ResNet-56-noshort                                              |           | 0.01                                        | 0.024 | 0.704         | 10.83     |     |
|     |         | ResNet-110                                                     |           | 0.1                                         | 0.002 | 0.042         | 5.79      |     |
|     |         | ResNet-110-noshort                                             |           | 0.01                                        | 0.258 | 8.732         | 16.44     |     |
18