| Identity | Mappings |     | in Deep | Residual | Networks |
| -------- | -------- | --- | ------- | -------- | -------- |
6102 luJ 52  ]VC.sc[  3v72050.3061:viXra
|     | Kaiming | He, Xiangyu | Zhang,    | Shaoqing Ren, | and Jian Sun |
| --- | ------- | ----------- | --------- | ------------- | ------------ |
|     |         |             | Microsoft | Research      |              |
Abstract Deep residual networks [1] have emerged as a family of ex-
tremely deep architectures showing compelling accuracy and nice con-
vergence behaviors. In this paper, we analyze the propagation formu-
lations behind the residual building blocks, which suggest that the for-
ward and backward signals can be directly propagated from one block
to any other block, when using identity mappings as the skip connec-
tionsandafter-additionactivation.Aseriesofablationexperimentssup-
port the importance of these identity mappings. This motivates us to
propose a new residual unit, which makes training easier and improves
generalization. We report improved results using a 1001-layer ResNet
on CIFAR-10 (4.62% error) and CIFAR-100, and a 200-layer ResNet
on ImageNet. Code is available at: https://github.com/KaimingHe/
resnet-1k-layers.
1 Introduction
Deep residual networks (ResNets) [1] consist of many stacked “Residual Units”.
| Each unit | (Fig. 1 (a)) | can be | expressed  | in a general | form: |
| --------- | ------------ | ------ | ---------- | ------------ | ----- |
|           |              | y      | =h(x )+F(x | ,W ),        |       |
|           |              |        | l l        | l l          |       |
|           |              |        | x =f(y     | ),           |       |
|           |              |        | l+1        | l            |       |
where x l and x l+1 are input and output of the l-th unit, and F is a residual
function. In [1], h(x )=x is an identity mapping and f is a ReLU [2] function.
l l
ResNetsthatareover100-layerdeephaveshownstate-of-the-artaccuracyfor
severalchallengingrecognitiontasksonImageNet[3]andMSCOCO[4]compe-
titions. The central idea of ResNets is to learn the additive residual function F
withrespecttoh(x l ),withakeychoiceofusinganidentitymappingh(x l )=x l .
This is realized by attaching an identity skip connection (“shortcut”).
In this paper, we analyze deep residual networks by focusing on creating a
“direct” path for propagating information — not only within a residual unit,
but through the entire network. Our derivations reveal that if both h(x ) and
l
f(y l ) are identity mappings, the signal could be directly propagated from one
unit to any other units, in both forward and backward passes. Our experiments
empirically show that training in general becomes easier when the architecture
| is closer | to the above | two conditions. |     |     |     |
| --------- | ------------ | --------------- | --- | --- | --- |
To understand the role of skip connections, we analyze and compare various
types of h(x l ). We find that the identity mapping h(x l ) = x l chosen in [1]

2
|     |     | 2   |     |     |   20 |
| --- | --- | --- | --- | --- | ---- |
ResNet−1001, original (error: 7.61%)
| xl  | xl  |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
ResNet−1001, proposed (error: 4.92%)
| weight | BN  |     |     |     |     |
| ------ | --- | --- | --- | --- | --- |
15
| BN   | ReLU   | 0.2           |     |     |                |
| ---- | ------ | ------------- | --- | --- | -------------- |
|      |        | ssoL gniniarT |     |     | Test Error (%) |
| ReLU | weight |               |     |     |                |
10
| weight | BN   |     |     |     |     |
| ------ | ---- | --- | --- | --- | --- |
| BN     | ReLU |     |     |     |     |
0.02
| addition | weight |     |     |     |     |
| -------- | ------ | --- | --- | --- | --- |
5
| ReLU         | addition     |        |            |     |       |
| ------------ | ------------ | ------ | ---------- | --- | ----- |
| xl+1         | xl+1         |        |            |     |       |
|              |              | 0.002  |            |     | 0     |
| (a) original | (b) proposed | 0 1    | 2 3        | 4 5 | 6     |
|              |              |        | Iterations |     | x 104 |
Figure1.Left:(a)originalResidualUnitin[1];(b)proposedResidualUnit.Thegrey
arrows indicate the easiest paths for the information to propagate, corresponding to
the additive term “x” l in Eqn.(4) (forward propagation) and the additive term “1” in
Eqn.(5) (backward propagation). Right: training curves on CIFAR-10 of 1001-layer
ResNets. Solid lines denote test error (y-axis on the right), and dashed lines denote
trainingloss(y-axisontheleft).TheproposedunitmakesResNet-1001easiertotrain.
achieves the fastest error reduction and lowest training loss among all variants
we investigated, whereas skip connections of scaling, gating [5,6,7], and 1×1
convolutionsallleadtohighertraininglossanderror.Theseexperimentssuggest
thatkeepinga“clean”informationpath(indicatedbythegreyarrowsinFig.1,2,
| and 4) is helpful | for easing optimization. |     |     |     |     |
| ----------------- | ------------------------ | --- | --- | --- | --- |
To construct an identity mapping f(y ) = y , we view the activation func-
l l
tions (ReLU and BN [8]) as “pre-activation” of the weight layers, in contrast
to conventional wisdom of “post-activation”. This point of view leads to a new
residual unit design, shown in (Fig. 1(b)). Based on this unit, we present com-
petitiveresultsonCIFAR-10/100witha1001-layerResNet,whichismucheasier
totrainandgeneralizesbetterthantheoriginalResNetin[1].Wefurtherreport
improved results on ImageNet using a 200-layer ResNet, for which the counter-
part of [1] starts to overfit. These results suggest that there is much room to
exploit the dimension of network depth, a key to the success of modern deep
learning.
| 2 Analysis | of Deep | Residual | Networks |     |     |
| ---------- | ------- | -------- | -------- | --- | --- |
The ResNets developed in [1] are modularized architectures that stack building
blocksofthesameconnectingshape.Inthispaperwecalltheseblocks“Residual

3
Units”. The original Residual Unit in [1] performs the following computation:
|     |     |     |     | y l =h(x | l )+F(x  | l ,W | l ), |     | (1) |
| --- | --- | --- | --- | -------- | -------- | ---- | ---- | --- | --- |
|     |     |     |     | x        | l+1 =f(y | l ). |      |     | (2) |
Here x is the input feature to the l-th Residual Unit. W ={W | } is a
| l   |     |     |     |     |     |     |     | l l,k 1≤k≤K |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- |
set of weights (and biases) associated with the l-th Residual Unit, and K is the
number of layers in a Residual Unit (K is 2 or 3 in [1]). F denotes the residual
function, e.g., a stack of two 3×3 convolutional layers in [1]. The function f is
the operation after element-wise addition, and in [1] f is ReLU. The function h
| is set as | an identity |     | mapping: | h(x | )=x | .1  |     |     |     |
| --------- | ----------- | --- | -------- | --- | --- | --- | --- | --- | --- |
|           |             |     |          |     | l   | l   |     |     |     |
If f is also an identity mapping: x ≡y , we can put Eqn.(2) into Eqn.(1)
|     |     |     |     |     | l+1 | l   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
and obtain:
|             |     |     |        | x =x | +F(x | ,W            | ).  |             | (3) |
| ----------- | --- | --- | ------ | ---- | ---- | ------------- | --- | ----------- | --- |
|             |     |     |        | l+1  | l    | l             | l   |             |     |
| Recursively | (x  | =   | x +F(x | ,W   | ) =  | x +F(x,W)+F(x |     | ,W ), etc.) | we  |
|             |     | l+2 | l+1    | l+1  | l+1  | l             | l l | l+1 l+1     |     |
will have:
L−1
(cid:88)
|     |     |     |     | x =x | +   | F(x ,W | ),  |     | (4) |
| --- | --- | --- | --- | ---- | --- | ------ | --- | --- | --- |
|     |     |     |     | L    | l   | i      | i   |     |     |
i=l
for any deeper unit L and any shallower unit l. Eqn.(4) exhibits some nice
properties. (i) The feature x of any deeper unit L can be represented as the
L
(cid:80)L−1F,
feature x l of any shallower unit l plus a residual function in a form of
i=l
indicatingthatthemodelisinaresidual fashionbetweenanyunitsLandl.(ii)
(cid:80)L−1F(x
The feature x L = x 0 + i ,W i ), of any deep unit L, is the summation
i=0
oftheoutputsofallprecedingresidualfunctions(plusx ).Thisisincontrastto
0
a “plain network” where a feature x is a series of matrix-vector products, say,
L
(cid:81)L−1W
|     | x (ignoring |     | BN  | and ReLU). |     |     |     |     |     |
| --- | ----------- | --- | --- | ---------- | --- | --- | --- | --- | --- |
| i=0 | i 0         |     |     |            |     |     |     |     |     |
Eqn.(4) also leads to nice backward propagation properties. Denoting the
loss function as E, from the chain rule of backpropagation [9] we have:
|     |     |     |     |     | (cid:32) |     |     | (cid:33) |     |
| --- | --- | --- | --- | --- | -------- | --- | --- | -------- | --- |
L−1
|     |     | ∂E  | ∂E  | ∂x L  | ∂E  | ∂   | (cid:88) |        |     |
| --- | --- | --- | --- | ----- | --- | --- | -------- | ------ | --- |
|     |     | =   |     | =     |     | 1+  | F(x      | ,W ) . | (5) |
|     |     | ∂x  | ∂x  | ∂x ∂x |     | ∂x  |          | i i    |     |
|     |     | l   | L   | l     | L   | l   |          |        |     |
i=l
∂E
Eqn.(5) indicates that the gradient can be decomposed into two additive
∂xl
terms: a term of ∂E that propagates information directly without concern-
∂ x L
ing any weight lay e rs , and another term of ∂E (cid:16) ∂ (cid:80)L−1F (cid:17) that propagates
|     |     |     |     |     |     | ∂xL | ∂xl i=l |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- |
through the weight layers. The additive term of ∂E ensures that information is
∂xL
directly propagated back to any shallower unit l. Eqn.(5) also suggests that it
1 ItisnoteworthythatthereareResidualUnitsforincreasingdimensionsandreducing
featuremapsizes[1]inwhichhisnotidentity.Inthiscasethefollowingderivations
donotholdstrictly.Butasthereareonlyaveryfewsuchunits(twoonCIFARand
three on ImageNet, depending on image sizes [1]), we expect that they do not have
theexponentialimpactaswepresentinSec.3.Onemayalsothinkofourderivations
as applied to all Residual Units within the same feature map size.

4
is unlikely for the gradient ∂E to be canceled out for a mini-batch, because in
∂xl
generaltheterm ∂ (cid:80)L−1F cannotbealways-1forallsamplesinamini-batch.
|     |     | ∂xl | i=l |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
This implies that the gradient of a layer does not vanish even when the weights
| are arbitrarily | small. |     |     |     |     |     |     |     |
| --------------- | ------ | --- | --- | --- | --- | --- | --- | --- |
Discussions
Eqn.(4) and Eqn.(5) suggest that the signal can be directly propagated from
any unit to another, both forward and backward. The foundation of Eqn.(4) is
two identity mappings: (i) the identity skip connection h(x ) = x , and (ii) the
l l
| condition | that f | is an | identity | mapping. |     |     |     |     |
| --------- | ------ | ----- | -------- | -------- | --- | --- | --- | --- |
These directly propagated information flows are represented by the grey ar-
rows in Fig. 1, 2, and 4. And the above two conditions are true when these grey
arrows cover no operations (expect addition) and thus are “clean”. In the fol-
lowing two sections we separately investigate the impacts of the two conditions.
| 3 On | the Importance |     |     | of Identity |     | Skip Connections |     |     |
| ---- | -------------- | --- | --- | ----------- | --- | ---------------- | --- | --- |
Let’sconsiderasimplemodification,h(x )=λ x ,tobreaktheidentityshortcut:
|     |     |     |       |          | l    | l l       |     |     |
| --- | --- | --- | ----- | -------- | ---- | --------- | --- | --- |
|     |     |     | x l+1 | =λ l x l | +F(x | l ,W l ), |     | (6) |
where λ is a modulating scalar (for simplicity we still assume f is identity).
l
RecursivelyapplyingthisformulationweobtainanequationsimilartoEqn.(4):
x =( (cid:81)L−1λ )x + (cid:80)L−1( (cid:81)L−1 λ )F(x ,W ), or simply:
| L   | i=l i | l   | i=l j=i+1 | j    | i        | i          |     |     |
| --- | ----- | --- | --------- | ---- | -------- | ---------- | --- | --- |
|     |       |     | L−1       |      | L−1      |            |     |     |
|     |       |     | (cid:89)  |      | (cid:88) |            |     |     |
|     |       |     | x =(      | λ )x | +        | Fˆ(x ,W ), |     | (7) |
|     |       |     | L         | i l  |          | i i        |     |     |
|     |       |     | i=l       |      | i=l      |            |     |     |
where the notation Fˆ absorbs the scalars into the residual functions. Similar to
| Eqn.(5), | we have | backpropagation |          | of the   | following | form:    |          |     |
| -------- | ------- | --------------- | -------- | -------- | --------- | -------- | -------- | --- |
|          |         |                 | (cid:32) | L−1      |           | L−1      | (cid:33) |     |
|          |         | ∂E              | ∂E       | (cid:89) | ∂         | (cid:88) |          |     |
|          |         | =               |          | ( λ )+   |           | Fˆ(x ,W  | ) .      | (8) |
|          |         |                 |          | i        |           | i        | i        |     |
|          |         | ∂x l            | ∂x L     |          | ∂x l      |          |          |     |
|          |         |                 |          | i=l      |           | i=l      |          |     |
Unlike Eqn.(5), in Eqn.(8) the first additive term is modulated by a factor
(cid:81)L−1λ . For an extremely deep network (L is large), if λ > 1 for all i, this
| i   |     |     |     |     |     |     | i   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
i=l
factor can be exponentially large; if λ < 1 for all i, this factor can be expo-
i
nentially small and vanish, which blocks the backpropagated signal from the
shortcut and forces it to flow through the weight layers. This results in opti-
| mization | difficulties | as  | we show | by experiments. |     |     |     |     |
| -------- | ------------ | --- | ------- | --------------- | --- | --- | --- | --- |
In the above analysis, the original identity skip connection in Eqn.(3) is re-
placedwithasimplescalingh(x )=λ x .Iftheskipconnectionh(x )represents
|     |     |     |     | l l | l   |     | l   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
more complicated transforms (such as gating and 1×1 convolutions), in Eqn.(8)
(cid:81)L−1h(cid:48)
the first term becomes where h(cid:48) is the derivative of h. This product
|     |     |     | i=l | i   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
may also impede information propagation and hamper the training procedure
| as witnessed | in  | the following | experiments. |     |     |     |     |     |
| ------------ | --- | ------------- | ------------ | --- | --- | --- | --- | --- |

5
3x3 conv 3x3 conv
ReLU ReLU
3x3 conv 3x3 conv
0.5 0.5
addition addition
ReLU (a) original ReLU (b) constant scaling
3x3 conv 3x3 conv
ReLU ReLU
1x1 conv 3x3 conv 1x1 conv 3x3 conv
sigmoid sigmoid
1- 1-
addition addition
ReLU (c) exclusive gating ReLU (d) shortcut-only gating
3x3 conv 3x3 conv
ReLU ReLU
1x1 conv 3x3 conv dropout 3x3 conv
addition addition
ReLU (e) conv shortcut ReLU (f) dropout shortcut
Figure2. Various types of shortcut connections used in Table 1. The grey arrows
indicate the easiest paths for the information to propagate. The shortcut connections
in (b-f) are impeded by different components. For simplifying illustrations we do not
displaytheBNlayers,whichareadoptedrightaftertheweightlayersforallunitshere.
3.1 Experiments on Skip Connections
We experiment with the 110-layer ResNet as presented in [1] on CIFAR-10 [10].
This extremely deep ResNet-110 has 54 two-layer Residual Units (consisting of
3×3 convolutional layers) and is challenging for optimization. Our implementa-
tiondetails(seeappendix)arethesameas[1].Throughoutthispaperwereport
the median accuracy of 5 runs for each architecture on CIFAR, reducing the
impacts of random variations.
Though our above analysis is driven by identity f, the experiments in this
sectionareallbasedonf =ReLUasin[1];weaddressidentityf inthenextsec-
tion. Our baseline ResNet-110 has 6.61% error on the test set. The comparisons
of other variants (Fig. 2 and Table 1) are summarized as follows:
Constant scaling. We set λ=0.5 for all shortcuts (Fig. 2(b)). We further
studytwocasesofscalingF:(i)F isnotscaled;or(ii)F isscaledbyaconstant
scalarof1−λ=0.5,whichissimilartothehighwaygating[6,7]butwithfrozen
gates. The former case does not converge well; the latter is able to converge,
but the test error (Table 1, 12.35%) is substantially higher than the original
ResNet-110. Fig 3(a) shows that the training error is higher than that of the
original ResNet-110, suggesting that the optimization has difficulties when the
shortcut signal is scaled down.

6
Table 1. Classification error on the CIFAR-10 test set using ResNet-110 [1], with
different types of shortcut connections applied to all Residual Units. We report “fail”
| when | the         | test error | is higher | than | 20%.       |     |          |                 |
| ---- | ----------- | ---------- | --------- | ---- | ---------- | --- | -------- | --------------- |
|      |             | case       | Fig.      |      | onshortcut | onF | error(%) | remark          |
|      | original[1] |            | Fig.2(a)  |      | 1          | 1   | 6.61     |                 |
|      |             |            |           |      | 0          | 1   | fail     | Thisisaplainnet |
constant
|     |     |     | Fig.2(b) |     | 0.5 | 1   | fail |     |
| --- | --- | --- | -------- | --- | --- | --- | ---- | --- |
scaling
|     |                 |     |          |     | 0.5        | 0.5  | 12.35 | frozengating |
| --- | --------------- | --- | -------- | --- | ---------- | ---- | ----- | ------------ |
|     |                 |     |          |     | 1−g(x)     | g(x) | fail  | initbg=0to−5 |
|     | exclusive       |     | Fig.2(c) |     |            |      |       |              |
|     | gating          |     |          |     | 1−g(x)     | g(x) | 8.70  | initbg=-6    |
|     |                 |     |          |     | 1−g(x)     | g(x) | 9.81  | initbg=-7    |
|     |                 |     |          |     | 1−g(x)     | 1    | 12.86 |              |
|     | shortcut-only   |     |          |     |            |      |       | initbg=0     |
|     | gating          |     | Fig.2(d) |     |            |      |       |              |
|     |                 |     |          |     | 1−g(x)     | 1    | 6.91  | initbg=-6    |
|     | 1×1convshortcut |     | Fig.2(e) |     | 1×1conv    | 1    | 12.22 |              |
|     | dropoutshortcut |     | Fig.2(f) |     | dropout0.5 | 1    | fail  |              |
Exclusivegating.FollowingtheHighwayNetworks[6,7]thatadoptagating
mechanism [5], we consider a gating function g(x) = σ(W x + b ) where a
|     |     |     |     |     |     |     |     | g g |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
transform is represented by weights W and biases b followed by the sigmoid
|     |     |     |     |     | g   |     | g   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
function σ(x) = 1 . In a convolutional network g(x) is realized by a 1×1
1+e−x
convolutional layer. The gating function modulates the signal by element-wise
multiplication.
We investigate the “exclusive” gates as used in [6,7] — the F path is scaled
byg(x)andtheshortcutpathisscaledby1−g(x).SeeFig2(c).Wefindthatthe
initialization of the biases b is critical for training gated models, and following
g
theguidelines2
in[6,7],weconducthyper-parametersearchontheinitialvalueof
b intherangeof0to-10withadecrementstepof-1onthetrainingsetbycross-
g
validation. The best value (−6 here) is then used for training on the training
set, leading to a test result of 8.70% (Table 1), which still lags far behind the
ResNet-110baseline.Fig3(b)showsthetrainingcurves.Table1alsoreportsthe
resultsofusingotherinitializedvalues,notingthattheexclusivegatingnetwork
does not converge to a good solution when b is not appropriately initialized.
g
The impact of the exclusive gating mechanism is two-fold. When 1−g(x)
approaches 1, the gated shortcut connections are closer to identity which helps
information propagation; but in this case g(x) approaches 0 and suppresses the
function F. To isolate the effects of the gating functions on the shortcut path
alone, we investigate a non-exclusive gating mechanism in the next.
Shortcut-only gating. In this case the function F is not scaled; only the
shortcutpathisgatedby1−g(x).SeeFig2(d).Theinitializedvalueofb isstill
g
essential in this case. When the initialized b is 0 (so initially the expectation
g
of 1−g(x) is 0.5), the network converges to a poor result of 12.86% (Table 1).
| This | is also | caused | by higher | training | error | (Fig 3(c)). |     |     |
| ---- | ------- | ------ | --------- | -------- | ----- | ----------- | --- | --- |
2
See also: people.idsia.ch/~rupesh/very_deep_learning/ by [6,7].

7
| 2             |               |     |     |     |   20 2         |               |     |     |   20           |
| ------------- | ------------- | --- | --- | --- | -------------- | ------------- | --- | --- | -------------- |
|               |               |     |     |     | 15             |               |     |     | 15             |
| 0.2           |               |     |     |     | 0.2            |               |     |     |                |
|               |               |     |     |     | Test Error (%) |               |     |     | Test Error (%) |
| ssoL gniniarT |               |     |     |     | ssoL gniniarT  |               |     |     |                |
|               |               |     |     |     | 10             |               |     |     | 10             |
| 0.02          |               |     |     |     | 0.02           |               |     |     |                |
|               |               |     |     |     | 5              |               |     |     | 5              |
|               | 110, original |     |     |     |                | 110, original |     |     |                |
110, const scaling (0.5, 0.5) 110, exclusive gating (init b=−6)
| 0.002  0      | 1 2                                  | 3          | 4 5 | 6     | 0 0.002  0                   | 1 2                    | 3 4        | 5   | 6 0            |
| ------------- | ------------------------------------ | ---------- | --- | ----- | ---------------------------- | ---------------------- | ---------- | --- | -------------- |
|               |                                      | Iterations |     | x 104 |                              |                        | Iterations |     | x 104          |
|               |                                      | (a)        |     |       |                              |                        | (b)        |     |                |
| 2             |                                      |            |     |       |   20 2                       |                        |            |     |   20           |
|               |                                      |            |     |       | 15                           |                        |            |     | 15             |
| 0.2           |                                      |            |     |       | 0.2                          |                        |            |     |                |
| ssoL gniniarT |                                      |            |     |       | Test Error (%) ssoL gniniarT |                        |            |     | Test Error (%) |
|               |                                      |            |     |       | 10                           |                        |            |     | 10             |
| 0.02          |                                      |            |     |       | 0.02                         |                        |            |     |                |
|               |                                      |            |     |       | 5                            |                        |            |     | 5              |
|               | 110, original                        |            |     |       |                              | 110, original          |            |     |                |
|               | 110, shortcut−only gating (init b=0) |            |     |       |                              | 110, 1x1 conv shortcut |            |     |                |
| 0.002         |                                      |            |     |       | 0 0.002                      |                        |            |     | 0              |
| 0             | 1 2                                  | 3          | 4 5 | 6     | 0                            | 1 2                    | 3 4        | 5   | 6              |
|               |                                      | Iterations |     | x 104 |                              |                        | Iterations |     | x 104          |
|               |                                      | (c)        |     |       |                              |                        | (d)        |     |                |
Figure3. Training curves on CIFAR-10 of various shortcuts. Solid lines denote test
error (y-axis on the right), and dashed lines denote training loss (y-axis on the left).
When the initialized b g is very negatively biased (e.g., −6), the value of
1−g(x)iscloserto1andtheshortcutconnectionisnearlyanidentitymapping.
Therefore,theresult(6.91%,Table1)ismuchclosertotheResNet-110baseline.
1×1 convolutional shortcut. Next we experiment with 1×1 convolutional
shortcutconnectionsthatreplacetheidentity.Thisoptionhasbeeninvestigated
in [1] (known as option C) on a 34-layer ResNet (16 Residual Units) and shows
good results, suggesting that 1×1 shortcut connections could be useful. But we
findthatthisisnotthecasewhentherearemanyResidualUnits.The110-layer
ResNet has a poorer result (12.22%, Table 1) when using 1×1 convolutional
shortcuts. Again, the training error becomes higher (Fig 3(d)). When stacking
so many Residual Units (54 for ResNet-110), even the shortest path may still
impede signal propagation. We witnessed similar phenomena on ImageNet with
| ResNet-101 | when | using | 1×1 | convolutional | shortcuts. |     |     |     |     |
| ---------- | ---- | ----- | --- | ------------- | ---------- | --- | --- | --- | --- |
Dropout shortcut.Lastweexperimentwithdropout[11](ataratioof0.5)
which we adopt on the output of the identity shortcut (Fig. 2(f)). The network
fails to converge to a good solution. Dropout statistically imposes a scale of λ
with an expectation of 0.5 on the shortcut, and similar to constant scaling by
| 0.5, it impedes |     | signal | propagation. |     |     |     |     |     |     |
| --------------- | --- | ------ | ------------ | --- | --- | --- | --- | --- | --- |

8
Table 2. Classification error (%) on the CIFAR-10 test set using different activation
functions.
|          |        | case                    |        |          | Fig.     | ResNet-110 |        | ResNet-164 |        |
| -------- | ------ | ----------------------- | ------ | -------- | -------- | ---------- | ------ | ---------- | ------ |
|          |        | originalResidualUnit[1] |        |          | Fig.4(a) | 6.61       |        | 5.93       |        |
|          |        | BNafteraddition         |        |          | Fig.4(b) | 8.17       |        | 6.50       |        |
|          |        | ReLUbeforeaddition      |        |          | Fig.4(c) | 7.84       |        | 6.14       |        |
|          |        | ReLU-onlypre-activation |        |          | Fig.4(d) | 6.71       |        | 5.91       |        |
|          |        | full pre-activation     |        |          | Fig.4(e) | 6.37       |        | 5.46       |        |
| xl       |        | xl                      |        | xl       |          | xl         |        | xl         |        |
|          | weight |                         | weight |          | weight   |            | ReLU   |            | BN     |
|          | BN     |                         | BN     |          | BN       |            | weight |            | ReLU   |
|          | ReLU   |                         | ReLU   |          | ReLU     |            | BN     |            | weight |
|          | weight |                         | weight |          | weight   |            | ReLU   |            | BN     |
|          | BN     | addition                |        |          | BN       |            | weight |            | ReLU   |
| addition |        | BN                      |        |          | ReLU     |            | BN     |            | weight |
| ReLU     |        | ReLU                    |        | addition |          | addition   |        | addition   |        |
| xl+1     |        | xl+1                    |        | xl+1     |          | xl+1       |        | xl+1       |        |
(b) BN after  (c) ReLU before  (d) ReLU-only (e) full pre-activation
(a) original
|     |     |     | addition |     | addition | pre-activation |     |     |     |
| --- | --- | --- | -------- | --- | -------- | -------------- | --- | --- | --- |
Figure4. Various usages of activation in Table 2. All these units consist of the same
| components |     | — only the | orders | are different. |     |     |     |     |     |
| ---------- | --- | ---------- | ------ | -------------- | --- | --- | --- | --- | --- |
3.2 Discussions
As indicated by the grey arrows in Fig. 2, the shortcut connections are the
mostdirectpathsfortheinformationtopropagate.Multiplicative manipulations
(scaling, gating, 1×1 convolutions, and dropout) on the shortcuts can hamper
| information |     | propagation | and | lead to | optimization | problems. |     |     |     |
| ----------- | --- | ----------- | --- | ------- | ------------ | --------- | --- | --- | --- |
It is noteworthy that the gating and 1×1 convolutional shortcuts introduce
more parameters, and should have stronger representational abilities than iden-
tity shortcuts. In fact, the shortcut-only gating and 1×1 convolution cover the
solution space of identity shortcuts (i.e., they could be optimized as identity
shortcuts). However, their training error is higher than that of identity short-
cuts, indicating that the degradation of these models is caused by optimization
| issues, | instead | of representational |               | abilities. |           |     |     |     |     |
| ------- | ------- | ------------------- | ------------- | ---------- | --------- | --- | --- | --- | --- |
| 4       | On the  | Usage               | of Activation |            | Functions |     |     |     |     |
Experiments in the above section support the analysis in Eqn.(5) and Eqn.(8),
both being derived under the assumption that the after-addition activation f

9
is the identity mapping. But in the above experiments f is ReLU as designed
in [1], so Eqn.(5) and (8) are approximate in the above experiments. Next we
| investigate | the impact | of f. |     |     |     |
| ----------- | ---------- | ----- | --- | --- | --- |
We want to make f an identity mapping, which is done by re-arranging
the activation functions (ReLU and/or BN). The original Residual Unit in [1]
has a shape in Fig. 4(a) — BN is used after each weight layer, and ReLU is
adoptedafterBNexceptthatthelastReLUinaResidualUnitisafterelement-
wise addition (f = ReLU). Fig. 4(b-e) show the alternatives we investigated,
| explained as    | following. |            |     |     |     |
| --------------- | ---------- | ---------- | --- | --- | --- |
| 4.1 Experiments | on         | Activation |     |     |     |
In this section we experiment with ResNet-110 and a 164-layer Bottleneck [1]
architecture (denoted as ResNet-164). A bottleneck Residual Unit consist of a
1×1 layer for reducing dimension, a 3×3 layer, and a 1×1 layer for restoring
dimension. As designed in [1], its computational complexity is similar to the
two-3×3 Residual Unit. More details are in the appendix. The baseline ResNet-
| 164 has a competitive |     | result of 5.93% | on  | CIFAR-10 (Table 2). |     |
| --------------------- | --- | --------------- | --- | ------------------- | --- |
BN after addition. Before turning f into an identity mapping, we go the
opposite way by adopting BN after addition (Fig. 4(b)). In this case f involves
BN and ReLU. The results become considerably worse than the baseline (Ta-
ble 2). Unlike the original design, now the BN layer alters the signal that passes
through the shortcut and impedes information propagation, as reflected by the
difficulties on reducing training loss at the beginning of training (Fib. 6 left).
ReLU before addition. A na¨ıve choice of making f into an identity map-
ping is to move the ReLU before addition (Fig. 4(c)). However, this leads to a
non-negative output from the transform F, while intuitively a “residual” func-
tion should take values in (−∞,+∞). As a result, the forward propagated sig-
nal is monotonically increasing. This may impact the representational ability,
and the result is worse (7.84%, Table 2) than the baseline. We expect to have
a residual function taking values in (−∞,+∞). This condition is satisfied by
| other Residual | Units including | the | following | ones. |     |
| -------------- | --------------- | --- | --------- | ----- | --- |
Post-activation or pre-activation? In the original design (Eqn.(1) and
Eqn.(2)), the activation x = f(y ) affects both paths in the next Residual
|     |     | l+1 | l   |     |     |
| --- | --- | --- | --- | --- | --- |
Unit: y = f(y ) + F(f(y ),W ). Next we develop an asymmetric form
| l+1 | l   | l   | l+1 |     |     |
| --- | --- | --- | --- | --- | --- |
where an activation fˆonly affects the F path: y = y +F(fˆ(y ),W ), for
|     |     |     |     | l+1 l l l+1 |     |
| --- | --- | --- | --- | ----------- | --- |
anyl (Fig.5(a)to(b)).Byrenamingthenotations,wehavethefollowingform:
|     |     | x =x | +F(fˆ(x | ),W ),. | (9) |
| --- | --- | ---- | ------- | ------- | --- |
|     |     | l+1  | l       | l l     |     |
It is easy to see that Eqn.(9) is similar to Eqn.(4), and can enable a backward
formulationsimilartoEqn.(5).ForthisnewResidualUnitasinEqn.(9),thenew
after-addition activation becomes an identity mapping. This design means that
fˆis
if a new after-addition activation asymmetrically adopted, it is equivalent
torecastingfˆasthepre-activation ofthenextResidualUnit.Thisisillustrated
in Fig. 5.

10
|     | ... |     |     |     | ... |     | ... |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
act.
|     |     |     |     |     | act. |     |     | act. |
| --- | --- | --- | --- | --- | ---- | --- | --- | ---- |
original
| Residual |          |        | asymmetric |          |        |     |                |        |
| -------- | -------- | ------ | ---------- | -------- | ------ | --- | -------------- | ------ |
|          |          | weight |            |          | weight |     |                | weight |
|          | Unit     |        |            | output   |        |     |                |        |
|          |          | act.   | activation |          | act.   |     |                | act.   |
|          |          | weight |            |          | weight |     |                | weight |
|          | addition |        |            | addition |        |     | addition       |        |
|          | act.     |        |            |          |        |     | pre-activation |        |
|          |          |        |            |          | act.   |     |                | act.   |
Residual Unit
|     |          | weight |     |          | weight |     |          | weight |
| --- | -------- | ------ | --- | -------- | ------ | --- | -------- | ------ |
|     |          | act.   |     |          | act.   |     |          | act.   |
|     |          | weight |     |          | weight |     |          | weight |
|     | addition |        |     | addition |        |     | addition |        |
|     | act.     |        |     |          | ...    |     | ...      |        |
adopt output activation
|     | ... |     |     |     | equivalent to |     |     |     |
| --- | --- | --- | --- | --- | ------------- | --- | --- | --- |
only to weight path
|     | (a) |     |     | (b) |     |     | (c) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure5. Using asymmetric after-addition activation is equivalent to constructing a
| pre-activation |     | Residual | Unit. |     |     |     |     |     |
| -------------- | --- | -------- | ----- | --- | --- | --- | --- | --- |
Table 3. Classification error (%) on the CIFAR-10/100 test set using the original
| Residual | Units   | and our                | pre-activation | Residual | Units.       |                    |      |     |
| -------- | ------- | ---------------------- | -------------- | -------- | ------------ | ------------------ | ---- | --- |
|          | dataset | network                |                |          | baselineunit | pre-activationunit |      |     |
|          |         | ResNet-110(1layerskip) |                |          | 9.90         |                    | 8.91 |     |
|          |         | ResNet-110             |                |          | 6.61         |                    | 6.37 |     |
CIFAR-10
|     |     | ResNet-164  |     |     | 5.93  |     | 5.46  |     |
| --- | --- | ----------- | --- | --- | ----- | --- | ----- | --- |
|     |     | ResNet-1001 |     |     | 7.61  |     | 4.92  |     |
|     |     | ResNet-164  |     |     | 25.16 |     | 24.33 |     |
CIFAR-100
|     |     | ResNet-1001 |     |     | 27.82 |     | 22.71 |     |
| --- | --- | ----------- | --- | --- | ----- | --- | ----- | --- |
Thedistinctionbetweenpost-activation/pre-activationiscausedbythepres-
ence of the element-wise addition. For a plain network that has N layers, there
are N −1 activations (BN/ReLU), and it does not matter whether we think of
them as post- or pre-activations. But for branched layers merged by addition,
| the position |     | of activation | matters. |     |     |     |     |     |
| ------------ | --- | ------------- | -------- | --- | --- | --- | --- | --- |
Weexperimentwithtwosuchdesigns:(i)ReLU-onlypre-activation(Fig.4(d)),
and(ii)fullpre-activation(Fig.4(e))whereBNandReLUarebothadoptedbe-
fore weight layers. Table 2 shows that the ReLU-only pre-activation performs
very similar to the baseline on ResNet-110/164. This ReLU layer is not used in
conjunction with a BN layer, and may not enjoy the benefits of BN [8].
Somehow surprisingly, when BN and ReLU are both used as pre-activation,
theresultsareimprovedbyhealthymargins(Table2andTable3).InTable3we
report results using various architectures: (i) ResNet-110, (ii) ResNet-164, (iii)
a 110-layer ResNet architecture in which each shortcut skips only 1 layer (i.e.,

11
| 2   |     |     |   20 2 |     |     |   20 |
| --- | --- | --- | ------ | --- | --- | ---- |
164, original
164, proposed (pre−activation)
|               |     |     | 15             |     |     | 15             |
| ------------- | --- | --- | -------------- | --- | --- | -------------- |
| 0.2           |     |     | 0.2            |     |     |                |
|               |     |     | Test Error (%) |     |     | Test Error (%) |
| ssoL gniniarT |     |     | ssoL gniniarT  |     |     |                |
10
10
| 0.02 |     |     | 0.02 |     |     |     |
| ---- | --- | --- | ---- | --- | --- | --- |
|      |     |     | 5    |     |     | 5   |
110, original
110, BN after add
| 0.002  0 1 | 2 3        | 4 5 | 6 0 0.002  0 1 | 2 3 4      | 5   | 6 0   |
| ---------- | ---------- | --- | -------------- | ---------- | --- | ----- |
|            | Iterations |     | x 104          | Iterations |     | x 104 |
Figure6. Training curves on CIFAR-10. Left: BN after addition (Fig. 4(b)) using
ResNet-110. Right: pre-activation unit (Fig. 4(e)) on ResNet-164. Solid lines denote
| test error, | and dashed lines | denote | training loss. |     |     |     |
| ----------- | ---------------- | ------ | -------------- | --- | --- | --- |
a Residual Unit has only 1 layer), denoted as “ResNet-110(1layer)”, and (iv)
a 1001-layer bottleneck architecture that has 333 Residual Units (111 on each
feature map size), denoted as “ResNet-1001”. We also experiment on CIFAR-
100.Table3showsthatour“pre-activation”modelsareconsistentlybetterthan
the baseline counterparts. We analyze these results in the following.
4.2 Analysis
Wefindtheimpactofpre-activationistwofold.First,theoptimizationisfurther
eased (comparing with the baseline ResNet) because f is an identity mapping.
Second, using BN as pre-activation improves regularization of the models.
Ease of optimization. This effect is particularly obvious when training
the 1001-layer ResNet. Fig. 1 shows the curves. Using the original design in
[1], the training error is reduced very slowly at the beginning of training. For
f = ReLU, the signal is impacted if it is negative, and when there are many
Residual Units, this effect becomes prominent and Eqn.(3) (so Eqn.(5)) is not
a good approximation. On the other hand, when f is an identity mapping, the
signalcanbepropagateddirectlybetweenanytwounits.Our1001-layernetwork
reduces the training loss very quickly (Fig. 1). It also achieves the lowest loss
among all models we investigated, suggesting the success of optimization.
We also find that the impact of f = ReLU is not severe when the ResNet
has fewer layers (e.g., 164 in Fig. 6(right)). The training curve seems to suffer
a little bit at the beginning of training, but goes into a healthy status soon. By
monitoring the responses we observe that this is because after some training,
theweightsareadjustedintoastatussuchthaty inEqn.(1)ismorefrequently
l
above zero and f does not truncate it (x is always non-negative due to the pre-
l
viousReLU,soy isbelowzeroonlywhenthemagnitudeofF isverynegative).
l
The truncation, however, is more frequent when there are 1000 layers.

12
Table 4. Comparisons with state-of-the-art methods on CIFAR-10 and CIFAR-100
using “moderate data augmentation” (flip/translation), except for ELU [12] with no
augmentation.Betterresultsof[13,14]havebeenreportedusingstrongerdataaugmen-
tationandensembling.FortheResNetswealsoreportthenumberofparameters.Our
results are the median of 5 runs with mean±std in the brackets. All ResNets results
†
are obtained with a mini-batch size of 128 except with a mini-batch size of 64 (code
| available              | at https://github.com/KaimingHe/resnet-1k-layers). |          |                        |          |
| ---------------------- | -------------------------------------------------- | -------- | ---------------------- | -------- |
| CIFAR-10               |                                                    | error(%) | CIFAR-100              | error(%) |
| NIN[15]                |                                                    | 8.81     | NIN[15]                | 35.68    |
| DSN[16]                |                                                    | 8.22     | DSN[16]                | 34.57    |
| FitNet[17]             |                                                    | 8.39     | FitNet[17]             | 35.04    |
| Highway[7]             |                                                    | 7.72     | Highway[7]             | 32.39    |
| All-CNN[14]            |                                                    | 7.25     | All-CNN[14]            | 33.71    |
| ELU[12]                |                                                    | 6.55     | ELU[12]                | 24.28    |
| FitResNet,LSUV[18]     |                                                    | 5.84     | FitNet,LSUV[18]        | 27.66    |
| ResNet-110[1](1.7M)    |                                                    | 6.61     | ResNet-164[1](1.7M)    | 25.16    |
| ResNet-1202[1](19.4M)  |                                                    | 7.93     | ResNet-1001[1](10.2M)  | 27.82    |
| ResNet-164[ours](1.7M) |                                                    | 5.46     | ResNet-164[ours](1.7M) | 24.33    |
ResNet-1001[ours](10.2M) 4.92(4.89±0.14) ResNet-1001[ours](10.2M) 22.71(22.68±0.22)
| ResNet-1001[ours](10.2M)† |     | 4.62(4.69±0.20) |     |     |
| ------------------------- | --- | --------------- | --- | --- |
Reducingoverfitting.Anotherimpactofusingtheproposedpre-activation
unit is on regularization, as shown in Fig. 6 (right). The pre-activation ver-
sionreachesslightlyhighertraininglossatconvergence,butproduceslowertest
error. This phenomenon is observed on ResNet-110, ResNet-110(1-layer), and
ResNet-164onbothCIFAR-10and100.ThisispresumablycausedbyBN’sreg-
ularization effect [8]. In the original Residual Unit (Fig. 4(a)), although the BN
normalizes the signal, this is soon added to the shortcut and thus the merged
signal is not normalized. This unnormalized signal is then used as the input of
the next weight layer. On the contrary, in our pre-activation version, the inputs
| to all weight | layers have | been normalized. |     |     |
| ------------- | ----------- | ---------------- | --- | --- |
5 Results
ComparisonsonCIFAR-10/100.Table4comparesthestate-of-the-artmeth-
ods on CIFAR-10/100, where we achieve competitive results. We note that we
do not specially tailor the network width or filter sizes, nor use regularization
techniques (such as dropout) which are very effective for these small datasets.
Weobtaintheseresultsviaasimplebutessentialconcept—goingdeeper.These
results demonstrate the potential of pushing the limits of depth.
ComparisonsonImageNet.Nextwereportexperimentalresultsonthe1000-
classImageNetdataset[3].Wehavedonepreliminaryexperimentsusingtheskip
connectionsstudiedinFig.2&3onImageNetwithResNet-101[1],andobserved
similaroptimizationdifficulties.Thetrainingerrorofthesenon-identityshortcut
networks is obviously higher than the original ResNet at the first learning rate

13
Table 5. Comparisons of single-crop error on the ILSVRC 2012 validation set. All
ResNets are trained using the same hyper-parameters and implementations as [1]).
OurResidualUnitsarethefullpre-activationversion(Fig.4(e)).†:code/modelavail-
able at https://github.com/facebook/fb.resnet.torch/tree/master/pretrained,
using scale and aspect ratio augmentation in [20].
method augmentation traincrop testcrop top-1 top-5
ResNet-152,originalResidualUnit[1] scale 224×224 224×224 23.0 6.7
ResNet-152,originalResidualUnit[1] scale 224×224 320×320 21.3 5.5
ResNet-152,pre-actResidualUnit scale 224×224 320×320 21.1 5.5
ResNet-200,originalResidualUnit[1] scale 224×224 320×320 21.8 6.0
ResNet-200,pre-actResidualUnit scale 224×224 320×320 20.7 5.3
ResNet-200,pre-actResidualUnit scale+aspratio 224×224 320×320 20.1† 4.8†
Inceptionv3[19] scale+aspratio 299×299 299×299 21.2 5.6
(similar to Fig. 3), and we decided to halt training due to limited resources.
But we did finish a “BN after addition” version (Fig. 4(b)) of ResNet-101 on
ImageNet and observed higher training loss and validation error. This model’s
single-crop (224×224) validation error is 24.6%/7.5%, vs. the original ResNet-
101’s 23.6%/7.1%. This is in line with the results on CIFAR in Fig. 6 (left).
Table5showstheresultsofResNet-152[1]andResNet-2003,alltrainedfrom
scratch. We notice that the original ResNet paper [1] trained the models using
scale jittering with shorter side s∈[256,480], and so the test of a 224×224 crop
on s=256 (as did in [1]) is negatively biased. Instead, we test a single 320×320
crop from s = 320, for all original and our ResNets. Even though the ResNets
are trained on smaller crops, they can be easily tested on larger crops because
the ResNets are fully convolutional by design. This size is also close to 299×299
used by Inception v3 [19], allowing a fairer comparison.
TheoriginalResNet-152[1]hastop-1errorof21.3%ona320×320crop,and
our pre-activation counterpart has 21.1%. The gain is not big on ResNet-152
because this model has not shown severe generalization difficulties. However,
the original ResNet-200 has an error rate of 21.8%, higher than the baseline
ResNet-152. But we find that the original ResNet-200 has lower training error
than ResNet-152, suggesting that it suffers from overfitting.
Our pre-activation ResNet-200 has an error rate of 20.7%, which is 1.1%
lower than the baseline ResNet-200 and also lower than the two versions of
ResNet-152. When using the scale and aspect ratio augmentation of [20,19], our
ResNet-200 has a result better than Inception v3 [19] (Table 5). Concurrent
with our work, an Inception-ResNet-v2 model [21] achieves a single-crop result
of19.9%/4.9%.WeexpectourobservationsandtheproposedResidualUnitwill
help this type and generally other types of ResNets.
Computational Cost. Our models’ computational complexity is linear on
3 The ResNet-200 has 16 more 3-layer bottleneck Residual Units than ResNet-152,
which are added on the feature map of 28×28.

14
depth (so a 1001-layer net is ∼10× complex of a 100-layer net). On CIFAR,
ResNet-1001 takes about 27 hours to train on 2 GPUs; on ImageNet, ResNet-
200 takes about 3 weeks to train on 8 GPUs (on par with VGG nets [22]).
6 Conclusions
This paper investigates the propagation formulations behind the connection
mechanismsofdeepresidualnetworks.Ourderivationsimplythatidentityshort-
cut connections and identity after-addition activation are essential for making
information propagation smooth. Ablation experiments demonstrate phenom-
ena that are consistent with our derivations. We also present 1000-layer deep
networks that can be easily trained and achieve improved accuracy.
Appendix: Implementation Details Theimplementationdetailsandhyper-
parameters are the same as those in [1]. On CIFAR we use only the translation
and flipping augmentation in [1] for training. The learning rate starts from 0.1,
and is divided by 10 at 32k and 48k iterations. Following [1], for all CIFAR
experiments we warm up the training by using a smaller learning rate of 0.01 at
the beginning 400 iterations and go back to 0.1 after that, although we remark
that this is not necessary for our proposed Residual Unit. The mini-batch size
is 128 on 2 GPUs (64 each), the weight decay is 0.0001, the momentum is 0.9,
and the weights are initialized as in [23].
On ImageNet, we train the models using the same data augmentation as in
[1]. The learning rate starts from 0.1 (no warming up), and is divided by 10 at
30 and 60 epochs. The mini-batch size is 256 on 8 GPUs (32 each). The weight
decay, momentum, and weight initialization are the same as above.
When using the pre-activation Residual Units (Fig. 4(d)(e) and Fig. 5), we
pay special attention to the first and the last Residual Units of the entire net-
work.ForthefirstResidualUnit(thatfollowsastand-aloneconvolutionallayer,
conv ), we adopt the first activation right after conv and before splitting into
1 1
two paths; for the last Residual Unit (followed by average pooling and a fully-
connected classifier), we adopt an extra activation right after its element-wise
addition. These two special cases are the natural outcome when we obtain the
pre-activation network via the modification procedure as shown in Fig. 5.
The bottleneck Residual Units (for ResNet-164/1001 on CIFAR) are con-
structed following [1]. For example, a (cid:34) 3×3,16 (cid:35) unit in ResNet-110 is replaced
3×3,16
 
with a 1×1,16 unit in ResNet-164, both of which have roughly the same num-
 3×3,16

1×1,64
ber of parameters. For the bottleneck ResNets, when reducing the feature map
size we use projection shortcuts [1] for increasing dimensions, and when pre-
activation is used, these projection shortcuts are also with pre-activation.

15
References
1. He, K., Zhang, X., Ren, S., Sun, J.: Deep residual learning for image recognition.
| In: CVPR. | (2016) |     |     |     |     |
| --------- | ------ | --- | --- | --- | --- |
2. Nair, V., Hinton, G.E.: Rectified linear units improve restricted boltzmann ma-
| chines. In: | ICML. | (2010) |     |     |     |
| ----------- | ----- | ------ | --- | --- | --- |
3. Russakovsky, O., Deng, J., Su, H., Krause, J., Satheesh, S., Ma, S., Huang, Z.,
Karpathy, A., Khosla, A., Bernstein, M., Berg, A.C., Fei-Fei, L.: ImageNet Large
| Scale Visual | Recognition | Challenge. | IJCV | (2015) |     |
| ------------ | ----------- | ---------- | ---- | ------ | --- |
4. Lin, T.Y., Maire, M., Belongie, S., Hays, J., Perona, P., Ramanan, D., Dolla´r, P.,
Zitnick, C.L.: Microsoft COCO: Common objects in context. In: ECCV. (2014)
5. Hochreiter, S., Schmidhuber, J.: Long short-term memory. Neural computation
(1997)
6. Srivastava, R.K., Greff, K., Schmidhuber, J.: Highway networks. In: ICML work-
shop. (2015)
7. Srivastava, R.K., Greff, K., Schmidhuber, J.: Training very deep networks. In:
NIPS. (2015)
8. Ioffe,S.,Szegedy,C.: Batchnormalization:Acceleratingdeepnetworktrainingby
| reducing | internal covariate |     | shift. In: ICML. | (2015) |     |
| -------- | ------------------ | --- | ---------------- | ------ | --- |
9. LeCun, Y., Boser, B., Denker, J.S., Henderson, D., Howard, R.E., Hubbard, W.,
Jackel,L.D.: Backpropagationappliedtohandwrittenzipcoderecognition. Neural
| computation | (1989) |     |     |     |     |
| ----------- | ------ | --- | --- | --- | --- |
10. Krizhevsky,A.: Learningmultiplelayersoffeaturesfromtinyimages. TechReport
(2009)
11. Hinton, G.E., Srivastava, N., Krizhevsky, A., Sutskever, I., Salakhutdinov, R.R.:
Improving neural networks by preventing co-adaptation of feature detectors.
| arXiv:1207.0580 | (2012) |     |     |     |     |
| --------------- | ------ | --- | --- | --- | --- |
12. Clevert, D.A., Unterthiner, T., Hochreiter, S.: Fast and accurate deep network
learning by exponential linear units (ELUs). In: ICLR. (2016)
13. Graham, B.: Fractional max-pooling. arXiv:1412.6071 (2014)
14. Springenberg,J.T.,Dosovitskiy,A.,Brox,T.,Riedmiller,M.: Strivingforsimplic-
| ity: The | all convolutional | net. | arXiv:1412.6806 |     | (2014) |
| -------- | ----------------- | ---- | --------------- | --- | ------ |
15. Lin, M., Chen, Q., Yan, S.: Network in network. In: ICLR. (2014)
16. Lee, C.Y., Xie, S., Gallagher, P., Zhang, Z., Tu, Z.: Deeply-supervised nets. In:
| AISTATS. | (2015) |     |     |     |     |
| -------- | ------ | --- | --- | --- | --- |
17. Romero,A.,Ballas,N.,Kahou,S.E.,Chassang,A.,Gatta,C.,Bengio,Y.: Fitnets:
| Hints for | thin deep | nets. In: | ICLR. (2015) |     |     |
| --------- | --------- | --------- | ------------ | --- | --- |
18. Mishkin, D., Matas, J.: All you need is a good init. In: ICLR. (2016)
19. Szegedy,C.,Vanhoucke,V.,Ioffe,S.,Shlens,J.,Wojna,Z.: Rethinkingtheincep-
| tion architecture | for | computer | vision. | In: CVPR. | (2016) |
| ----------------- | --- | -------- | ------- | --------- | ------ |
20. Szegedy, C., Liu, W., Jia, Y., Sermanet, P., Reed, S., Anguelov, D., Erhan, D.,
Vanhoucke,V.,Rabinovich,A.:Goingdeeperwithconvolutions.In:CVPR.(2015)
21. Szegedy,C.,Ioffe,S.,Vanhoucke,V.:Inception-v4,inception-resnetandtheimpact
| of residual | connections | on  | learning. arXiv:1602.07261 |     | (2016) |
| ----------- | ----------- | --- | -------------------------- | --- | ------ |
22. Simonyan, K., Zisserman, A.: Very deep convolutional networks for large-scale
| image recognition. |     | In: ICLR. | (2015) |     |     |
| ------------------ | --- | --------- | ------ | --- | --- |
23. He,K.,Zhang,X.,Ren,S.,Sun,J.:Delvingdeepintorectifiers:Surpassinghuman-
level performance on imagenet classification. In: ICCV. (2015)