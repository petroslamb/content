5
1
0
2

n
u
J

8

]

G
L
.
s
c
[

1
v
7
1
6
2
0
.
6
0
5
1
:
v
i
X
r
a

Path-SGD: Path-Normalized Optimization in
Deep Neural Networks

Behnam Neyshabur1, Ruslan Salakhutdinov2 and Nathan Srebro1

1Toyota Technological Institute at Chicago
2Department of Computer Science, University of Toronto

Abstract

We revisit the choice of SGD for training deep neural networks by reconsidering the appropriate
geometry in which to optimize the weights. We argue for a geometry invariant to rescaling of weights
that does not affect the output of the network, and suggest Path-SGD, which is an approximate steepest
descent method with respect to a path-wise regularizer related to max-norm regularization. Path-SGD is
easy and efﬁcient to implement and leads to empirical gains over SGD and AdaGrad.

1 Introduction

Training deep networks is a challenging problem [16, 2] and various heuristics and optimization algorithms
have been suggested in order to improve the efﬁciency of the training [5, 9, 4]. However, training deep
architectures is still considerably slow and the problem has remained open. Many of the current training
methods rely on good initialization and then performing Stochastic Gradient Descent (SGD), sometimes
together with an adaptive stepsize or momentum term [16, 1, 6].

Revisiting the choice of gradient descent, we recall that optimization is inherently tied to a choice of ge-
ometry or measure of distance, norm or divergence. Gradient descent for example is tied to the (cid:96)2 norm as it
is the steepest descent with respect to (cid:96)2 norm in the parameter space, while coordinate descent corresponds
to steepest descent with respect to the (cid:96)1 norm and exp-gradient (multiplicative weight) updates is tied to
an entropic divergence. Moreover, at least when the objective function is convex, convergence behavior is
tied to the corresponding norms or potentials. For example, with gradient descent, or SGD, convergence
speeds depend on the (cid:96)2 norm of the optimum. The norm or divergence can be viewed as a regularizer for
the updates. There is therefore also a strong link between regularization for optimization and regularization
for learning: optimization may provide implicit regularization in terms of its corresponding geometry, and
for ideal optimization performance the optimization geometry should be aligned with inductive bias driving
the learning [14].

Is the (cid:96)2 geometry on the weights the appropriate geometry for the space of deep networks? Or can we
suggest a geometry with more desirable properties that would enable faster optimization and perhaps also
better implicit regularization? As suggested above, this question is also linked to the choice of an appropriate
regularizer for deep networks.

Focusing on networks with RELU activations, we observe that scaling down the incoming edges to a
hidden unit and scaling up the outgoing edges by the same factor yields an equivalent network computing
the same function. Since predictions are invariant to such rescalings, it is natural to seek a geometry, and
corresponding optimization method, that is similarly invariant.

1

We consider here a geometry inspired by max-norm regularization (regularizing the maximum norm of
incoming weights into any unit) which seems to provide a better inductive bias compared to the (cid:96)2 norm
(weight decay) [3, 15]. But to achieve rescaling invariance, we use not the max-norm itself, but rather the
minimum max-norm over all rescalings of the weights. We discuss how this measure can be expressed as a
“path regularizer” and can be computed efﬁciently.

We therefore suggest a novel optimization method, Path-SGD , that is an approximate steepest descent
method with respect to path regularization. Path-SGD is rescaling-invariant and we demonstrate that Path-
SGD outperforms gradient descent and AdaGrad for classiﬁcations tasks on several benchmark datasets.

Notations A feedforward neural network that computes a function f : RD → RC can be represented
by a directed acyclic graph (DAG) G(V, E) with D input nodes vin[1], . . . , vin[D] ∈ V , C output nodes
vout[1], . . . , vout[C] ∈ V , weights w : E → R and an activation function σ : R → R that is applied on the
internal nodes (hidden units). We denote the function computed by this network as fG,w,σ. In this paper we
focus on RELU (REctiﬁed Linear Unit) activation function σRELU(x) = max{0, x}. We refer to the depth
d of the network which is the length of the longest directed path in G. For any 0 ≤ i ≤ d, we deﬁne V i
in to
be the set of vertices with longest path of length i to an input unit and V i
out is deﬁned similarly for paths to
output units. In layered networks V i

is the set of hidden units in a hidden layer i.

in = V d−i

out

2 Rescaling and Unbalanceness

One of the special properties of RELU activation function is non-negative homogeneity. That is, for any
scalar c ≥ 0 and any x ∈ R, we have σRELU(c · x) = c · σRELU(x). This interesting property allows the
network to be rescaled without changing the function computed by the network. We deﬁne the rescaling
function ρc,v(w), such that given the weights of the network w : E → R, a constant c > 0, and a node v, the
rescaling function multiplies the incoming edges and divides the outgoing edges of v by c. That is, ρc,v(w)
maps w to the weights ˜w for the rescaled network, where for any (u1 → u2) ∈ E:

˜w(u1→u2) =






c.w(u1→u2) u2 = v,
1
u1 = v,
c w(u1→u2)
w(u1→u2)
otherwise.

(1)

It is easy to see that the rescaled network computes the same function, i.e. fG,w,σRELU = fG,ρc,v(w),σRELU .
We say that the two networks with weights w and ˜w are rescaling equivalent denoted by w ∼ ˜w if and only
if one of them can be transformed to another by applying a sequence of rescaling functions ρc,v.

Given a training set S = {(x1, yn), . . . , (xn, yn)}, our goal is to minimize the following objective

function:

L(w) =

n
(cid:88)

(cid:96)(fw(xi), yi).

(2)

1
n

i=1
Let w(t) be the weights at step t of the optimization. We consider update step of the following form w(t+1) =
w(t) + ∆w(t+1). For example, for gradient descent, we have ∆w(t+1) = −η∇L(w(t)), where η is the step-
size. In the stochastic setting, such as SGD or mini-batch gradient descent, we calculate the gradient on a
small subset of the training set.

Since rescaling equivalent networks compute the same function, it is desirable to have an update rule that
is not affected by rescaling. We call an optimization method rescaling invariant if the updates of rescaling
equivalent networks are rescaling equivalent. That is, if we start at either one of the two rescaling equivalent
weight vectors ˜w(0) ∼ w(0), after applying t update steps separately on ˜w(0) and w(0), they will remain
rescaling equivalent and we have ˜w(t) ∼ w(t).

2

(a) Training on MNIST

(b) Weight Explosion in an unbalanced network

(c) Poor updates in an unbalanced network

Figure 1: (a): Evolution of the cross-entropy error function when training a feed-forward network on MNIST with
two hidden layers, each containing 4000 hidden units. The unbalanced initialization (blue curve) is generated by
applying a sequence of rescaling functions on the balanced initializations (red curve). (b): Updates for a simple case
where the input is x = 1, thresholds are set to zero (constant), the stepsize is 1, and the gradient with respect to output
is δ = −1. (c): Updated network for the case where the input is x = (1, 1), thresholds are set to zero (constant), the
stepsize is 1, and the gradient with respect to output is δ = (−1, −1).

Unfortunately, gradient descent is not rescaling invariant. The main problem with the gradient updates
is that scaling down the weights of an edge will also scale up the gradient which, as we see later, is exactly
the opposite of what is expected from a rescaling invariant update.

Furthermore, gradient descent performs very poorly on “unbalanced” networks. We say that a network
is balanced if the norm of incoming weights to different units are roughly the same or within a small range.
For example, Figure 1(a) shows a huge gap in the performance of SGD initialized with a randomly gener-
ated balanced network w(0), when training on MNIST, compared to a network initialized with unbalanced
weights ˜w(0). Here ˜w(0) is generated by applying a sequence of random rescaling functions on w(0) (and
therefore w(0) ∼ ˜w(0)).

In an unbalanced network, gradient descent updates could blow up the smaller weights, while keeping
the larger weights almost unchanged. This is illustrated in Figure 1(b). If this were the only issue, one could
scale down all the weights after each update. However, in an unbalanced network, the relative changes in the
weights are also very different compared to a balanced network. For example, Figure 1(c) shows how two
rescaling equivalent networks could end up computing a very different function after only a single update.

3

010020030000.511.522.5EpochObjective  BalancedUnbalanced100 10-4 SGD Update 100 ~100 ~104 ~100 1 1 Rescaling 1 uvuvuv≈ ≈ 8 6 8 3 7 7 8 4 vu6 1 1 1 4 2 1 1 vu60.2 10.5 70.1 10.2 30.4 20.5 70.1 30.1 vu60 10 0.1 10 0.4 20 0.1 0.1 vuSGD Update SGD Update Rescaling 3 Magnitude/Scale measures for deep networks

Following [12], we consider the grouping of weights going into each node of the network. This forms the
following generic group-norm type regularizer, parametrized by 1 ≤ p, q ≤ ∞:

µp,q(w) =






(cid:88)





v∈V

q/p

1/q



(cid:88)

(cid:12)
(cid:12)w(u→v)

(cid:12)
(cid:12)

p



(u→v)∈E




.

(3)

Two simple cases of above group-norm are p = q = 1 and p = q = 2 that correspond to overall (cid:96)1 regular-
ization and weight decay respectively. Another form of regularization that is shown to be very effective in
RELU networks is the max-norm regularization, which is the maximum over all units of norm of incoming
edge to the unit1 [3, 15]. The max-norm correspond to “per-unit” regularization when we set q = ∞ in
equation (4) and can be written in the following form:

µp,∞(w) = sup
v∈V







1/p

(cid:88)

(cid:12)
(cid:12)w(u→v)

(cid:12)
(cid:12)

p



(u→v)∈E

(4)

Weight decay is probably the most commonly used regularizer. On the other hand, per-unit regulariza-
tion might not seem ideal as it is very extreme in the sense that the value of regularizer corresponds to the
highest value among all nodes. However, the situation is very different for networks with RELU activations
(and other activation functions with non-negative homogeneity property). In these cases, per-unit (cid:96)2 regu-
larization has shown to be very effective [15]. The main reason could be because RELU networks can be
rebalanced in such a way that all hidden units have the same norm. Hence, per-unit regularization will not
be a crude measure anymore.

Since µp,∞ is not rescaling invariant and the values of the scale measure are different for rescaling
equivalent networks, it is desirable to look for the minimum value of a regularizer among all rescaling
equivalent networks. Surprisingly, for a feed-forward network, the minimum (cid:96)p per-unit regularizer among
all rescaling equivalent networks can be efﬁciently computed by a single forward step. To see this, we
consider the vector π(w), the path vector, where the number of coordinates of π(w) is equal to the total
number of paths from the input to output units and each coordinate of π(w) is the equal to the product of
weights along a path from an input nodes to an output node. The (cid:96)p-path regularizer is then deﬁned as the
(cid:96)p norm of π(w) [12]:

φp(w) = (cid:107)π(w)(cid:107)p =






(cid:88)

vin[i]

e1→v1

e2→v2...

ed→vout[j]

d
(cid:89)

(cid:12)
(cid:12)
(cid:12)
(cid:12)
(cid:12)
k=1

wek

1/p

p



(cid:12)
(cid:12)
(cid:12)
(cid:12)
(cid:12)

(5)

The following Lemma establishes that the (cid:96)p-path regularizer corresponds to the minimum over all equiva-
lent networks of the per-unit (cid:96)p norm:

Lemma 3.1 ([12]). φp(w) = min
˜w∼w

µp,∞( ˜w)

(cid:18)

(cid:19)d

1This deﬁnition of max-norm is a bit different than the one used in the context of matrix factorization [13]. The later is similar
to the minimum upper bound over (cid:96)2 norm of both outgoing edges from the input units and incoming edges to the output units in a
two layer feed-forward network.

4

The deﬁnition (5) of the (cid:96)p-path regularizer involves an exponential number of terms. But it can be
computed efﬁciently by dynamic programming in a single forward step using the following equivalent form
as nested sums:





φp(w) =

(cid:88)

(cid:12)
(cid:12)w(vd−1→vout[j])

p (cid:88)
(cid:12)
(cid:12)

(cid:88)

. . .

(cid:12)
(cid:12)w(vin[i]→v1)

(cid:12)
(cid:12)

p



(vd−1→vout[j])∈E

(vd−2→vd−1)∈E

(vin[i]→v1)∈E



1/p

A straightforward consequence of Lemma 3.1 is that the (cid:96)p path-regularizer φp is invariant to rescaling, i.e.
for any ˜w ∼ w, φp( ˜w) = φp(w).

4 Path-SGD : An Approximate Path-Regularized Steepest Descent

Motivated by empirical performance of max-norm regularization and the fact that path-regularizer is in-
variant to rescaling, we are interested in deriving the steepest descent direction with respect to the path
regularizer φp(w):

w(t+1) = arg min
w

η

(cid:68)

∇L(w(t)), w

(cid:69)

+

= arg min

w

(cid:68)

η

∇L(w(t)), w

(cid:69)

+

= arg min

w

J (t)(w)

1
2





(cid:13)
(cid:13)
2
(cid:13)π(w) − π(w(t))
(cid:13)
(cid:13)
(cid:13)
p

(6)

(cid:88)

(cid:32) d
(cid:89)

wek −

vin[i]

e1→v1

e2→v2...

ed→vout[j]

k=1

2/p

(cid:33)p



w(t)
ek

)

