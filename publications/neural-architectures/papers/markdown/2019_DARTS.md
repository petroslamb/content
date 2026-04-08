PublishedasaconferencepaperatICLR2019
DARTS: DIFFERENTIABLE ARCHITECTURE SEARCH
HanxiaoLiu∗ KarenSimonyan YimingYang
CMU DeepMind CMU
hanxiaol@cs.cmu.com simonyan@google.com yiming@cs.cmu.edu
ABSTRACT
Thispaperaddressesthescalabilitychallengeofarchitecturesearchbyformulating
thetaskinadifferentiablemanner.Unlikeconventionalapproachesofapplyingevo-
lutionorreinforcementlearningoveradiscreteandnon-differentiablesearchspace,
ourmethodisbasedonthecontinuousrelaxationofthearchitecturerepresentation,
allowing efficient search of the architecture using gradient descent. Extensive
experimentsonCIFAR-10,ImageNet,PennTreebankandWikiText-2showthat
ouralgorithmexcelsindiscoveringhigh-performanceconvolutionalarchitectures
forimageclassificationandrecurrentarchitecturesforlanguagemodeling,while
beingordersofmagnitudefasterthanstate-of-the-artnon-differentiabletechniques.
Ourimplementationhasbeenmadepubliclyavailabletofacilitatefurtherresearch
onefficientarchitecturesearchalgorithms.
1 INTRODUCTION
Discoveringstate-of-the-artneuralnetworkarchitecturesrequiressubstantialeffortofhumanexperts.
Recently, there has been a growing interest in developing algorithmic solutions to automate the
manualprocessofarchitecturedesign. Theautomaticallysearchedarchitectureshaveachievedhighly
competitiveperformanceintaskssuchasimageclassification(Zoph&Le,2017;Zophetal.,2018;
Liuetal.,2018b;a;Realetal.,2018)andobjectdetection(Zophetal.,2018).
Thebestexistingarchitecturesearchalgorithmsarecomputationallydemandingdespitetheirremark-
ableperformance. Forexample,obtainingastate-of-the-artarchitectureforCIFAR-10andImageNet
required2000GPUdaysofreinforcementlearning(RL)(Zophetal.,2018)or3150GPUdaysof
evolution(Realetal.,2018). Severalapproachesforspeedinguphavebeenproposed,suchasimpos-
ingaparticularstructureofthesearchspace(Liuetal.,2018b;a),weightsorperformanceprediction
foreachindividualarchitecture(Brocketal.,2018;Bakeretal.,2018)andweightsharing/inheritance
acrossmultiplearchitectures(Elskenetal.,2017;Phametal.,2018b;Caietal.,2018;Benderetal.,
2018),butthefundamentalchallengeofscalabilityremains. Aninherentcauseofinefficiencyforthe
dominantapproaches,e.g. basedonRL,evolution,MCTS(Negrinho&Gordon,2017),SMBO(Liu
etal.,2018a)orBayesianoptimization(Kandasamyetal.,2018),isthefactthatarchitecturesearch
istreatedasablack-boxoptimizationproblemoveradiscretedomain,whichleadstoalargenumber
ofarchitectureevaluationsrequired.
Inthiswork,weapproachtheproblemfromadifferentangle,andproposeamethodforefficient
architecturesearchcalledDARTS(DifferentiableARchiTectureSearch). Insteadofsearchingover
a discrete set of candidate architectures, we relax the search space to be continuous, so that the
architecturecanbeoptimizedwithrespecttoitsvalidationsetperformancebygradientdescent. The
dataefficiencyofgradient-basedoptimization,asopposedtoinefficientblack-boxsearch,allows
DARTS to achieve competitive performance with the state of the art using orders of magnitude
lesscomputationresources. Italsooutperformsanotherrecentefficientarchitecturesearchmethod,
ENAS(Phametal.,2018b). Notably,DARTSissimplerthanmanyexistingapproachesasitdoes
notinvolvecontrollers(Zoph&Le,2017;Bakeretal.,2017;Zophetal.,2018;Phametal.,2018b;
Zhongetal.,2018),hypernetworks(Brocketal.,2018)orperformancepredictors(Liuetal.,2018a),
yetitisgenericenoughhandlebothconvolutionalandrecurrentarchitectures.
Theideaofsearchingarchitectureswithinacontinuousdomainisnotnew(Saxena&Verbeek,2016;
Ahmed&Torresani,2017;Veniat&Denoyer,2017;Shinetal.,2018),butthereareseveralmajor
∗Currentaffiliation:GoogleBrain.
1
9102
rpA
32
]GL.sc[
2v55090.6081:viXra

PublishedasaconferencepaperatICLR2019
distinctions. Whilepriorworksseektofine-tuneaspecificaspectofanarchitecture,suchasfilter
shapesorbranchingpatternsinaconvolutionalnetwork,DARTSisabletolearnhigh-performance
architecturebuildingblockswithcomplexgraphtopologieswithinarichsearchspace. Moreover,
DARTSisnotrestrictedtoanyspecificarchitecturefamily,andisapplicabletobothconvolutional
andrecurrentnetworks.
Inourexperiments(Sect.3)weshowthatDARTSisabletodesignaconvolutionalcellthatachieves
2.76 ± 0.09% test error on CIFAR-10 for image classification using 3.3M parameters, which is
competitivewiththestate-of-the-artresultbyregularizedevolution(Realetal.,2018)obtainedusing
threeordersofmagnitudemorecomputationresources. Thesameconvolutionalcellalsoachieves
26.7%top-1errorwhentransferredtoImageNet(mobilesetting),whichiscomparabletothebestRL
method(Zophetal.,2018). Onthelanguagemodelingtask,DARTSefficientlydiscoversarecurrent
cellthatachieves55.7testperplexityonPennTreebank(PTB),outperformingbothextensivelytuned
LSTM(Melisetal.,2018)andalltheexistingautomaticallysearchedcellsbasedonNAS(Zoph&
Le,2017)andENAS(Phametal.,2018b).
Ourcontributionscanbesummarizedasfollows:
• We introduce a novel algorithm for differentiable network architecture search based on
bileveloptimization,whichisapplicabletobothconvolutionalandrecurrentarchitectures.
• Throughextensiveexperimentsonimageclassificationandlanguagemodelingtasksweshow
thatgradient-basedarchitecturesearchachieveshighlycompetitiveresultsonCIFAR-10
andoutperformsthestateoftheartonPTB.Thisisaveryinterestingresult,considering
thatsofarthebestarchitecturesearchmethodsusednon-differentiablesearchtechniques,
e.g. basedonRL(Zophetal.,2018)orevolution(Realetal.,2018;Liuetal.,2018b).
• Weachieveremarkableefficiencyimprovement(reducingthecostofarchitecturediscovery
toafewGPUdays),whichweattributetotheuseofgradient-basedoptimizationasopposed
tonon-differentiablesearchtechniques.
• WeshowthatthearchitectureslearnedbyDARTSonCIFAR-10andPTBaretransferable
toImageNetandWikiText-2,respectively.
TheimplementationofDARTSisavailableathttps://github.com/quark0/darts
2 DIFFERENTIABLE ARCHITECTURE SEARCH
WedescribeoursearchspaceingeneralforminSect.2.1,wherethecomputationprocedureforan
architecture(oracellinit)isrepresentedasadirectedacyclicgraph. Wethenintroduceasimple
continuousrelaxationschemeforoursearchspacewhichleadstoadifferentiablelearningobjective
for the joint optimization of the architecture and its weights (Sect. 2.2). Finally, we propose an
approximationtechniquetomakethealgorithmcomputationallyfeasibleandefficient(Sect.2.3).
2.1 SEARCHSPACE
FollowingZophetal.(2018);Realetal.(2018);Liuetal.(2018a;b),wesearchforacomputation
cellasthebuildingblockofthefinalarchitecture. Thelearnedcellcouldeitherbestackedtoforma
convolutionalnetworkorrecursivelyconnectedtoformarecurrentnetwork.
AcellisadirectedacyclicgraphconsistingofanorderedsequenceofN nodes. Eachnodex(i)is
alatentrepresentation(e.g. afeaturemapinconvolutionalnetworks)andeachdirectededge(i,j)
isassociatedwithsomeoperationo(i,j)thattransformsx(i). Weassumethecelltohavetwoinput
nodesandasingleoutputnode. Forconvolutionalcells,theinputnodesaredefinedasthecelloutputs
intheprevioustwolayers(Zophetal.,2018). Forrecurrentcells,thesearedefinedastheinputat
thecurrentstepandthestatecarriedfromthepreviousstep. Theoutputofthecellisobtainedby
applyingareductionoperation(e.g. concatenation)toalltheintermediatenodes.
Eachintermediatenodeiscomputedbasedonallofitspredecessors:
(cid:88)
x(j) = o(i,j)(x(i)) (1)
i<j
2

PublishedasaconferencepaperatICLR2019
Figure1: AnoverviewofDARTS:(a)Operationsontheedgesareinitiallyunknown. (b)Continuous
relaxationofthesearchspacebyplacingamixtureofcandidateoperationsoneachedge. (c)Joint
optimizationofthemixingprobabilitiesandthenetworkweightsbysolvingabileveloptimization
problem. (d)Inducingthefinalarchitecturefromthelearnedmixingprobabilities.
Aspecialzerooperationisalsoincludedtoindicatealackofconnectionbetweentwonodes. The
taskoflearningthecellthereforereducestolearningtheoperationsonitsedges.
2.2 CONTINUOUSRELAXATIONANDOPTIMIZATION
LetObeasetofcandidateoperations(e.g.,convolution,maxpooling,zero)whereeachoperation
representssomefunctiono(·)tobeappliedtox(i). Tomakethesearchspacecontinuous,werelax
thecategoricalchoiceofaparticularoperationtoasoftmaxoverallpossibleoperations:
o¯(i,j)(x)= (cid:88) exp(α o (i,j)) o(x) (2)
(cid:80) exp(α(i,j))
o∈O o(cid:48)∈O o(cid:48)
wheretheoperationmixingweightsforapairofnodes(i,j)areparameterizedbyavectorα(i,j)of
dimension|O|. Thetaskofarchitecturesearchthenreducestolearningasetofcontinuousvariables
α=
(cid:8) α(i,j)(cid:9)
,asillustratedinFig.1. Attheendofsearch,adiscretearchitecturecanbeobtainedby
replacingeachmixedoperationo¯(i,j)withthemostlikelyoperation,i.e.,o(i,j) =argmax α(i,j).
o∈O o
Inthefollowing,werefertoαasthe(encodingofthe)architecture.
Afterrelaxation,ourgoalistojointlylearnthearchitectureαandtheweightswwithinallthemixed
operations(e.g. weightsoftheconvolutionfilters). AnalogoustoarchitecturesearchusingRL(Zoph
&Le,2017;Zophetal.,2018;Phametal.,2018b)orevolution(Liuetal.,2018b;Realetal.,2018)
wherethevalidationsetperformanceistreatedastherewardorfitness,DARTSaimstooptimizethe
validationloss,butusinggradientdescent.
DenotebyL andL thetrainingandthevalidationloss,respectively. Bothlossesaredeter-
train val
minednotonlybythearchitectureα,butalsotheweightswinthenetwork. Thegoalforarchitecture
searchistofindα∗thatminimizesthevalidationlossL (w∗,α∗),wheretheweightsw∗associated
val
withthearchitectureareobtainedbyminimizingthetraininglossw∗ =argmin L (w,α∗).
w train
Thisimpliesabileveloptimizationproblem(Anandalingam&Friesz,1992;Colsonetal.,2007)with
αastheupper-levelvariableandwasthelower-levelvariable:
min L (w∗(α),α) (3)
val
α
s.t. w∗(α)=argmin L (w,α) (4)
w train
Thenestedformulationalsoarisesingradient-basedhyperparameteroptimization(Maclaurinetal.,
2015;Pedregosa,2016;Franceschietal.,2018),whichisrelatedinasensethatthearchitectureα
couldbeviewedasaspecialtypeofhyperparameter,althoughitsdimensionissubstantiallyhigher
thanscalar-valuedhyperparameterssuchasthelearningrate,anditishardertooptimize.
3

PublishedasaconferencepaperatICLR2019
Algorithm1:DARTS–DifferentiableArchitectureSearch
Createamixedoperationo¯(i,j)parametrizedbyα(i,j)foreachedge(i,j)
whilenotconvergeddo
| 1. Updatearchitectureαbydescending∇ |     |     |     | L (w−ξ∇ | L       | (w,α),α) |     |
| ----------------------------------- | --- | --- | --- | ------- | ------- | -------- | --- |
|                                     |     |     |     | α val   | w train |          |     |
(ξ =0ifusingfirst-orderapproximation)
| 2. Updateweightswbydescending∇ |     |     |     | L (w,α) |     |     |     |
| ------------------------------ | --- | --- | --- | ------- | --- | --- | --- |
w train
Derivethefinalarchitecturebasedonthelearnedα.
2.3 APPROXIMATEARCHITECTUREGRADIENT
Evaluatingthearchitecturegradientexactlycanbeprohibitiveduetotheexpensiveinneroptimization.
Wethereforeproposeasimpleapproximationschemeasfollows:
|     |     | ∇   | L (w∗(α),α) |     |     |     | (5) |
| --- | --- | --- | ----------- | --- | --- | --- | --- |
α val
|     |     | ≈∇  | α L val (w−ξ∇ | w L train | (w,α),α) |     | (6) |
| --- | --- | --- | ------------- | --------- | -------- | --- | --- |
wherewdenotesthecurrentweightsmaintainedbythealgorithm,andξisthelearningrateforastep
ofinneroptimization. Theideaistoapproximatew∗(α)byadaptingwusingonlyasingletraining
step,withoutsolvingtheinneroptimization(equation4)completelybytraininguntilconvergence.
Relatedtechniqueshavebeenusedinmeta-learningformodeltransfer(Finnetal.,2017),gradient-
basedhyperparametertuning(Luketinaetal.,2016)andunrolledgenerativeadversarialnetworks
(Metzetal.,2017). Noteequation6willreduceto∇ L (w,α)ifwisalreadyalocaloptimumfor
α val
| theinneroptimizationandthus∇ |     |     | L (w,α)=0. |     |     |     |     |
| ---------------------------- | --- | --- | ---------- | --- | --- | --- | --- |
|                              |     |     | w train    |     |     |     |     |
TheiterativeprocedureisoutlinedinAlg.1. Whilewearenotcurrentlyawareoftheconvergence
guaranteesforouroptimizationalgorithm,inpracticeitisabletoreachafixedpointwithasuitable
choiceofξ1. Wealsonotethatwhenmomentumisenabledforweightoptimisation,theone-step
unrolledlearningobjectiveinequation6ismodifiedaccordinglyandallofouranalysisstillapplies.
Applyingchainruletotheapproximatearchitecturegradient(equation6)yields
|     |     | ∇ L (w(cid:48),α)−ξ∇2 |     | L (w,α)∇  | L             | (w(cid:48),α) | (7) |
| --- | --- | --------------------- | --- | --------- | ------------- | ------------- | --- |
|     |     | α val                 |     | α,w train | w(cid:48) val |               |     |
wherew(cid:48) =w−ξ∇ L (w,α)denotestheweightsforaone-stepforwardmodel.Theexpression
w train
abovecontainsanexpensivematrix-vectorproductinitssecondterm. Fortunately,thecomplexity
Let(cid:15)beasmallscalar2and
canbesubstantiallyreducedusingthefinitedifferenceapproximation.
| w±           |                 | (w(cid:48),α).   |                |         |          |           |     |
| ------------ | --------------- | ---------------- | -------------- | ------- | -------- | --------- | --- |
| =w±(cid:15)∇ | w(cid:48) L val | Then:            |                |         |          |           |     |
|              |                 |                  |                | ∇ L     | (w+,α)−∇ | L (w−,α)  |     |
| ∇2           |                 |                  | (w(cid:48),α)≈ | α train |          | α train   |     |
|              | L train         | (w,α)∇ w(cid:48) | L val          |         |          |           | (8) |
|              | α,w             |                  |                |         |          | 2(cid:15) |     |
Evaluatingthefinitedifferencerequiresonlytwoforwardpassesfortheweightsandtwobackward
passesforα,andthecomplexityisreducedfromO(|α||w|)toO(|α|+|w|).
First-orderApproximation Whenξ =0,thesecond-orderderivativeinequation7willdisappear.
Inthiscase,thearchitecturegradientisgivenby∇ L (w,α),correspondingtothesimpleheuristic
α val
ofoptimizingthevalidationlossbyassumingthecurrentwisthesameasw∗(α). Thisleadstosome
speed-upbutempiricallyworseperformance,accordingtoourexperimentalresultsinTable1and
Table2. Inthefollowing,werefertothecaseofξ =0asthefirst-orderapproximation,andreferto
| thegradientformulationwithξ |     | >0asthesecond-orderapproximation. |     |     |     |     |     |
| --------------------------- | --- | --------------------------------- | --- | --- | --- | --- | --- |
2.4 DERIVINGDISCRETEARCHITECTURES
Toformeachnodeinthediscretearchitecture,weretainthetop-kstrongestoperations(fromdistinct
nodes)amongallnon-zerocandidateoperationscollectedfromallthepreviousnodes. Thestrength
|     |     |     | exp(α( i,j)) |     |     |     |     |
| --- | --- | --- | ------------ | --- | --- | --- | --- |
ofanoperationisdefinedas o . Tomakeourderivedarchitecturecomparablewith
|     |     | (cid:80)    | exp(α( | i ,j))   |     |     |     |
| --- | --- | ----------- | ------ | -------- | --- | --- | --- |
|     |     | o(cid:48)∈O |        | (cid:48) |     |     |     |
o
1Asimpleworkingstrategyistosetξequaltothelearningrateforw’soptimizer.
| 2Wefound(cid:15)=0.01/(cid:107)∇ |     | (w(cid:48),α)(cid:107) |                                                  |     |     |     |     |
| -------------------------------- | --- | ---------------------- | ------------------------------------------------ | --- | --- | --- | --- |
|                                  |     | w(cid:48)L val         | 2 tobesufficientlyaccurateinallofourexperiments. |     |     |     |     |
4

PublishedasaconferencepaperatICLR2019
|     |     | Figure2: Learningdynamicsofouriterativealgorithm |     |     |     |
| --- | --- | ------------------------------------------------ | --- | --- | --- |
=0.7
|     |     | when L val (w,α) | = αw−2α+1 | and L train | (w,α) = |
| --- | --- | ---------------- | --------- | ----------- | ------- |
3 =0.5
| =0.3 |     | w2−2αw+α2,startingfrom(α(0),w(0))=(2,−2).The |     |     |     |
| ---- | --- | -------------------------------------------- | --- | --- | --- |
=0
)w( sthgieW 2 analyticalsolutionforthecorrespondingbileveloptimiza-
|     |     | tionproblemis(α∗,w∗) |     | = (1,1),whichishighlighted |     |
| --- | --- | -------------------- | --- | -------------------------- | --- |
1
|     |     | in the red circle. | The dashed | red line indicates | the fea- |
| --- | --- | ------------------ | ---------- | ------------------ | -------- |
0
siblesetwhereconstraintequation4issatisfiedexactly
| 1   |     | (namely,weightsinwareoptimalforthegivenarchitec- |     |     |     |
| --- | --- | ------------------------------------------------ | --- | --- | --- |
|     |     | tureα). Theexampleshowsthatasuitablechoiceofξ    |     |     |     |
2
helpstoconvergetoabetterlocaloptimum.
| 0.5 1.0        | 1.5 2.0 2.5 | 3.0 3.5 |     |     |     |
| -------------- | ----------- | ------- | --- | --- | --- |
| Architecture ( | )           |         |     |     |     |
thoseintheexistingworks,weusek =2forconvolutionalcells(Zophetal.,2018;Liuetal.,2018a;
| Realetal.,2018)andk | =1forrecurrentcells(Phametal.,2018b). |     |     |     |     |
| ------------------- | ------------------------------------- | --- | --- | --- | --- |
Thezerooperationsareexcludedintheabovefortworeasons. First,weneedexactlyk non-zero
incomingedgespernodeforfaircomparisonwiththeexistingmodels. Second,thestrengthofthe
zerooperationsisunderdetermined,asincreasingthelogitsofzerooperationsonlyaffectsthescale
oftheresultingnoderepresentations,anddoesnotaffectthefinalclassificationoutcomeduetothe
presenceofbatchnormalization(Ioffe&Szegedy,2015).
| 3 EXPERIMENTS | RESULTS |     |     |     |     |
| ------------- | ------- | --- | --- | --- | --- |
AND
OurexperimentsonCIFAR-10andPTBconsistoftwostages,architecturesearch(Sect.3.1)and
architectureevaluation(Sect.3.2). Inthefirststage,wesearchforthecellarchitecturesusingDARTS,
anddeterminethebestcellsbasedontheirvalidationperformance. Inthesecondstage,weusethese
cellstoconstructlargerarchitectures,whichwetrainfromscratchandreporttheirperformanceon
thetestset. WealsoinvestigatethetransferabilityofthebestcellslearnedonCIFAR-10andPTBby
evaluatingthemonImageNetandWikiText-2(WT2)respectively.
3.1 ARCHITECTURESEARCH
3.1.1 SEARCHINGFORCONVOLUTIONALCELLSONCIFAR-10
WeincludethefollowingoperationsinO: 3×3and5×5separableconvolutions,3×3and5×5
dilatedseparableconvolutions,3×3maxpooling,3×3averagepooling,identity,andzero. All
operationsareofstrideone(ifapplicable)andtheconvolvedfeaturemapsarepaddedtopreserve
theirspatialresolution. WeusetheReLU-Conv-BNorderforconvolutionaloperations,andeach
separableconvolutionisalwaysappliedtwice(Zophetal.,2018;Realetal.,2018;Liuetal.,2018a).
Our convolutional cell consists of N = 7 nodes, among which the output node is defined as the
depthwiseconcatenationofalltheintermediatenodes(inputnodesexcluded). Therestofthesetup
followsZophetal.(2018);Liuetal.(2018a);Realetal.(2018),whereanetworkisthenformedby
stackingmultiplecellstogether.Thefirstandsecondnodesofcellkaresetequaltotheoutputsofcell
k−2andcellk−1,respectively,and1×1convolutionsareinsertedasnecessary.Cellslocatedatthe
1/3and2/3ofthetotaldepthofthenetworkarereductioncells,inwhichalltheoperationsadjacent
totheinputnodesareofstridetwo. Thearchitectureencodingthereforeis(α ,α ),where
|     |     |     |     | normal reduce |     |
| --- | --- | --- | --- | ------------- | --- |
α issharedbyallthenormalcellsandα issharedbyallthereductioncells.
normal reduce
DetailedexperimentalsetupforthissectioncanbefoundinSect.A.1.1.
3.1.2 SEARCHINGFORRECURRENTCELLSONPENNTREEBANK
Oursetofavailableoperationsincludeslineartransformationsfollowedbyoneoftanh,relu,sigmoid
activations,aswellastheidentitymappingandthezerooperation. Thechoiceofthesecandidate
operationsfollowsZoph&Le(2017);Phametal.(2018b).
OurrecurrentcellconsistsofN =12nodes. Theveryfirstintermediatenodeisobtainedbylinearly
transformingthetwoinputnodes,addinguptheresultsandthenpassingthroughatanhactivation
5

PublishedasaconferencepaperatICLR2019
|     | CIFAR-10    |     |     | CIFAR-10      |     |     | Penn Treebank |       |     | Penn Treebank |
| --- | ----------- | --- | --- | ------------- | --- | --- | ------------- | ----- | --- | ------------- |
|     |             |     |     |               |     | 71  |               |       | 71  |               |
| 15  | DARTS       |     | 15  | DARTS (run 1) |     |     |               | DARTS |     | DARTS (run 1) |
|     | AmoebaNet-A |     |     | DARTS (run 2) |     | 70  |               | ENAS  | 70  | DARTS (run 2) |
NASNet-A )%( raF oS rorrE dilaV tseB DARTS (run 3) raF oS ytixelpreP dilaV tseB DARTS (run 3)
| 14                 |           |       | 14  |               |     |                  |           |       |     |               |
| ------------------ | --------- | ----- | --- | ------------- | --- | ---------------- | --------- | ----- | --- | ------------- |
|                    |           |       |     | DARTS (run 4) |     | 69               |           |       | 69  | DARTS (run 4) |
| )%( rorrE dilaV 13 |           |       | 13  | AmoebaNet-A   |     | ytixelpreP dilaV |           |       |     | ENAS          |
|                    |           |       |     | NASNet-A      |     | 68               |           |       | 68  |               |
| 12                 |           |       | 12  |               |     |                  |           |       |     |               |
|                    |           |       |     |               |     | 67               |           |       | 67  |               |
| 11                 |           |       | 11  |               |     |                  |           |       |     |               |
|                    |           |       |     |               |     | 66               |           |       | 66  |               |
| 10                 |           |       | 10  |               |     | 65               |           |       | 65  |               |
| 9                  |           |       | 9   |               |     | 64               |           |       | 64  |               |
| 8                  |           |       | 8   |               |     | 63               |           |       | 63  |               |
|                    | 0 5 10 15 | 20 25 |     | 0 10          | 20  |                  | 0 1       | 2 3 4 |     | 0 1 2 3 4     |
|                    | GPU Hours |       |     | GPU Hours     |     |                  | GPU Hours |       |     | GPU Hours     |
Figure3: SearchprogressofDARTSforconvolutionalcellsonCIFAR-10andrecurrentcellson
PennTreebank. Wekeeptrackofthemostrecentarchitecturesovertime. Eacharchitecturesnapshot
isre-trainedfromscratchusingthetrainingset(for100epochsonCIFAR-10andfor300epochson
PTB)andthenevaluatedonthevalidationset. Foreachtask,werepeattheexperimentsfor4times
withdifferentrandomseeds,andreportthemedianandthebest(perrun)validationperformanceof
thearchitecturesovertime. Asreferences,wealsoreporttheresults(underthesameevaluationsetup;
withcomparablenumberofparameters)ofthebestexistingcellsdiscoveredusingRLorevolution,
includingNASNet-A(Zophetal.,2018)(2000GPUdays),AmoebaNet-A(3150GPUdays)(Real
etal.,2018)andENAS(0.5GPUday)(Phametal.,2018b).
function,asdoneintheENAScell(Phametal.,2018b). Therestofthecellislearned. Othersettings
aresimilartoENAS,whereeachoperationisenhancedwithahighwaybypass(Zillyetal.,2016)and
thecelloutputisdefinedastheaverageofalltheintermediatenodes. AsinENAS,weenablebatch
normalizationineachnodetopreventgradientexplosionduringarchitecturesearch,anddisableit
duringarchitectureevaluation. Ourrecurrentnetworkconsistsofonlyasinglecell,i.e.wedonot
assumeanyrepetitivepatternswithintherecurrentarchitecture.
DetailedexperimentalsetupforthissectioncanbefoundinSect.A.1.2.
sep_conv_3x3
|     |     |     |     |     |     |     |     |     | x_{t} | h_{t-1} |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------- |
c_{k-1} sep_conv_3x3
skip_connect
|     |     |     | 2   |     |     |     |     |     | 0   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sep_conv_3x3
|         |              |     | 1            |     |       |     |     |     |     | sigmoid |
| ------- | ------------ | --- | ------------ | --- | ----- | --- | --- | --- | --- | ------- |
|         | sep_conv_3x3 |     |              |     | c_{k} |     |     |     |     |         |
| c_{k-2} |              |     | 0            |     |       |     |     |     | 1   |         |
|         | sep_conv_3x3 |     | dil_conv_3x3 |     |       |     |     |     |     |         |
3
|          |                              | skip_connect |     |     |     |     |     |      | relu   | identity |
| -------- | ---------------------------- | ------------ | --- | --- | --- | --- | --- | ---- | ------ | -------- |
|          |                              |              |     |     |     |     |     |      | 2 relu |          |
| Figure4: | NormalcelllearnedonCIFAR-10. |              |     |     |     |     |     |      |        |          |
|          |                              |              |     |     |     |     |     | tanh |        | 4        |
max_pool_3x3
|         |              |     |     | skip_connect 2 |       |     |             |     |      |     |
| ------- | ------------ | --- | --- | -------------- | ----- | --- | ----------- | --- | ---- | --- |
| c_{k-2} | max_pool_3x3 |     |     |                |       |     |             | 5   | 3    |     |
|         |              |     | 0   |                | c_{k} |     | sigmoidrelu |     | tanh |     |
skip_connect
|     | max_pool_3x3 |     |     | 3            |     |     |     |     |     |     |
| --- | ------------ | --- | --- | ------------ | --- | --- | --- | --- | --- | --- |
|     |              |     |     | skip_connect |     |     | 6   | 8   | 7   |     |
1
| c_{k-1} |     | max_pool_3x3 |     |     |     |     |     |     |     |     |
| ------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
h_{t}
max_pool_3x3
Figure5: ReductioncelllearnedonCIFAR-10. Figure6: RecurrentcelllearnedonPTB.
3.2 ARCHITECTUREEVALUATION
Todeterminethearchitectureforfinalevaluation,werunDARTSfourtimeswithdifferentrandom
seedsandpickthebestcellbasedonitsvalidationperformanceobtainedbytrainingfromscratchfor
6

PublishedasaconferencepaperatICLR2019
ashortperiod(100epochsonCIFAR-10and300epochsonPTB).Thisisparticularlyimportantfor
recurrentcells,astheoptimizationoutcomescanbeinitialization-sensitive(Fig.3).
Toevaluatetheselectedarchitecture,werandomlyinitializeitsweights(weightslearnedduringthe
searchprocessarediscarded),trainitfromscratch,andreportitsperformanceonthetestset. We
notethetestsetisneverusedforarchitecturesearchorarchitectureselection.
Detailed experimental setup for architecture evaluation on CIFAR-10 and PTB can be found in
Sect.A.2.1andSect.A.2.2,respectively. BesidesCIFAR-10andPTB,wefurtherinvestigatedthe
transferabilityofourbestconvolutionalcell(searchedonCIFAR-10)andrecurrentcell(searchedon
PTB)byevaluatingthemonImageNet(mobilesetting)andWikiText-2,respectively. Moredetailsof
thetransferlearningexperimentscanbefoundinSect.A.2.3andSect.A.2.4.
Table1: Comparisonwithstate-of-the-artimageclassifiersonCIFAR-10(lowererrorrateisbetter).
NotethesearchcostforDARTSdoesnotincludetheselectioncost(1GPUday)orthefinalevaluation
costbytrainingtheselectedarchitecturefromscratch(1.5GPUdays).
|                                  | TestError | Params | SearchCost |      | Search    |
| -------------------------------- | --------- | ------ | ---------- | ---- | --------- |
| Architecture                     |           |        |            | #ops |           |
|                                  | (%)       | (M)    | (GPUdays)  |      | Method    |
| DenseNet-BC(Huangetal.,2017)     | 3.46      | 25.6   | –          | –    | manual    |
| NASNet-A+cutout(Zophetal.,2018)  | 2.65      | 3.3    | 2000       | 13   | RL        |
| NASNet-A+cutout(Zophetal.,2018)† | 2.83      | 3.1    | 2000       | 13   | RL        |
| BlockQNN(Zhongetal.,2018)        | 3.54      | 39.8   | 96         | 8    | RL        |
| AmoebaNet-A(Realetal.,2018)      | 3.34±0.06 | 3.2    | 3150       | 19   | evolution |
AmoebaNet-A+cutout(Realetal.,2018)† 3.12 3.1 3150 19 evolution
AmoebaNet-B+cutout(Realetal.,2018) 2.55±0.05 2.8 3150 19 evolution
Hierarchicalevolution(Liuetal.,2018b) 3.75±0.12 15.7 300 6 evolution
| PNAS(Liuetal.,2018a)         | 3.41±0.09 | 3.2 | 225 | 8   | SMBO |
| ---------------------------- | --------- | --- | --- | --- | ---- |
| ENAS+cutout(Phametal.,2018b) | 2.89      | 4.6 | 0.5 | 6   | RL   |
ENAS+cutout(Phametal.,2018b)*
|     | 2.91 | 4.2 | 4   | 6   | RL  |
| --- | ---- | --- | --- | --- | --- |
Randomsearchbaseline‡+cutout
|                           | 3.29±0.15 | 3.2 | 4   | 7                | random |
| ------------------------- | --------- | --- | --- | ---------------- | ------ |
| DARTS(firstorder)+cutout  | 3.00±0.14 | 3.3 | 1.5 | 7 gradient-based |        |
| DARTS(secondorder)+cutout | 2.76±0.09 | 3.3 | 4   | 7 gradient-based |        |
*
ObtainedbyrepeatingENASfor8timesusingthecodepubliclyreleasedbytheauthors.Thecellforfinal
evaluationischosenaccordingtothesameselectionprotocolasforDARTS.
† Obtainedbytrainingthecorrespondingarchitecturesusingoursetup.
‡ Bestarchitectureamong24samplesaccordingtothevalidationerrorafter100trainingepochs.
Table2: Comparisonwithstate-of-the-artlanguagemodelsonPTB(lowerperplexityisbetter). Note
thesearchcostforDARTSdoesnotincludetheselectioncost(1GPUday)orthefinalevaluation
costbytrainingtheselectedarchitecturefromscratch(3GPUdays).
|                                 | Perplexity | Params   | SearchCost |      | Search |
| ------------------------------- | ---------- | -------- | ---------- | ---- | ------ |
| Architecture                    |            |          |            | #ops |        |
|                                 | valid      | test (M) | (GPUdays)  |      | Method |
| VariationalRHN(Zillyetal.,2016) | 67.9 65.4  | 23       | –          | –    | manual |
| LSTM(Merityetal.,2018)          | 60.7 58.8  | 24       | –          | –    | manual |
LSTM+skipconnections(Melisetal.,2018) 60.9 58.3 24 – – manual
LSTM+15softmaxexperts(Yangetal.,2018) 58.1 56.0 22 – – manual
| NAS(Zoph&Le,2017)      | – 64.0    | 25  | 1e4CPUdays | 4   | RL             |
| ---------------------- | --------- | --- | ---------- | --- | -------------- |
| ENAS(Phametal.,2018b)* | 68.3 63.1 | 24  | 0.5        | 4   | RL             |
| ENAS(Phametal.,2018b)† | 60.8 58.6 | 24  | 0.5        | 4   | RL             |
| Randomsearchbaseline‡  | 61.8 59.4 | 23  | 2          | 4   | random         |
| DARTS(firstorder)      | 60.2 57.6 | 23  | 0.5        | 4   | gradient-based |
| DARTS(secondorder)     | 58.1 55.7 | 23  | 1          | 4   | gradient-based |
*
Obtainedusingthecode(Phametal.,2018a)publiclyreleasedbytheauthors.
†
Obtainedbytrainingthecorrespondingarchitectureusingoursetup.
‡ Bestarchitectureamong8samplesaccordingtothevalidationperplexityafter300trainingepochs.
7

PublishedasaconferencepaperatICLR2019
Table3: Comparisonwithstate-of-the-artimageclassifiersonImageNetinthemobilesetting.
|     | TestError(%) | Params +× | SearchCost | Search |
| --- | ------------ | --------- | ---------- | ------ |
Architecture
|                                    | top-1 top-5 | (M) (M)  | (GPUdays) | Method         |
| ---------------------------------- | ----------- | -------- | --------- | -------------- |
| Inception-v1(Szegedyetal.,2015)    | 30.2 10.1   | 6.6 1448 | –         | manual         |
| MobileNet(Howardetal.,2017)        | 29.4 10.5   | 4.2 569  | –         | manual         |
| ShuffleNet2×(g=3)(Zhangetal.,2017) | 26.3 –      | ∼5 524   | –         | manual         |
| NASNet-A(Zophetal.,2018)           | 26.0 8.4    | 5.3 564  | 2000      | RL             |
| NASNet-B(Zophetal.,2018)           | 27.2 8.7    | 5.3 488  | 2000      | RL             |
| NASNet-C(Zophetal.,2018)           | 27.5 9.0    | 4.9 558  | 2000      | RL             |
| AmoebaNet-A(Realetal.,2018)        | 25.5 8.0    | 5.1 555  | 3150      | evolution      |
| AmoebaNet-B(Realetal.,2018)        | 26.0 8.5    | 5.3 555  | 3150      | evolution      |
| AmoebaNet-C(Realetal.,2018)        | 24.3 7.6    | 6.4 570  | 3150      | evolution      |
| PNAS(Liuetal.,2018a)               | 25.8 8.1    | 5.1 588  | ∼225      | SMBO           |
| DARTS(searchedonCIFAR-10)          | 26.7 8.7    | 4.7 574  | 4         | gradient-based |
3.3 RESULTSANALYSIS
TheCIFAR-10resultsforconvolutionalarchitecturesarepresentedinTable1. Notably,DARTS
achievedcomparableresultswiththestateoftheart(Zophetal.,2018;Realetal.,2018)whileusing
threeordersofmagnitudelesscomputationresources(i.e. 1.5or4GPUdaysvs2000GPUdaysfor
NASNetand3150GPUdaysforAmoebaNet). Moreover,withslightlylongersearchtime,DARTS
outperformedENAS(Phametal.,2018b)bydiscoveringcellswithcomparableerrorratesbutless
parameters. Thelongersearchtimeisduetothefactthatwehaverepeatedthesearchprocessfour
timesforcellselection. Thispracticeislessimportantforconvolutionalcellshowever,becausethe
performanceofdiscoveredarchitecturesdoesnotstronglydependoninitialization(Fig. 3).
AlternativeOptimizationStrategies Tobetterunderstandthenecessityofbileveloptimization,
weinvestigatedasimplisticsearchstrategy,whereαandwarejointlyoptimizedovertheunionof
thetrainingandvalidationsetsusingcoordinatedescent. Theresultingbestconvolutionalcell(outof
4runs)yielded4.16±0.16%testerrorusing3.1Mparameters,whichisworsethanrandomsearch.
Inthesecondexperiment,weoptimizedαsimultaneouslywithw(withoutalteration)usingSGD,
againoverallthedataavailable(training+validation). Theresultingbestcellyielded3.56±0.10%
testerrorusing3.0Mparameters. Wehypothesizethattheseheuristicswouldcauseα(analogous
tohyperparameters)tooverfitthetrainingdata,leadingtopoorgeneralization. Notethatαisnot
directlyoptimizedonthetrainingsetinDARTS.
Table2presentstheresultsforrecurrentarchitecturesonPTB,whereacelldiscoveredbyDARTS
achievedthetestperplexityof55.7. Thisisonparwiththestate-of-the-artmodelenhancedbya
mixtureofsoftmaxes(Yangetal.,2018),andbetterthanalltherestofthearchitecturesthatareeither
manuallyorautomaticallydiscovered. Notethatourautomaticallysearchedcelloutperformsthe
extensivelytunedLSTM(Melisetal.,2018),demonstratingtheimportanceofarchitecturesearchin
additiontohyperparametersearch. Intermsofefficiency,theoverallcost(4runsintotal)iswithin1
GPUday,whichiscomparabletoENASandsignificantlyfasterthanNAS(Zoph&Le,2017).
Itisalsointerestingtonotethatrandomsearchiscompetitiveforbothconvolutionalandrecurrent
models,whichreflectstheimportanceofthesearchspacedesign. Nevertheless,withcomparableor
lesssearchcost,DARTSisabletosignificantlyimproveuponrandomsearchinbothcases(2.76±
0.09vs3.29±0.15onCIFAR-10;55.7vs59.4onPTB).
ResultsinTable3showthatthecelllearnedonCIFAR-10isindeedtransferabletoImageNet. Itis
worthnoticingthatDARTSachievescompetitiveperformancewiththestate-of-the-artRLmethod
(Zophetal.,2018)whileusingthreeordersofmagnitudelesscomputationresources.
Table4showsthatthecellidentifiedbyDARTStransferstoWT2betterthanENAS,althoughthe
overallresultsarelessstrongthanthosepresentedinTable2forPTB.Theweakertransferability
betweenPTBandWT2(ascomparedtothatbetweenCIFAR-10andImageNet)couldbeexplainedby
therelativelysmallsizeofthesourcedataset(PTB)forarchitecturesearch.Theissueoftransferability
couldpotentiallybecircumventedbydirectlyoptimizingthearchitectureonthetaskofinterest.
8

PublishedasaconferencepaperatICLR2019
Table4: Comparisonwithstate-of-the-artlanguagemodelsonWT2.
|     |     | Perplexity | Params SearchCost | Search |
| --- | --- | ---------- | ----------------- | ------ |
Architecture
|                                    |     | valid test | (M) (GPUdays) | Method |
| ---------------------------------- | --- | ---------- | ------------- | ------ |
| LSTM+augmentedloss(Inanetal.,2017) |     | 91.5 87.0  | 28 –          | manual |
LSTM+continuouscachepointer(Graveetal.,2016) – 68.9 – – manual
| LSTM(Merityetal.,2018)                |     | 69.1 66.0 | 33 –   | manual         |
| ------------------------------------- | --- | --------- | ------ | -------------- |
| LSTM+skipconnections(Melisetal.,2018) |     | 69.1 65.9 | 24 –   | manual         |
| LSTM+15softmaxexperts(Yangetal.,2018) |     | 66.0 63.3 | 33 –   | manual         |
| ENAS(Phametal.,2018b)†(searchedonPTB) |     | 72.4 70.4 | 33 0.5 | RL             |
| DARTS(searchedonPTB)                  |     | 71.2 69.6 | 33 1   | gradient-based |
†
Obtainedbytrainingthecorrespondingarchitectureusingoursetup.
4 CONCLUSION
WepresentedDARTS,asimpleyetefficientarchitecturesearchalgorithmforbothconvolutionaland
recurrentnetworks. Bysearchinginacontinuousspace,DARTSisabletomatchoroutperformthe
state-of-the-artnon-differentiablearchitecturesearchmethodsonimageclassificationandlanguage
modelingtaskswithremarkableefficiencyimprovementbyseveralordersofmagnitude.
TherearemanyinterestingdirectionstoimproveDARTSfurther. Forexample,thecurrentmethod
maysufferfromdiscrepanciesbetweenthecontinuousarchitectureencodingandthederiveddiscrete
architecture. Thiscouldbealleviated,e.g.,byannealingthesoftmaxtemperature(withasuitable
schedule)toenforceone-hotselection. Itwouldalsobeinterestingtoinvestigateperformance-aware
architecturederivationschemesbasedonthesharedparameterslearnedduringthesearchprocess.
ACKNOWLEDGEMENTS
TheauthorswouldliketothankZihangDai,HieuPhamandZicoKolterforusefuldiscussions.
REFERENCES
KarimAhmedandLorenzoTorresani.Connectivitylearninginmulti-branchnetworks.arXivpreprint
arXiv:1709.09582,2017.
AnnalsofOperations
| GAnandalingamandTLFriesz. | Hierarchicaloptimization: |     | Anintroduction. |     |
| ------------------------- | ------------------------- | --- | --------------- | --- |
Research,34(1):1–11,1992.
BowenBaker,OtkristGupta,NikhilNaik,andRameshRaskar. Designingneuralnetworkarchitec-
| turesusingreinforcementlearning. | ICLR,2017. |     |     |     |
| -------------------------------- | ---------- | --- | --- | --- |
BowenBaker, OtkristGupta, RameshRaskar, andNikhilNaik. Acceleratingneuralarchitecture
| searchusingperformanceprediction. | ICLRWorkshop,2018. |     |     |     |
| --------------------------------- | ------------------ | --- | --- | --- |
GabrielBender,Pieter-JanKindermans,BarretZoph,VijayVasudevan,andQuocLe. Understanding
andsimplifyingone-shotarchitecturesearch. InInternationalConferenceonMachineLearning,
pp.549–558,2018.
Andrew Brock, Theodore Lim, James M Ritchie, and Nick Weston. Smash: one-shot model
| architecturesearchthroughhypernetworks. |     | ICLR,2018. |     |     |
| --------------------------------------- | --- | ---------- | --- | --- |
HanCai,TianyaoChen,WeinanZhang,YongYu,andJunWang. Efficientarchitecturesearchby
| networktransformation. AAAI,2018. |     |     |     |     |
| --------------------------------- | --- | --- | --- | --- |
BenoîtColson,PatriceMarcotte,andGillesSavard. Anoverviewofbileveloptimization. Annalsof
operationsresearch,153(1):235–256,2007.
TerranceDeVriesandGrahamWTaylor. Improvedregularizationofconvolutionalneuralnetworks
withcutout. arXivpreprintarXiv:1708.04552,2017.
9

PublishedasaconferencepaperatICLR2019
ThomasElsken,Jan-HendrikMetzen,andFrankHutter. Simpleandefficientarchitecturesearchfor
| convolutionalneuralnetworks. | arXivpreprintarXiv:1711.04528,2017. |     |
| ---------------------------- | ----------------------------------- | --- |
ChelseaFinn,PieterAbbeel,andSergeyLevine. Model-agnosticmeta-learningforfastadaptationof
deepnetworks. InICML,pp.1126–1135,2017.
LucaFranceschi,PaoloFrasconi,SaverioSalzo,andMassimilanoPontil. Bilevelprogrammingfor
hyperparameteroptimizationandmeta-learning. ICML,2018.
YarinGalandZoubinGhahramani. Atheoreticallygroundedapplicationofdropoutinrecurrent
neuralnetworks. InNIPS,pp.1019–1027,2016.
EdouardGrave, ArmandJoulin, andNicolasUsunier. Improvingneurallanguagemodelswitha
| continuouscache. arXivpreprintarXiv:1612.04426,2016. |     |     |
| ---------------------------------------------------- | --- | --- |
AndrewGHoward,MenglongZhu,BoChen,DmitryKalenichenko,WeijunWang,TobiasWeyand,
MarcoAndreetto,andHartwigAdam. Mobilenets: Efficientconvolutionalneuralnetworksfor
| mobilevisionapplications. | arXivpreprintarXiv:1704.04861,2017. |     |
| ------------------------- | ----------------------------------- | --- |
GaoHuang,ZhuangLiu,KilianQWeinberger,andLaurensvanderMaaten. Denselyconnected
| convolutionalnetworks. | InCVPR,2017. |     |
| ---------------------- | ------------ | --- |
HakanInan,KhashayarKhosravi,andRichardSocher. Tyingwordvectorsandwordclassifiers: A
lossframeworkforlanguagemodeling. ICLR,2017.
SergeyIoffeandChristianSzegedy. Batchnormalization: Acceleratingdeepnetworktrainingby
| reducinginternalcovariateshift. | arXivpreprintarXiv:1502.03167,2015. |     |
| ------------------------------- | ----------------------------------- | --- |
KirthevasanKandasamy,WillieNeiswanger,JeffSchneider,BarnabasPoczos,andEricXing. Neural
| architecturesearchwithbayesianoptimisationandoptimaltransport. |     | NIPS,2018. |
| -------------------------------------------------------------- | --- | ---------- |
DiederikPKingmaandJimmyBa. Adam: Amethodforstochasticoptimization. arXivpreprint
arXiv:1412.6980,2014.
BenKrause,EmmanuelKahembwe,IainMurray,andSteveRenals. Dynamicevaluationofneural
| sequencemodels. arXivpreprintarXiv:1709.07432,2017. |     |     |
| --------------------------------------------------- | --- | --- |
ChenxiLiu,BarretZoph,JonathonShlens,WeiHua,Li-JiaLi,LiFei-Fei,AlanYuille,Jonathan
| Huang,andKevinMurphy. | Progressiveneuralarchitecturesearch. | ECCV,2018a. |
| --------------------- | ------------------------------------ | ----------- |
HanxiaoLiu,KarenSimonyan,OriolVinyals,ChrisanthaFernando,andKorayKavukcuoglu. Hierar-
chicalrepresentationsforefficientarchitecturesearch. ICLR,2018b.
Ilya Loshchilov and Frank Hutter. Sgdr: Stochastic gradient descent with warm restarts. arXiv
preprintarXiv:1608.03983,2016.
JelenaLuketina,MathiasBerglund,KlausGreff,andTapaniRaiko. Scalablegradient-basedtuning
ofcontinuousregularizationhyperparameters. InICML,pp.2952–2960,2016.
DougalMaclaurin,DavidDuvenaud,andRyanAdams. Gradient-basedhyperparameteroptimization
| throughreversiblelearning. | InICML,pp.2113–2122,2015. |     |
| -------------------------- | ------------------------- | --- |
GáborMelis,ChrisDyer,andPhilBlunsom. Onthestateoftheartofevaluationinneurallanguage
models. ICLR,2018.
Stephen Merity, Nitish Shirish Keskar, and Richard Socher. Regularizing and optimizing lstm
| languagemodels. ICLR,2018. |     |     |
| -------------------------- | --- | --- |
Luke Metz, Ben Poole, David Pfau, and Jascha Sohl-Dickstein. Unrolled generative adversarial
networks. ICLR,2017.
Renato Negrinho and Geoff Gordon. Deeparchitect: Automatically designing and training deep
architectures. arXivpreprintarXiv:1704.08792,2017.
10

PublishedasaconferencepaperatICLR2019
Adam Paszke, Sam Gross, Soumith Chintala, Gregory Chanan, Edward Yang, Zachary DeVito,
Zeming Lin, Alban Desmaison, Luca Antiga, and Adam Lerer. Automatic differentiation in
pytorch. InNIPS-W,2017.
FabianPedregosa. Hyperparameteroptimizationwithapproximategradient. InICML,2016.
HieuPham,MelodyYGuan,BarretZoph,QuocVLe,andJeffDean. Authors’implementation
of “Efficient Neural Architecture Search via Parameter Sharing”. https://github.com/
melodyguan/enas/tree/2734eb2657847f090e1bc5c51c2b9cbf0be51887,
2018a. Accessed: 2018-04-05.
HieuPham,MelodyYGuan,BarretZoph,QuocVLe,andJeffDean. Efficientneuralarchitecture
searchviaparametersharing. ICML,2018b.
BorisTPolyakandAnatoliBJuditsky. Accelerationofstochasticapproximationbyaveraging. SIAM
JournalonControlandOptimization,30(4):838–855,1992.
EstebanReal,AlokAggarwal,YanpingHuang,andQuocVLe. Regularizedevolutionforimage
classifierarchitecturesearch. arXivpreprintarXiv:1802.01548,2018.
ShreyasSaxenaandJakobVerbeek. Convolutionalneuralfabrics. InNIPS,pp.4053–4061,2016.
RichardShin,CharlesPacker,andDawnSong. Differentiableneuralnetworkarchitecturesearch. In
ICLRWorkshop,2018.
ChristianSzegedy,WeiLiu,YangqingJia,PierreSermanet,ScottReed,DragomirAnguelov,Dumitru
Erhan,VincentVanhoucke,AndrewRabinovich,Jen-HaoRickChang,etal. Goingdeeperwith
convolutions. InCVPR,2015.
TomVeniatandLudovicDenoyer. Learningtime/memory-efficientdeeparchitectureswithbudgeted
supernetworks. arXivpreprintarXiv:1706.00046,2017.
Zhilin Yang, Zihang Dai, Ruslan Salakhutdinov, and William W Cohen. Breaking the softmax
bottleneck: ahigh-rankrnnlanguagemodel. ICLR,2018.
Xiangyu Zhang, Xinyu Zhou, Mengxiao Lin, and Jian Sun. Shufflenet: An extremely efficient
convolutionalneuralnetworkformobiledevices. arXivpreprintarXiv:1707.01083,2017.
ZhaoZhong,JunjieYan,WeiWu,JingShao,andCheng-LinLiu.Practicalblock-wiseneuralnetwork
architecturegeneration. InProceedingsoftheIEEEConferenceonComputerVisionandPattern
Recognition,pp.2423–2432,2018.
JulianGeorgZilly, RupeshKumarSrivastava, JanKoutník, andJürgenSchmidhuber. Recurrent
highwaynetworks. arXivpreprintarXiv:1607.03474,2016.
BarretZophandQuocVLe. Neuralarchitecturesearchwithreinforcementlearning. ICLR,2017.
BarretZoph,VijayVasudevan,JonathonShlens,andQuocVLe. Learningtransferablearchitectures
forscalableimagerecognition. CVPR,2018.
11

PublishedasaconferencepaperatICLR2019
A EXPERIMENTAL DETAILS
A.1 ARCHITECTURESEARCH
A.1.1 CIFAR-10
Sincethearchitecturewillbevaryingthroughoutthesearchprocess,wealwaysusebatch-specific
statisticsforbatchnormalizationratherthantheglobalmovingaverage. Learnableaffineparameters
inallbatchnormalizationsaredisabledduringthesearchprocesstoavoidrescalingtheoutputsofthe
candidateoperations.
Tocarryoutarchitecturesearch,weholdouthalfoftheCIFAR-10trainingdataasthevalidation
set. Asmallnetworkof8cellsistrainedusingDARTSfor50epochs,withbatchsize64(forboth
thetrainingandvalidationsets)andtheinitialnumberofchannels16. Thenumberswerechosento
ensurethenetworkcanfitintoasingleGPU.WeusemomentumSGDtooptimizetheweightsw,
withinitiallearningrateη = 0.025(annealeddowntozerofollowingacosineschedulewithout
w
restart (Loshchilov & Hutter, 2016)), momentum 0.9, and weight decay 3×10−4. We use zero
initializationforarchitecturevariables(theα’sinboththenormalandreductioncells),whichimplies
equalamountofattention(aftertakingthesoftmax)overallpossibleops. Attheearlystagethis
ensuresweightsineverycandidateoptoreceivesufficientlearningsignal(moreexploration). We
useAdam(Kingma&Ba,2014)astheoptimizerforα,withinitiallearningrateη = 3×10−4,
α
momentumβ =(0.5,0.999)andweightdecay10−3. ThesearchtakesonedayonasingleGPU3.
A.1.2 PTB
Forarchitecturesearch,boththeembeddingandthehiddensizesaresetto300. Thelineartransfor-
mationparametersacrossallincomingoperationsconnectedtothesamenodeareshared(theirshapes
areall300×300),asthealgorithmalwayshastheoptiontofocusononeofthepredecessorsand
maskawaytheothers. Tyingtheweightsleadstomemorysavingsandfastercomputation,allowing
us to train the continuous architecture using a single GPU. Learnable affine parameters in batch
normalizationsaredisabled,aswedidforconvolutionalcells. Thenetworkisthentrainedfor50
epochsusingSGDwithoutmomentum,withlearningrateη = 20,batchsize256,BPTTlength
w
35, andweightdecay5×10−7. Weapplyvariationaldropout(Gal&Ghahramani,2016)of0.2
towordembeddings,0.75tothecellinput,and0.25toallthehiddennodes. Adropoutof0.75is
alsoappliedtotheoutputlayer. OthertrainingsettingsareidenticaltothoseinMerityetal.(2018);
Yangetal.(2018). Similarlytotheconvolutionalarchitectures,weuseAdamfortheoptimizationof
α(initializedaszeros),withinitiallearningrateη =3×10−3,momentumβ =(0.9,0.999)and
α
weightdecay10−3. Thesearchtakes6hoursonasingleGPU.
A.2 ARCHITECTUREEVALUATION
A.2.1 CIFAR-10
A large network of 20 cells is trained for 600 epochs with batch size 96. The initial number of
channelsisincreasedfrom16to36toensureourmodelsizeiscomparablewithotherbaselinesin
theliterature(around3M).Otherhyperparametersremainthesameastheonesusedforarchitecture
search. Following existing works (Pham et al., 2018b; Zoph et al., 2018; Liu et al., 2018a; Real
etal.,2018), additionalenhancementsincludecutout(DeVries&Taylor,2017), pathdropoutof
probability0.2andauxiliarytowerswithweight0.4. Thetrainingtakes1.5daysonasingleGPU
withourimplementationinPyTorch(Paszkeetal.,2017). SincetheCIFARresultsaresubjectto
highvarianceevenwithexactlythesamesetup(Liuetal.,2018b),wereportthemeanandstandard
deviationof10independentrunsforourfullmodel.
Toavoidanydiscrepancybetweendifferentimplementationsortrainingsettings(e.g. thebatchsizes),
weincorporatedtheNASNet-Acell(Zophetal.,2018)andtheAmoebaNet-Acell(Realetal.,2018)
intoourtrainingframeworkandreportedtheirresultsunderthesamesettingsasourcells.
3AllofourexperimentswereperformedusingNVIDIAGTX1080TiGPUs.
12

PublishedasaconferencepaperatICLR2019
A.2.2 PTB
Asingle-layerrecurrentnetworkwiththediscoveredcellistraineduntilconvergencewithbatchsize
64usingaveragedSGD(Polyak&Juditsky,1992)(ASGD),withlearningrateη =20andweight
w
decay8×10−7. Tospeedup,westartwithSGDandtriggerASGDusingthesameprotocolasin
Yangetal.(2018);Merityetal.(2018). Boththeembeddingandthehiddensizesaresetto850to
ensureourmodelsizeiscomparablewithotherbaselines. Thetoken-wisedropoutontheembedding
layerissetto0.1. Otherhyperparametersremainexactlythesameasthoseforarchitecturesearch.
Forfaircomparison,wedonotfinetuneourmodelattheendoftheoptimization,nordoweuseany
additionalenhancementssuchasdynamicevaluation(Krauseetal.,2017)orcontinuouscache(Grave
etal.,2016). Thetrainingtakes3daysonasingle1080TiGPUwithourPyTorchimplementation. To
accountforimplementationdiscrepancies,wealsoincorporatedtheENAScell(Phametal.,2018b)
intoourcodebaseandtrainedtheirnetworkunderthesamesetupasourdiscoveredcells.
A.2.3 IMAGENET
Weconsiderthemobilesettingwheretheinputimagesizeis224×224andthenumberofmultiply-add
operationsinthemodelisrestrictedtobelessthan600M.
Anetworkof14cellsistrainedfor250epochswithbatchsize128,weightdecay3×10−5andinitial
SGDlearningrate0.1(decayedbyafactorof0.97aftereachepoch). Otherhyperparametersfollow
Zophetal.(2018);Realetal.(2018);Liuetal.(2018a)4. Thetrainingtakes12daysonasingleGPU.
A.2.4 WIKITEXT-2
Weuseembeddingandhiddensizes700,weightdecay5×10−7,andhidden-nodevariationaldropout
0.15. OtherhyperparametersremainthesameasinourPTBexperiments.
B SEARCH WITH INCREASED DEPTH
Tobetterunderstandtheeffectofdepthforarchitecturesearch,weconductedarchitecturesearchon
CIFAR-10byincreasingthenumberofcellsinthestackfrom8to20. Theinitialnumberofchannels
isreducedfrom16to6duetomemorybudgetofasingleGPU.Alltheotherhyperparametersremain
thesame. Thesearchcostdoublesandtheresultingcellachieves2.88±0.09%testerror,whichis
slightlyworsethan2.76±0.09%obtainedusingashallowernetwork. Thisparticularsetupmayhave
sufferedfromtheenlargeddiscrepancyofthenumberofchannelsbetweenarchitecturesearchand
finalevaluation. Moreover,searchingwithadeepermodelmightrequiredifferenthyperparameters
duetotheincreasednumberoflayerstoback-propthrough.
C COMPLEXITY ANALYSIS
Inthissection,weanalyzethecomplexityofoursearchspaceforconvolutionalcells.
Eachofourdiscretizedcellallows (cid:81)4 (k+1)k ×(72)≈109possibleDAGswithoutconsidering
k=1 2
graph isomorphism (recall we have 7 non-zero ops, 2 input nodes, 4 intermediate nodes with 2
predecessorseach). Sincewearejointlylearningbothnormalandreductioncells,thetotalnumber
ofarchitecturesisapproximately(109)2 =1018. Thisisgreaterthanthe 5.6×1014ofPNAS(Liu
etal.,2018a)whichlearnsonlyasingletypeofcell.
Alsonotethatweretainedthetop-2predecessorspernodeonlyattheveryend,andourcontinuous
searchspacebeforethisfinaldiscretizationstepisevenlarger. Specifically,eachrelaxedcell(afully
connected graph) contains 2+3+4+5 = 14 learnable edges, allowing (7+1)14 ≈ 4×1012
possibleconfigurations(+1toincludethezeroopindicatingalackofconnection). Again,since
wearelearningbothnormalandreductioncells,thetotalnumberofarchitecturescoveredbythe
continuousspacebeforediscretizationis(4×1012)2 ≈1025.
4Wedidnotconductextensivehyperparametertuning.
13