d
(cid:89)

k=1

The steepest descent step (6) is hard to calculate exactly. Instead, we will update each coordinate we inde-
pendently (and synchronously) based on (6). That is:

w(t+1)
e

= arg min
we

J (t)(w)

s.t. ∀e(cid:48)(cid:54)=e we(cid:48) = w(t)
e(cid:48)

(7)

Taking the partial derivative with respect to we and setting it to zero we obtain:

0 = η

∂L
∂we

(w(t)) −

(cid:16)

we − w(t)
e

(cid:17)






(cid:88)

(cid:89)

vin[i]···

e
→...vout[j]

ek(cid:54)=e



2/p

p

(cid:12)
(cid:12)w(t)
(cid:12)

e

(cid:12)
(cid:12)
(cid:12)




where vin[i] · · ·
Solving for we gives us the following update rule:

e→ . . . vout[j] denotes the paths from any input unit i to any output unit j that includes e.

where γp(w, e) is given as

ˆw(t+1)
e

= w(t)

e −

η
γp(w(t), e)

∂L
∂w

(w(t))

γp(w, e) =






(cid:88)

(cid:89)

vin[i]···

e
→...vout[j]

ek(cid:54)=e



2/p

|wek |p




(8)

(9)

We call the optimization using the update rule (8) path-normalized gradient descent. When used in stochastic
settings, we refer to it as Path-SGD .

Now that we know Path-SGD is an approximate steepest descent with respect to the path-regularizer, we
can ask whether or not this makes Path-SGD a rescaling invariant optimization method. The next theorem
proves that Path-SGD is indeed rescaling invariant.

5

in

Algorithm 1 Path-SGD update rule
γin(v) = 1
1: ∀v∈V 0
2: ∀v∈V 0
γout(v) = 1
3: for i = 1 to d do
∀v∈V i
4:
∀v∈V i

γin(v) = (cid:80)
γout(v) = (cid:80)

out

in

(u→v)∈E γin(u) (cid:12)
(cid:12)
(cid:12)w(v,u)

(cid:12)
p
(cid:12)w(u,v)
(cid:12)
(cid:12)
p γout(u)
(cid:12)

out

(v→u)∈E

5:
6: end for
7: ∀(u→v)∈E γ(w(t), (u, v)) = γin(u)2/pγout(v)2/p
8: ∀e∈Ew(t+1)

= w(t)

(w(t))

e −

e

η
γ(w(t),e)

∂L
∂we

(cid:46) Initialization

(cid:46) Update Rule

Theorem 4.1. Path-SGD is rescaling invariant.

Proof. It is sufﬁcient to prove that using the update rule (8), for any c > 0 and any v ∈ E, if ˜w(t) =
ρc,v(w(t)), then ˜w(t+1) = ρc,v(w(t+1)). For any edge e in the network, if e is neither incoming nor out-
going edge of the node v, then ˜w(e) = w(e), and since the gradient is also the same for edge e we have
˜w(t+1)
. However, if e is an incoming edge to v, we have that ˜w(t)(e) = cw(t)(e). Moreover,
e
since the outgoing edges of v are divided by c, we get γp( ˜w(t), e) = γp(w(t),e)
(w(t)).
Therefore,

( ˜w(t)) = ∂L
c∂we

= w(t+1)
e

and ∂L
∂we

c2

˜w(t+1)
e

= cw(t)

e −

c2η
γp(w(t), e)

(cid:18)

= c

w(t) −

η
γp(w(t), e)

(cid:19)

(w(t))

= cw(t+1)
e

.

(w(t))

∂L
c∂we
∂L
∂we

A similar argument proves the invariance of Path-SGD update rule for outgoing edges of v. Therefore,
Path-SGD is rescaling invariant.

Efﬁcient Implementation: The Path-SGD update rule (8), in the way it is written, needs to consider all
the paths, which is exponential in the depth of the network. However, it can be calculated in a time that is no
more than a forward-backward step on a single data point. That is, in a mini-batch setting with batch size B,
if the backpropagation on the mini-batch can be done in time BT , the running time of the Path-SGD on the
mini-batch will be roughly (B + 1)T – a very moderate runtime increase with typical mini-batch sizes of
hundreds or thousands of points. Algorithm 1 shows an efﬁcient implementation of the Path-SGD update
rule.

We next compare Path-SGD to other optimization methods in both balanced and unbalanced settings.

5 Experiments

In this section, we compare (cid:96)2-Path-SGD to two commonly used optimization methods in deep learning,
SGD and AdaGrad. We conduct our experiments on four common benchmark datasets: the standard MNIST
dataset of handwritten digits [8]; CIFAR-10 and CIFAR-100 datasets of tiny images of natural scenes [7];
and Street View House Numbers (SVHN) dataset containing color images of house numbers collected by
Google Street View [10]. Details of the datasets are shown in Table 1.

In all of our experiments, we trained feed-forward networks with two hidden layers, each containing
4000 hidden units. We used mini-batches of size 100 and the step-size of 10−α, where α is an integer
between 0 and 10. To choose α, for each dataset, we considered the validation errors over the validation set

6

Table 1: General information on datasets used in the experiments.

Data Set
CIFAR-10
CIFAR-100
MNIST
SVHN

Dimensionality
3072 (32 × 32 color)
3072 (32 × 32 color)
784 (28 × 28 grayscale)
3072 (32 × 32 color)

Classes Training Set Test Set
10000
50000
10000
50000
10000
60000
26032
73257

10
100
10
10

Cross-Entropy Training Loss

0/1 Training Error

0/1 Test Error

0
1
-
R
A
F
I
C

0
0
1
-
R
A
F
I
C

T
S
I
N
M

N
H
V
S

Figure 2: Learning curves using different optimization methods for 4 datasets without dropout. Left panel displays
the cross-entropy objective function; middle and right panels show the corresponding values of the training and test
errors, where the values are reported on different epochs during the course of optimization. Best viewed in color.

(10000 randomly chosen points that are kept out during the initial training) and picked the one that reaches
the minimum error faster. We then trained the network over the entire training set. All the networks were
trained both with and without dropout. When training with dropout, at each update step, we retained each

7

02040608010000.511.522.5.020406080100012345.02040608010000.511.522.5.02040608010000.511.522.5Epoch.02040608010000.050.10.150.2.02040608010000.020.040.060.080.1.02040608010000.0050.010.0150.02.02040608010000.050.10.150.2Epoch.0204060801000.40.450.50.550.6.  Path−SGD − UnbalancedSGD − BalancedSGD − UnbalancedAdaGrad − BalancedAdaGrad − Unbalanced0204060801000.650.70.750.80.85.0204060801000.0150.020.0250.030.035.0204060801000.140.150.160.170.180.190.2Epoch.Cross-Entropy Training Loss

0/1 Training Error

0/1 Test Error

0
1
-
R
A
F
I
C

0
0
1
-
R
A
F
I
C

T
S
I
N
M

N
H
V
S

Figure 3: Learning curves using different optimization methods for 4 datasets with dropout. Left panel displays the
cross-entropy objective function; middle and right panels show the corresponding values of the training and test errors.
Best viewed in color.

unit with probability 0.5.

We tried both balanced and unbalanced initializations. In balanced initialization, incoming weights to
each unit v are initialized to i.i.d samples from a Gaussian distribution with standard deviation 1/(cid:112)fan-in(v).
In the unbalanced setting, we ﬁrst initialized the weights to be the same as the balanced weights. We then
picked 2000 hidden units randomly with replacement. For each unit, we multiplied its incoming edge and
divided its outgoing edge by 10c, where c was chosen randomly from log-normal distribution.

The optimization results without dropout are shown in Figure 2. For each of the four datasets, the plots
for objective function (cross-entropy), the training error and the test error are shown from left to right where
in each plot the values are reported on different epochs during the optimization. Although we proved that
Path-SGD updates are the same for balanced and unbalanced initializations, to verify that despite numerical
issues they are indeed identical, we trained Path-SGD with both balanced and unbalanced initializations.
Since the curves were exactly the same we only show a single curve.

We can see that as expected, the unbalanced initialization considerably hurts the performance of SGD

8

02040608010000.511.522.5.020406080100012345.02040608010000.511.522.5.02040608010000.511.522.5Epoch.02040608010000.10.20.30.4.02040608010000.20.40.60.8.02040608010000.020.040.060.08.02040608010000.10.20.30.4Epoch.0204060801000.350.40.450.50.55.  Path−SGD + DropoutSGD + DropoutAdaGrad + Dropout0204060801000.60.650.70.750.8.0204060801000.0150.020.0250.030.035.0204060801000.120.130.140.150.160.170.18Epoch.and AdaGrad (in many cases their training and test errors are not even in the range of the plot to be dis-
played), while Path-SGD performs essentially the same. Another interesting observation is that even in
the balanced settings, not only does Path-SGD often get to the same value of objective function, training
and test error faster, but also the ﬁnal generalization error for Path-SGD is sometimes considerably lower
than SGD and AdaGrad (except CIFAR-100 where the generalization error for SGD is slightly better com-
pared to Path-SGD ). The plots for test errors could also imply that implicit regularization due to steepest
descent with respect to path-regularizer leads to a solution that generalizes better. This view is similar to
observations in [11] on the role of implicit regularization in deep learning.

The results for training with dropout are shown in Figure 3, where here we suppressed the (very poor)
results on unbalanced initializations. We observe that except for MNIST, Path-SGD convergences much
faster than SGD or AdaGrad. It also generalizes better to the test set, which again shows the effectiveness
of path-normalized updates.

The results suggest that Path-SGD outperforms SGD and AdaGrad in two different ways. First, it can
achieve the same accuracy much faster and second, the implicit regularization by Path-SGD leads to a local
minima that can generalize better even when the training error is zero. This can be better analyzed by
looking at the plots for more number of epochs which we have provided in Figures 4 and 5. We should also
point that Path-SGD can be easily combined with AdaGrad to take advantage of the adaptive stepsize or
used together with a momentum term. This could potentially perform even better compare to Path-SGD .

6 Discussion

We revisited the choice of the Euclidean geometry on the weights of RELU networks, suggested an alterna-
tive optimization method approximately corresponding to a different geometry, and showed that using such
an alternative geometry can be beneﬁcial. In this work we show proof-of-concept success, and we expect
Path-SGD to be beneﬁcial also in large-scale training for very deep convolutional networks. Combining
Path-SGD with AdaGrad, with momentum or with other optimization heuristics might further enhance re-
sults.

Although we do believe Path-SGD is a very good optimization method, and is an easy plug-in for SGD,
we hope this work will also inspire others to consider other geometries, other regularizers and perhaps better,
update rules. A particular property of Path-SGD is its rescaling invariance, which we argue is appropriate
for RELU networks. But Path-SGD is certainly not the only rescaling invariant update possible, and other
invariant geometries might be even better.

Finally, we choose to use steepest descent because of its simplicity of implementation. A better choice
might be mirror descent with respect to an appropriate potential function, but such a construction seems
particularly challenging considering the non-convexity of neural networks.

Acknowledgments

Research was partially funded by NSF award IIS-1302662 and Intel ICRI-CI. We thank Hao Tang for in-
sightful discussions.

References

[1] John Duchi, Elad Hazan, and Yoram Singer. Adaptive subgradient methods for online learning and

stochastic optimization. The Journal of Machine Learning Research, 12:2121 – 2159, 2011.

[2] Xavier Glorot and Yoshua Bengio. Understanding the difﬁculty of training deep feedforward neural

networks. In AISTATS, 2010.

9

[3] Ian J. Goodfellow, David Warde-Farley, Mehdi Mirza, Aaron C. Courville, and Yoshua Bengio. Max-
out networks. In Proceedings of the 30th International Conference on Machine Learning, ICML, pages
1319–1327, 2013.

[4] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Delving deep into rectiﬁers: Surpassing

human-level performance on imagenet classiﬁcation. arXiv preprint arXiv:1502.01852, 2015.

[5] Sergey Ioffe and Christian Szegedy. Batch normalization: Accelerating deep network training by

reducing internal covariate shift. In arXiv, 2015.

[6] D. P. Kingma and J. Ba. Adam: A method for stochastic optimization. CoRR, abs/1412.6980, 2014.

[7] Alex Krizhevsky and Geoffrey Hinton. Learning multiple layers of features from tiny images. Com-

puter Science Department, University of Toronto, Tech. Rep, 1(4):7, 2009.

[8] Yann LeCun, L´eon Bottou, Yoshua Bengio, and Patrick Haffner. Gradient-based learning applied to

document recognition. Proceedings of the IEEE, 86(11):2278–2324, 1998.

[9] James Martens and Roger Grosse. Optimizing neural networks with kronecker-factored approximate

curvature. In ICML, 2015.

[10] Yuval Netzer, Tao Wang, Adam Coates, Alessandro Bissacco, Bo Wu, and Andrew Y Ng. Reading
digits in natural images with unsupervised feature learning. In NIPS workshop on deep learning and
unsupervised feature learning, 2011.

[11] Behnam Neyshabur, Ryota Tomioka, and Nathan Srebro. In search of the real inductive bias: On the
role of implicit regularization in deep learning. International Conference on Learning Representations
(ICLR) workshop track, 2015.

[12] Behnam Neyshabur, Ryota Tomioka, and Nathan Srebro. Norm-based capacity control in neural net-

works. COLT, 2015.

[13] Nathan Srebro and Adi Shraibman. Rank, trace-norm and max-norm.

In Learning Theory, pages

545–560. Springer, 2005.

[14] Nathan Srebro, Karthik Sridharan, and Ambuj Tewari. On the universality of online mirror descent. In

Advances in neural information processing systems, pages 2645–2653, 2011.

[15] Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan Salakhutdinov.
Dropout: A simple way to prevent neural networks from overﬁtting. The Journal of Machine Learning
Research, 15(1):1929–1958, 2014.

[16] I. Sutskever, J. Martens, George Dahl, and Geoffery Hinton. On the importance of momentum and

initialization in deep learning. In ICML, 2013.

10

Cross-Entropy Training Loss

0/1 Training Error

0/1 Test Error

0
1
-
R
A
F
I
C

0
0
1
-
R
A
F
I
C

T
S
I
N
M

N
H
V
S

Figure 4: Learning curves for more number of epochs using different optimization methods for 4 datasets without
dropout. Left panel displays the cross-entropy objective function; middle and right panels show the corresponding val-
ues of the training and test errors, where the values are reported on different epochs during the course of optimization.
Best viewed in color.

11

05010015020025030000.511.522.5.050100150200250300012345.05010015020025030000.511.522.5.05010015020025030000.511.522.5Epoch.05010015020025030000.050.10.150.2.05010015020025030000.020.040.060.080.1.05010015020025030000.0050.010.0150.02.05010015020025030000.050.10.150.2Epoch.0501001502002503000.40.450.50.550.6.  Path−SGD − UnbalancedSGD − BalancedSGD − UnbalancedAdaGrad − BalancedAdaGrad − Unbalanced0501001502002503000.650.70.750.80.85.0501001502002503000.0150.020.0250.030.035.0501001502002503000.140.150.160.170.180.190.2Epoch.Cross-Entropy Training Loss

0/1 Training Error

0/1 Test Error

0
1
-
R
A
F
I
C

0
0
1
-
R
A
F
I
C

T
S
I
N
M

N
H
V
S

Figure 5: Learning curves for more number of epochs using different optimization methods for 4 datasets with
dropout. Left panel displays the cross-entropy objective function; middle and right panels show the corresponding
values of the training and test errors. Best viewed in color.

12

010020030040000.511.522.5.0100200300400012345.010020030040000.511.522.5.010020030040000.511.522.5Epoch.010020030040000.10.20.30.4.010020030040000.20.40.60.8.010020030040000.020.040.060.08.010020030040000.10.20.30.4Epoch.01002003004000.350.40.450.50.55.  Path−SGD + DropoutSGD + DropoutAdaGrad + Dropout01002003004000.60.650.70.750.8.01002003004000.0150.020.0250.030.035.01002003004000.120.130.140.150.160.170.18Epoch.