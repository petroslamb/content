Nystr¨omformer: A Nystr¨om-based Algorithm for Approximating Self-Attention
Yunyang Xiong 1 Zhanpeng Zeng 1 Rudrasis Chakraborty 2 Mingxing Tan 3
Glenn Fung 4 Yin Li 1 Vikas Singh 1
1 University of Wisconsin-Madison 2 UC Berkeley 3 Google Brain 4 American Family Insurance
yxiong43@wisc.edu, zzeng38@wisc.edu, rudra@berkeley.edu, tanmingxing@google.com, gfung@amfam.com,
yin.li@wisc.edu, vsingh@biostat.wisc.edu
Abstract
Transformers have emerged as a powerful tool for a broad
range of natural language processing tasks. A key compo-
nent that drives the impressive performance of Transform-
ers is the self-attention mechanism that encodes the inﬂuence
or dependence of other tokens on each speciﬁc token. While
beneﬁcial, the quadratic complexity of self-attention on the
input sequence length has limited its application to longer se-
quences – a topic being actively studied in the community. To
address this limitation, we propose Nystr¨omformer – a model
that exhibits favorable scalability as a function of sequence
length. Our idea is based on adapting the Nystr ¨om method
to approximate standard self-attention with O(n) complex-
ity. The scalability of Nystr ¨omformer enables application to
longer sequences with thousands of tokens. We perform eval-
uations on multiple downstream tasks on the GLUE bench-
mark and IMDB reviews with standard sequence length, and
ﬁnd that our Nystr ¨omformer performs comparably, or in a
few cases, even slightly better, than standard self-attention.
On longer sequence tasks in the Long Range Arena (LRA)
benchmark, Nystr ¨omformer performs favorably relative to
other efﬁcient self-attention methods. Our code is available
at https://github.com/mlpen/Nystromformer.
Introduction
Transformer-based models, such as BERT (Devlin et al.
2019) and GPT-3 (Brown et al. 2020), have been very
successful in natural language processing (NLP), achiev-
ing state-of-the-art performance in machine translation
(Vaswani et al. 2017), natural language inference (Williams,
Nangia, and Bowman 2018), paraphrasing (Dolan and
Brockett 2005), text classiﬁcation (Howard and Ruder
2018), question answering (Rajpurkar et al. 2016) and many
other NLP tasks (Peters et al. 2018; Radford et al. 2018).
A key feature of transformers is what is known as the self-
attention mechanism (Vaswani et al. 2017), where each to-
ken’s representation is computed fromall other tokens. Self-
attention enables interactions of token pairs across the full
sequence and has been shown quite effective.
Despite the foregoing advantages, self-attention also turns
out to be a major efﬁciency bottleneck since it has a memory
and time complexity ofO(n2) where nis the length of an in-
put sequence. This leads to high memory and computational
Copyright © 2021, Association for the Advancement of Artiﬁcial
Intelligence (www.aaai.org). All rights reserved.
requirements for training large Transformer-based models.
For example, training a BERT-large model (Devlin et al.
2019) will need 4 months using a single Tesla V100 GPU
(equivalent to 4 days using a 4x4 TPU pod). Further, the
O(n2) complexity makes it prohibitively expensive to train
large Transformers with long sequences (e.g., n= 2048).
To address this challenge, several recent works have pro-
posed strategies that avoid incurring the quadratic cost when
dealing with longer input sequences. For example, (Dai
et al. 2019) suggests a trade-off between memory and com-
putational efﬁciency. The ideas described in (Child et al.
2019; Kitaev, Kaiser, and Levskaya 2019) decrease the self-
attention complexity to O(n√n) and O(nlog n) respec-
tively. In (Shen et al. 2018b; Katharopoulos et al. 2020;
Wang et al. 2020), self-attention complexity can be reduced
to O(n) with various approximation ideas, each with its own
strengths and limitations.
In this paper, we propose a O(n) approximation, both
in the sense of memory and time, for self-attention. Our
model, Nystr¨omformer, scales linearly with the input se-
quence length n. This is achieved by leveraging the cele-
brated Nystr¨om method, repurposed for approximating self-
attention. Speciﬁcally, our Nystr¨omFormer algorithm makes
use of landmark (or Nystr¨om) points to reconstruct the soft-
max matrix in self-attention, thereby avoiding computing the
n×nsoftmax matrix. We show that this yields a good ap-
proximation of the true self-attention.
To evaluate our method, we consider a transfer learning
setting using Transformers, where models are ﬁrst pretrained
with a language modeling objective on a large corpus, and
then ﬁnetuned on target tasks using supervised data (Devlin
et al. 2019; Liu et al. 2019; Lewis et al. 2020; Wang et al.
2020). Following BERT (Devlin et al. 2019; Liu et al. 2019),
we pretrain our proposed model on English Wikipedia and
BookCorpus (Zhu et al. 2015) using a masked-language-
modeling objective. We observe a similar performance to
the baseline BERT model on English Wikipedia and Book-
Corpus. We then ﬁnetune our pretrained models on multi-
ple downstream tasks in the GLUE benchmark (Wang et al.
2018) and IMDB reviews (Maas et al. 2011), and compare
our results to BERT in both accuracy and efﬁciency. Across
all tasks, our model compares favorably to the vanilla pre-
trained BERT with signiﬁcant speedups.
Finally, we evaluate our model on tasks with longer se-
arXiv:2102.03902v3  [cs.CL]  31 Mar 2021

quence lengths from the Long Range Arena (LRA) bench-
mark (Tay et al. 2020). Nystr¨omFormer performs well com-
pared to several recent efﬁcient self-attention methods, in-
cluding Reformer (Kitaev, Kaiser, and Levskaya 2019), Lin-
former (Wang et al. 2020), and Performer (Choromanski
et al. 2020), by margin of ∼3.4% in average accuracy. We
believe that the idea is a step towards resource efﬁcient
Transformers.
Related Work
We brieﬂy review relevant works on efﬁcient Transformers,
linearized Softmax kernels and Nystr¨om-like methods.
Efﬁcient Transformers . Weight pruning (Michel, Levy,
and Neubig 2019), weight factorization (Lan et al. 2020),
weight quantization (Zafrir et al. 2019) or knowledge dis-
tillation (Sanh et al. 2019) are several strategies that have
been proposed to improve memory efﬁciency in Transform-
ers. The use of a new pretraining objective in (Clark et al.
2019), product-key attention in (Lample et al. 2019), and
the Transformer-XL model in (Dai et al. 2019) have shown
how the overall compute requirements can be reduced. In
(Child et al. 2019), a sparse factorization of the attention
matrix was used for reducing the overall complexity from
quadratic to O(n√n) for generative modeling of long se-
quences. In (Kitaev, Kaiser, and Levskaya 2019), the Re-
former model further reduced the complexity to O(nlog n)
via locality-sensitive-hashing (LSH). This relies on perform-
ing fewer dot product operations overall by assuming that
the keys need to be identical to the queries. Recently, in
(Wang et al. 2020), the Linformer model suggested the use
of random projections based on the JL lemma to reduce the
complexity to O(n) with a linear projection step. The Long-
former model in (Beltagy, Peters, and Cohan 2020) achieved
a O(n) complexity using a local windowed attention and a
task-motivated global attention for longer documents, while
BIGBIRD (Zaheer et al. 2020) used a sparse attention mech-
anism. There are also other existing approaches to improve
optimizer efﬁciency, such as micro-batching (Huang et al.
2019) and gradient checkpointing (Chen et al. 2016). Con-
currently with our developments, the Performer model pro-
posed in (Choromanski et al. 2020) made use of positive or-
thogonal random features to approximate softmax attention
kernels with O(n) complexity.
Linearized Softmax. In (Blanc and Rendle 2018), an adap-
tive sampled softmax with a kernel based sampling was
shown to speed up training. It involves sampling only some
of the classes at each training step using a linear dot product
approximation. In (Rawat et al. 2019), the Random Fourier
Softmax (RF-softmax) idea uses random Fourier features
to perform efﬁcient sampling from an approximate soft-
max distribution for normalized embedding. In (Shen et al.
2018b; Katharopoulos et al. 2020), linearizing the softmax
attention in transformers was based on heuristically separat-
ing keys and queries in a linear dot product approximation.
While the idea is interesting, the approximation error to the
softmax matrix in self-attention can be large in some cases.
The lambda layers in (Bello 2021), can also be thought of as
an efﬁcient relative attention mechanism.
Nystr¨om-like methods . Nystr ¨om-like methods sample
columns of the matrix to achieve a close approximation to
the original matrix. The Nystr ¨om method (Baker 1977) was
developed as a way of discretizing an integral equation with
a simple quadrature rule and remains a widely used approach
for approximating the kernel matrix with a given sampled
subset of columns (Williams and Seeger 2001). Many vari-
ants such as Nystr ¨om with k-means (Zhang, Tsang, and
Kwok 2008; Zhang and Kwok 2010), randomized Nystr ¨om
(Li, Kwok, and L¨u 2010), Nystr¨om with spectral shift (Wang
et al. 2014), Nystr ¨om with pseudo landmarks, prototype
method (Wang and Zhang 2013; Wang, Zhang, and Zhang
2016), fast-Nys (Si, Hsieh, and Dhillon 2016), and MEKA
(Si, Hsieh, and Dhillon 2017), ensemble Nystr ¨om (Kumar,
Mohri, and Talwalkar 2009) have been proposed for spe-
ciﬁc improvements over the basic Nystr ¨om approximation.
In (Nemtsov, Averbuch, and Schclar 2016), the Nystr ¨om
method was extended to deal with a general matrix (rather
than a symmetric matrix). The authors in (Musco and Musco
2017) introduced the RLS-Nystr¨om method, which proposes
a recursive sampling approach to accelerate landmark points
sampling. (Fanuel, Schreurs, and Suykens 2019) developed
DAS (Deterministic Adaptive Sampling) and RAS (Ran-
domized Adaptive Sampling) algorithms to promote diver-
sity of landmarks selection.
The most related ideas to our development are (Wang and
Zhang 2013; Musco and Musco 2017). These approaches
are designed for general matrix approximation (which ac-
curately reﬂects our setup) while only sampling a subset of
columns and rows. However, directly applying these meth-
ods to approximate a softmax matrix used by self-attention
does not directly reduce the computational complexity. This
is because that even accessing a subset of columns or rows of
a softmax matrix will require the calculation of all elements
in the full matrix before the softmax function. And calcu-
lating these entries will incur a quadratic cost. Nonetheless,
inspired by the key idea of using a subset of columns to re-
construct the full matrix, we propose a Nystr¨om approxima-
tion with O(n) complexity tailored for the softmax matrix,
for approximating self-attention efﬁciently.
Nystr¨om-Based Linear Transformers
In this section, we start by brieﬂy reviewing self-attention,
then discuss the basic idea of Nystr ¨om approximation
method for the softmax matrix in self-attention, and ﬁnally
adapting this idea to achieve our proposed construction.
Self-Attention
What is self-attention? Self-attention calculates a weighted
average of feature representations with the weight propor-
tional to a similarity score between pairs of representations.
Formally, an input sequence of n tokens of dimensions d,
X ∈Rn×d, is projected using three matrices WQ ∈Rd×dq ,
WK ∈Rd×dk , and WV ∈Rd×dv to extract feature repre-
sentations Q, K, and V, referred to as query, key, and value
respectively with dk = dq. The outputs Q, K, V are com-
puted as
Q = XWQ, K = XWK, V = XWV . (1)

So, self-attention can be written as,
D(Q, K, V) =SV = softmax
(
QKT
√
dq
)
V, (2)
where softmax denotes a row-wise softmax normalization
function. Thus, each element in the softmax matrix S de-
pends on all other elements in the same row.
Compute cost of self-attention . The self-attention mecha-
nism requires calculating n2 similarity scores between each
pair of tokens, leading to a complexity of O(n2) for both
memory and time. Due to this quadratic dependence on the
input length, the application of self-attention is limited to
short sequences (e.g., n <1000). This is a key motivation
for a resource-efﬁcient self-attention module.
Nystr¨om Method for Matrix Approximation
The starting point of our work is to reduce the computational
cost of self-attention in Transformers using the Nystr ¨om
method, widely adopted for matrix approximation (Williams
and Seeger 2001; Drineas and Mahoney 2005; Wang and
Zhang 2013). Following (Wang and Zhang 2013), we de-
scribe a potential strategy and its challenges for using the
Nystr¨om method to approximate the softmax matrix in self-
attention by sampling a subset of columns and rows.
Denote the softmax matrix used in self-attention S =
softmax
(
QKT
√
dq
)
∈Rn×n. Scan be written as
S = softmax
(
QKT
√
dq
)
=
[
AS BS
FS CS
]
, (3)
where AS ∈Rm×m,BS ∈Rm×(n−m),FS ∈R(n−m)×m
and CS ∈R(n−m)×(n−m). AS is designated to be our sam-
ple matrix by sampling mcolumns and rows from S.
Quadrature technique. S can be approximated via the ba-
sic quadrature technique of the Nystr ¨om method. It begins
with the singular value decomposition (SVD) of the sample
matrix, AS = UΛVT , where U,V ∈Rm×m are orthogonal
matrices, Λ ∈Rm×m is a diagonal matrix. Based on the out-
of-sample columns approximation (Wang and Zhang 2013),
the explicit Nystr¨om form of Scan be reconstructed with m
columns and mrows from S,
ˆS =
[
AS BS
FS FSA+
S BS
]
=
[
AS
FS
]
A+
S [AS BS] , (4)
where A+
S is the Moore-Penrose inverse of AS. CS is
approximated by FSA+
S BS. Here, (4) suggests that the
n×n matrix S can be reconstructed by sampling m rows
(AS,BS) and mcolumns (AS,FS) from S and ﬁnding the
Nystr¨om approximation ˆS.
Nystr¨om approximation for softmax matrix. We brieﬂy
discuss how to construct the out-of-sample approximation
for the softmax matrix in self-attention using the standard
Nystr¨om method. Given a query qi and key kj, let
KK(qi) = softmax
(
qiKT
√
dq
)
; KQ(kj) = softmax
(
QkT
j√
dq
)
QKT : n × nn×m
nm
n
Figure 1: A key challenge of Nystr¨om approximation. The orange
block on the left shows a n ×m sub-matrix of S used by Nystr¨om
matrix approximation in (4). Computing the sub-matrix, however,
requires all entries in the n ×n matrix before the softmax function
(QKT ). Therefore, a direct application of Nystr¨om approximation
is problematic.
where KK(qi) ∈R1×n and KQ(kj) ∈Rn×1. We can then
construct
φK(qi) = Λ−1
2 VT [KT
K(qi)]m×1
φQ(kj) = Λ−1
2 UT [KQ(kj)]m×1
where [·]m×1 refers to calculating the full n×1 vector and
then taking the ﬁrst m×1 entries. With φK(qi) and φQ(kj)
available in hand, the entry of ˆS for standard Nystr ¨om ap-
proximation is calculated as,
ˆSij = φK(qi)T φQ(kj),∀i= 1,...,n,j = 1,...,n (5)
In matrix form, ˆScan be represented as,
ˆS=
[
softmax
(
QKT
√
dq
)]
n×m
A+
S
[
softmax
(
QKT
√
dq
)]
m×n
(6)
where [·]n×m refers to taking mcolumns from n×nmatrix
and [·]m×n refers to taking mrows from n×nmatrix. This
representation is the application of (4) for softmax matrix
approximation in self-attention.
[
AS
FS
]
in (4) corresponds to
the ﬁrst n×mmatrix in (6) and[AS BS] in (4) corresponds
to the last n×mmatrix in (6). More details of the matrix
representation is available in the supplement.
A key challenge of Nystr ¨om approximation. Unfortu-
nately, (4) and (6) require calculating all entries in QKT
due to the softmax function, even though the approximation
only needs to access a subset of the columns ofS, i.e.,
[
AS
FS
]
.
The problem arises due to the denominator within the row-
wise softmax function. Speciﬁcally, computing an element
in Srequires a summation of the exponential of all elements
in the same row of QKT . Thus, calculating
[
AS
FS
]
needs ac-
cessing the full QKT , shown in Fig. 1, and directly applying
Nystr¨om approximation as in (4) is not attractive.
Linearized Self-Attention via Nystr¨om Method
We now adapt the Nystr ¨om method to approximately cal-
culate the full softmax matrix S. The basic idea is to use
landmarks ˜K and ˜Q from key K and query Q to derive

softmax
≈ =
 ×
 ×
Nystr¨ om approximation
Figure 2: Illustration of a Nystr¨om approximation of softmax ma-
trix in self-attention. The left image shows the true softmax matrix
used in self-attention and the right images show its Nystr ¨om ap-
proximation. Our approximation is computed via multiplication of
three matrices.
an efﬁcient Nystr ¨om approximation without accessing the
full QKT . When the number of landmarks, m, is much
smaller than the sequence lengthn, our Nystr¨om approxima-
tion scales linearly w.r.t. input sequence length in the sense
of both memory and time.
Following the Nystr ¨om method, we also start with the
SVD of a smaller matrix, AS, and apply the basic quadra-
ture technique. But instead of subsampling the matrix after
the softmax operation – as one should do in principle – the
main modiﬁcation is to select landmarks ˜Qfrom queries Q
and ˜Kfrom keys Kbefore softmax and then form a m×m
matrix AS by applying the softmax operation on the land-
marks. We also form the matrices corresponding to the left
and right matrices in (4) using landmarks ˜Q and ˜K. This
provides a n×m matrix and m×n matrix respectively.
With these three n×m,m ×m,m ×n matrices we con-
structed, our Nystr¨om approximation of the n×nmatrix S
involves the multiplication of three matrices as in (4).
In the description that follows, we ﬁrst deﬁne the matrix
form of landmarks. Then, based on the landmarks matrix,
we form the three matrices needed for our approximation.
Deﬁnition 1. Let us assume that the selected landmarks for
inputs Q= [q1; ... ; qn] and K = [k1; ... ; kn] are {˜qj}m
j=1
and {˜kj}m
j=1 respectively. We denote the matrix form of the
corresponding landmarks as
For {˜qj}m
j=1, ˜Q= [ ˜q1; ... ; ˜qm] ∈Rm×dq
For {˜kj}m
j=1, ˜K = [ ˜k1; ... ; ˜km] ∈Rm×dq
The corresponding m×mmatrix is generated by
AS = softmax
(˜Q˜KT
√
dq
)
where AS = Um×mΛm×mVT
m×m
Note that in the SVD decomposition of AS, Um×m and
Vm×m are orthogonal matrices.
Similar to the out-of-sample approximation procedure
for the standard Nystr ¨om scheme described above, given a
query qi and key kj, let
K˜K(qi) = softmax
(
qi ˜KT
√
dq
)
; K˜Q(kj) = softmax
(˜QkT
j√
dq
)
,
where K˜K(qi) ∈R1×m and K˜Q(kj) ∈Rm×1. We can then
construct,
φ˜K(qi) = Λ
−1
2
m×mVT
m×mKT
˜K(qi)
φ˜Q(kj) = Λ
−1
2
m×mUT
m×mK˜Q(kj)
So, the entry for ˆSdepends on landmark matrices ˜K and ˜Q
and is calculated as,
ˆSij = φ˜K(qi)T φ˜Q(kj),∀i= 1,...,n,j = 1,...,n, (7)
To derive the explicit Nystr¨om form, ˆS, of the softmax ma-
trix with the threen×m, m×m, m×nmatrices, we assume
that AS is non-singular ﬁrst to guarantee that the above ex-
pression to deﬁne φ˜K and φ˜Q is meaningful. We will shortly
relax this assumption to achieve the general form as (4).
When AS is non-singular,
ˆSij = φ˜K(qi)T φ˜Q(kj) (8)
= K˜K(qi)Vm×mΛ−1
m×mUT
m×mK˜Q(kj). (9)
Let Wm = Vm×mΛ−1
m×mUT
m×m. Recall that a SVD ofAS is
Um×mΛm×mVT
m×m, and so, WmAS = Im×m. Therefore,
ˆSij = K˜K(qi)A−1
S K˜Q(kj) (10)
Based on (10), we can rewrite it to have a similar form as
(4) (i.e., not requiring that AS is non-singular) as
ˆSij = K˜K(qi)T A+
S K˜Q(kj), (11)
where A+
S is a Moore-Penrose pseudoinverse of AS. So,
ˆSij = softmax
(
qi ˜KT
√
dq
)
A+
S softmax
(˜QkT
j√
dq
)
, (12)
for i,j = {1,...,n }. The Nystr ¨om form of the softmax
matrix, S = softmax
(
QKT
√
dq
)
is thus approximated as
ˆS= softmax
(
Q ˜KT
√
dq
)(
softmax
(
˜Q ˜KT
√
dq
))+
softmax
(
˜QKT
√
dq
)
(13)
Note that we arrive at (13) via an out-of-sample approxi-
mation similar to (4). The difference is that in (13), the land-
marks are selected before the softmax operation to gener-
ate the out-of-sample approximation. This is a compromise
but avoids the need to compute the full softmax matrix S
for a Nystr¨om approximation. Fig. 2 illustrates the proposed
Nystr¨om approximation and Alg. 1 summarizes our method.
We now describe(a) the calculation of the Moore-Penrose
inverse and (b) the selection of landmarks.
Moore-Penrose inverse computation . Moore-Penrose
pseudoinverse can be calculated by using singular value de-
composition. However, SVD is not very efﬁcient on GPUs.
To accelerate the computation, we use an iterative method
from (Razavi et al. 2014) to approximate the Moore-Penrose
inverse via efﬁcient matrix-matrix multiplications.
Lemma 1. For AS ∈Rm×m, the sequence {Zj}j=∞
j=0 gen-
erated by (Razavi et al. 2014),
Zj+1 = 1
4Zj(13I −ASZj(15I −ASZj(7I −ASZj))) (14)
converges to the Moore-Penrose inverse A+
S in the third-
order with initial approximation Z0 satisfying ||ASA+
S −
ASZ0||<1.

Algorithm 1: Pipeline for Nystr ¨om approximation
of softmax matrix in self-attention
Input: Query Qand Key K.
Output: Nystr¨om approximation of softmax matrix.
Compute landmarks from input Qand landmarks
from input K, ˜Qand ˜Kas the matrix form ;
Compute ˜F = softmax(Q ˜KT
√
dq
), ˜B = softmax(
˜QKT
√
dq
) ;
Compute ˜A= softmax(
˜Q ˜KT
√
dq
)+;
return ˜F ×˜A×˜B;
We select Z0 by Z0 = AT
S/(||AS||1||AS||∞) where
||AS||1 = max
j
m∑
i=1
|(AS)ij|; ||AS||∞= max
i
n∑
j=1
|(AS)ij|,
based on (Pan and Schreiber 1991). This choice ensures that
||I−ASZ0||2 <1. When AS is non-singular,
||ASA+
S −ASZ0||2 = ||I−ASZ0||2 <1.
Without the non-singular constraint, the choice of initializ-
ing Z0 provides a good approximation in our experiments.
For all our experiments, we need to run about 6 iterations in
order to achieve a good approximation of the pseudoinverse.
Let A+
S be approximated by Z⋆ with (14). Our Nystr ¨om
approximation of Scan be written as
ˆS = softmax
(
Q ˜KT
√
dq
)
Z⋆softmax
(
˜QKT
√
dq
)
. (15)
Here, (15) only needs matrix-matrix multiplications, thus the
gradient computation is straight-forward.
Landmarks selection . Landmark points (inducing points
(Lee et al. 2019)) can be selected by using K-means cluster-
ing (Zhang, Tsang, and Kwok 2008; Vyas, Katharopoulos,
and Fleuret 2020). However, the EM style of updates in K-
means is less desirable during mini-batch training. We pro-
pose to simply use Segment-means similar to the local aver-
age pooling previously used in the NLP literature (Shen et al.
2018a). Speciﬁcally, for input queries Q= [q1; ... ; qn], we
separate the nqueries into msegments. As we can pad in-
puts to a length divisible to m, we assume n is divisible
by m for simplicity. Let l = n/m, landmark points for Q
are calculated as shown in (16). Similarly, for input keys
K = [k1; ... ; kn], landmarks are computed as shown below
in (16).
˜qj =
(j−1)×l+m∑
i=(j−1)×l+1
qi
m, ˜kj =
(j−1)×l+m∑
i=(j−1)×l+1
ki
m, (16)
where j = 1,··· ,m. Segment-means requires a single scan
of the sequence to compute the landmarks leading to a com-
plexity of O(n). We ﬁnd that using 64 landmarks is often
sufﬁcient to ensure a good approximation, although this de-
pends on the application. More details regarding the land-
mark selection is provided in the supplement.
True self-attention
Nystr¨om approximate self-attention
Figure 3: An example of Nystr¨om approximation vs. ground-truth
self-attention. Top: standard self-attention computed by (2). Bot-
tom: self-attention from our proposed Nystr ¨om approximation in
(17). We see that the attention patterns are quite similar.
Approximate self-attention . With landmark points and
pseudoinverse computed, the Nystr ¨om approximation of
the softmax matrix can be calculated. By plugging in the
Nystr¨om approximation, we obtain a linearized version ˆSV,
to approximate the true self-attention SV,
ˆSV = softmax
(
Q ˜KT
√
dq
)
Z⋆softmax
(
˜QKT
√
dq
)
V. (17)
Fig. 3 presents an example of the ﬁdelity between Nystr ¨om
approximate self-attention versus true self-attention.
Complexity analysis. We now provide a complexity analy-
sis of the Nystr ¨om approximation, which needs to account
for landmark selection, pseudoinverse calculation, and the
matrix multiplications. Landmark selection using Segment-
means takes O(n). Iterative approximation of the pseudoin-
verse takes O(m3) in the worst case. The matrix multi-
plication ﬁrst calculates softmax (Q˜KT /
√
dq) ×Z⋆ and
softmax( ˜QKT /
√
dq) ×V, and then calculates the product
(softmax(Q˜KT /
√
dq)×Z⋆)×(softmax( ˜QKT /
√
dq)×V).
This costs O(nm2 +mndv +m3 +nmdv). The overall time
complexity is thusO(n+m3 +nm2 +mndv +m3 +nmdv).
In terms of memory, storing the landmarks matrix ˜Qand ˜K
involves a O(mdq) cost and storing four Nystr ¨om approxi-
mation matrices has a O(nm+m2 +mn+ndv) cost. Thus,
the memory footprint is O(mdq + nm+ m2 + mn+ ndv).
When the number of landmarks m≪n, the time and mem-
ory complexity of our Nystr¨om approximation is O(n), i.e.,
scales linearly w.r.t. the input sequence length n.
Analysis of Nystr¨om Approximation
The following simple result analyzes an idealized setting and
states that the Galerkin discretization of φ˜K(q)T φ˜Q(k) with
the same set of landmark points, induces the same Nystr ¨om
matrix, in particular, the samen×nNystr¨om approximation
ˆSij. This result agrees with the discussion in (Bremer 2012).
Lemma 2. Given the input data set Q = {qi}n
i=1 and
K = {ki}n
i=1, and the corresponding landmark point set
˜Q = {˜qj}m
j=1 and ˜Kj = {˜k}m
j=1. Using (17), the Nystr ¨om
approximate self-attention converges to true self-attention if

Q :
n×dp
KT : dp × n
V :
n × dv
X :
n × d
˜Q :
m×dp
˜KT : dp ×m
m×m m×m×
m × n
n ×m×
×
n ×m×
m × dv×
n × dv× O :
n × dv
+
DConv
k × 1 n × dv
sMEANS
sMEANS
pINV
Figure 4: The proposed architecture of efﬁcient self-attention via Nystr¨om approximation. Each box represents an input, output, or interme-
diate matrix. The variable name and the size of the matrix are inside box.×denotes matrix multiplication, and+ denotes matrix addition. The
orange colored boxes are those matrices used in the Nystr¨om approximation. The green boxes are the skip connection added in parrallel to the
approximation. The dashed bounding box illustrates the three matrices of Nystro ¨om approximate softmax matrix in self-attention in Eq. 15.
sMEANS is the landmark selection using Segment-means (averaging m segments of input sequence). pINV is the iterative Moore-Penrose
pseudoinverse approximation. And DConv denotes depthwise convolution.
there exist landmarks points ˜qp and ˜kt such that ˜qp = qi and
˜kt = kj, ∀i= 1,...,n,j = 1,...,n .
Lemma 2 suggests that if the landmark points overlap
sufﬁciently with the original data points, the approximation
to self-attention will be good. While the condition here is
problem dependent, we note that it is feasible to achieve
an accurate approximation without using a large number of
landmarks. This is because (Oglic and G¨artner 2017) points
out that the error of Nystr ¨om approximation depends on the
spectrum of the matrix to be approximated and it decreases
with the rank of the matrix. When this result is compared
with the observation in (Wang et al. 2020) where the authors
suggest that self-attention is low-rank, stronger guarantees
based on structural properties of the matrix that we wish to
approximate are possible.
Our Model: Nystr¨omformer
Architecture. Our proposed architecture is shown in Fig. 4.
Given the input key K and query Q, our model ﬁrst uses
Segment-means to compute landmark points as matrices ˜K
and ˜Q. With the landmark points, our model then calcu-
lates the Nystr¨om approximation using approximate Moore-
Penrose pseudoinverse. A skip connection of value V, im-
plemented using a 1D depthwise convolution, is also added
to the model to help the training.
Experiments
We now present our experiments and results. Our experi-
ments follow a transfer learning setting that consists of two
stages. In the ﬁrst stage, we train Nystr¨omformer on a large-
scale text corpus, and report the language modeling per-
formance of our model on a hold-out validation set. In the
second stage, we ﬁne-tune the pre-trained Nystr ¨omformer
across several different NLP tasks in GLUE benchmarks
(Wang et al. 2019) and IMDB reviews (Maas et al. 2011),
and report the performance on individual dataset for each
task. In both stages, we compare our results to a baseline
Transformer model (BERT). In addition to language mod-
eling, we also conduct experiments on long range context
tasks in the Long Range Arena (LRA) benchmark.
(Pre-)training of Language Modeling
Our ﬁrst experiment evaluates if our model can achieve sim-
ilar performance with reduced complexity compared to a
standard Transformer on language modeling. We introduce
the dataset and evaluation protocol, describe implementation
details, and ﬁnally present the results of our model.
Dataset and metrics . We consider BookCorpus plus En-
glish Wikipedia as the training corpus, which is further split
into training (80%) and validation (20%) sets. Our model
is trained using the training set. We report the masked-
language-modeling (MLM) and sentence-order-prediction
(SOP) accuracy on the validation set, and compare the ef-
ﬁciency (runtime/memory) to a baseline.
Baselines. Our baseline is the well-known Transformer
based model – BERT (Devlin et al. 2019). Speciﬁcally, we
consider two variants of BERT:
• BERT-smallis a light weighted BERT model with 4 lay-
ers. We use BERT-small to compare to linear Transform-
ers, including ELU linearized self-attention (Katharopou-
los et al. 2020) and Linformer (Wang et al. 2020).
• BERT-base is the base model from (Devlin et al. 2019).
We use this model as our baseline when ﬁne-tuning on
downstream NLP tasks.
Our Nystr ¨omformer replaces the self-attention in BERT-
small and BERT-base using the proposed Nystr ¨om approx-
imation. We acknowledge that several very recent articles

self-attention input sequence length n512 1024 2048 4096 8192memory (MB)time(ms)memory (MB)time (ms)memory (MB)time (ms)memory (MB)time (ms)memory (MB)time (ms)
Transformer 54 (1×) 0.8 (1×) 186 (1×) 2.4 (1×) 685 (1×) 10.0 (1×) 2620 (1×) 32.9 (1×) 10233 (1×) 155.4 (1×)Linformer-25641 (1.3×) 0.7 (1.1×) 81 (2.3×) 1.3 (1.8×) 165 (4.2×) 2.7 (3.6×) 366 (7.2×) 5.3 (6.2×) 635 (16.1×) 11.3 (13.8×)Longformer-25732.2 (1.7×) 2.4 (0.3×) 65 (2.9×) 4.6 (0.5×) 130 (5.3×) 9.2 (1.0×) 263 (10.0×) 18.5 (1.8×) 455 (22.5×) 36.2 (4.3×)
Nystr¨omformer-6435 (1.5×) 0.7 (1.1×) 63 (3.0×) 1.3 (1.8×) 118 (5.8×) 2.7 (3.6×) 229 (11.5×) 5.9 (5.6×) 450 (22.8×) 12.3 (12.7×)Nystr¨omformer-3226 (2.1×) 0.6 (1.2×) 49 (3.8×) 1.2 (1.9×) 96 (7.1×) 2.6 (3.7×) 193 (13.6×) 5.6 (5.9×) 383 (26.7×) 11.5 (13.4×)
Table 1: Memory consumption and running time results on various input sequence length. We report the average memory consump-
tion (MB) and running time (ms) for one input instance with different input length through self-attention module. Nystr ¨omformer-64 de-
notes Nystr¨omformer self-attention module using 64 landmarks and Nystr¨omformer-32 denotes Nystr¨omformer module using 32 landmarks.
Linformer-256 denotes Linformer self-attention module using linear projection dimension 256. Longformer-257 denotes Longformer self-
attention using sliding window size 257(128 ×2 + 1). Our Nystr¨om self-attention offers favorable memory and time efﬁciency over standard
self-attention and Longformer self-attention. With a length of8192, our model offers 1.2×memory saving and 3×speed-up over Longformer,
and 1.7×memory saving over Linformer with similar running time.
(Zaheer et al. 2020; Beltagy, Peters, and Cohan 2020), con-
current with our work, have also proposed efﬁcient O(n)
self-attention for Transformers. An exhaustive comparison
to a rapidly growing set of algorithms is prohibitive unless
extensive compute resources are freely available. Thus, we
only compare runtime performance and the memory con-
sumption of our method to Linformer (Wang et al. 2020) and
Longformer (Beltagy, Peters, and Cohan 2020) in Table 1.
Implementation details . Our model is pre-trained with
the masked-language-modeling (MLM) and sentence-order-
prediction (SOP) objectives (Lan et al. 2020). We use a
batch size of 256, Adam optimizer with learning rate 1e-4,
β1 = 0 .9, β2 = 0 .999, L2 weight decay of 0.01, learn-
ing rate warm-up over the ﬁrst 10,000 steps, and linear
learning rate decay to update our model. Training BERT-
base with 1M update steps takes more than one week on
8 V100 GPUs. To keep compute costs reasonable, our base-
line (BERT-base) and our model are trained with 0.5M steps.
We also train our model with∼0.25M steps, initialized from
pre-trained BERT-base for speed-up. For BERT-small, we
train for 0.1M steps. More details are in the supplement.
Figure 5: Results on masked-language-modeling (MLM) and
sentence-order-prediction (SOP). On BERT-small, our Nystr ¨om
self-attention is competitive to standard self-attention, outperform-
ing Linformer and other linear self-attentions.
Results on accuracy and efﬁciency . We report the vali-
dation accuracy and inference efﬁciency of our model and
compare the results to transformer based models. In Fig. 5
and 6, we plot MLM and SOP pre-training validation ac-
curacy, which shows that Nystr ¨oformer is comparable to
a standard transformer and outperforms other variants of
efﬁcient transformers. We also note the computation and
memory efﬁciency of our model in Table 1. To evaluate
the inference time and memory efﬁciency, we generate ran-
dom inputs for self-attention module with sequence length
Figure 6: Results on MLM and SOP. We report MLM and
SOP validation accuracy for each training step. BERT-base (from
scratch) is trained with 0.5M steps, our Nystr ¨om (from scratch)
is trained with 0.5M steps as BERT-base (from scratch), and our
Nystr¨omformer (from standard) is trained with ∼0.25M steps ini-
tialized from pretrained BERT-base. Our Nystr¨om self-attention is
competitive with standard self-attention, BERT-base, and initializ-
ing from pretrained BERT-base helps speed up training.
n∈[512,1024,2048,4096,8192]. All models are evaluated
on the same machine setting with a Nvidia 1080Ti and we
report the improved inference speed and memory savings.
Model SST-2 MRPC QNLI QQP MNLI m/mmIMDB
BERT-base 90.0 88.4 90.3 87.3 82.4/82.4 93.3
Nystr¨omformer 91.4 88.1 88.7 86.3 80.9/82.2 93.2
Table 2: Results on natural language understanding tasks. We re-
port F1 score for MRPC and QQP and accuracy for others. Our
Nystr¨omformer performs competitively with BERT-base.
Fine-tuning on Downstream NLP tasks
Our second experiment is designed to test the generalization
ability of our model on downstream NLP tasks. To this end,
we ﬁne-tune the pretrained model across several NLP tasks.
Datasets and metrics . We consider the datasets of SST-
2 (Socher et al. 2013), MRPC (Dolan and Brockett 2005),
QNLI (Rajpurkar et al. 2016), QQP (Chen et al. 2018), and
MNLI (Williams, Nangia, and Bowman 2018) in GLUE
benchmark and IMDB reviews (Maas et al. 2011). We follow
the standard evaluation protocols, ﬁne-tune the pre-trained
model on the training set, report the results on the validation
set, and compare them to our baseline BERT-base.
Implementation details . We ﬁne-tune our pre-trained
model on GLUE benchmark datasets and IMDB reviews
respectively and report its ﬁnal performance. For larger

Model ListOps (2K) Text (4K) Retrieval (4K) Image (1K) Pathﬁnder (1K) Avg
Standard (Vaswani et al. 2017) 37.10 65.02 79.35 38.20 74.16 58.77
Reformer (Kitaev, Kaiser, and Levskaya 2019)19.05 64.88 78.64 43.29 69.36 55.04
Linformer (Wang et al. 2020) 37.25 55.91 79.37 37.84 67.60 55.59
Performer (Choromanski et al. 2020) 18.80 63.81 78.62 37.07 69.87 53.63
Nystr¨omformer (ours) 37.15 65.52 79.56 41.58 70.94 58.95
Table 3: Results on Long Range Arena (LRA) benchmark using our PyTorch implementation. We report classiﬁcation accuracy for each
individual task and average accuracy across all tasks. Our Nystr ¨omformer performs competitively with standard self-attention, and signiﬁ-
cantly outperforms Reformer, Linformer, and Performer. While we achieve consistent results reported in (Tay et al. 2020) for most tasks in
our PyTorch reimplementation, the performance on Retrieval task is higher for all models following the hyperparameters in (Tay et al. 2020).
datasets (SST-2, QNLI, QQP, MMNL, IMDB reviews), we
use a batch size of 32 and the AdamW optimizer with learn-
ing rate 3e-5 and ﬁne-tune our models for 4 epochs. For
MRPC, due to the sensitivity of a smaller dataset, we follow
(Devlin et al. 2019) by performing a hyperparameter search
with candidate batch size [8, 16, 32 ] and learning rate [2e-
5, 3e-5, 4e-5, 5e-5], and select the best validation result. As
these downstream tasks do not exceed the maximum input
sequence length 512, we ﬁne-tune our model trained on an
input sequence length of 512.
Results. Table 2 presents our experimental results on natu-
ral language understanding benchmarks with different tasks.
Our results compares favorably to BERT-base across all
downstream tasks. Further, we also experiment with ﬁne-
tuning our model using longer sequences ( n = 1024 ), yet
the results remain almost identical to n= 512, e.g. 93.0 vs.
93.2 accuracy on IMDB reviews. These results suggest that
our model is able to scale linearly with input length. Addi-
tional details on longer sequences is in the supplement.
Long Range Arena (LRA) Benchmark
Our last experiment evaluates our model on tasks with
longer sequence lengths. We follow the LRA benchmark
(Tay et al. 2020) and compare our method against other efﬁ-
cient self-attention variants.
Datasets and metrics . We consider the LRA benchmark
(Tay et al. 2020) with tasks of Listops (Nangia and Bow-
man 2018), byte-level IMDb reviews text classiﬁcation
(Maas et al. 2011), byte-level document retrieval (Radev
et al. 2013), image classiﬁcation on sequences of pixels
(Krizhevsky, Hinton et al. 2009), and Pathﬁnder (Linsley
et al. 2018). We follow the evaluation protocol from (Tay
et al. 2020), including the train/test splits, and report the
classiﬁcation accuracy for each task, as well as the average
accuracy across all tasks.
Baselines. We compare different self-attention methods us-
ing a same Transformer model. Our baselines consist of
the vanilla self-attention (Vaswani et al. 2017), and several
recent efﬁcient self-attention variants, including Reformer
(Kitaev, Kaiser, and Levskaya 2019), Linformer (Wang et al.
2020), and Performer (Choromanski et al. 2020).
Implementation details. The ofﬁcial LRA benchmark (Tay
et al. 2020) is implemented in Jax/Flax (Frostig, John-
son, and Leary 2018). To achieve a fair comparison to our
baselines implemented in PyTorch, we reimplemented the
benchmark in PyTorch and veriﬁed the results. All our ex-
periments, including our method and all baselines, use a
Transformer model with 2 layers, 64 embedding dimension,
128 hidden dimension, 2 attention heads. Mean pooling is
used for all tasks. The number of hashes for Reformer is 2,
the projection dimension for Linformer is 256, and random
feature dimension for Performer is 256.
Results. Table 3 compares our method to baselines. Our re-
sults are on par with the vanilla self-attention for all tasks,
with comparable average accuracy (+0.18%) but are more
efﬁcient (see Table 1). Importantly, our method outperforms
other efﬁcient self-attention methods, with +3.91%, +3.36%,
+5.32% in average accuracy against Reformer, Linformer,
and Performer, respectively. We ﬁnd that the model be-
haves favorably relative to the concurrent work of Performer
across all tasks, and in general, provides a good approxima-
tion to self-attention for longer sequences.
Conclusion
Scaling Transformer based models to longer sequences is
desirable in both NLP as well as computer vision, and it will
involve identifying ways to mitigate its compute and mem-
ory requirements. Within the last year, this need has led to
a number of results describing how randomized numerical
linear algebra schemes based on random projections and low
rank assumptions can help (Katharopoulos et al. 2020; Wang
et al. 2020; Beltagy, Peters, and Cohan 2020; Zaheer et al.
2020). Here, we approach this task differently by showing
how the Nystr¨om method, a widely used strategy for matrix
approximation, can be adapted and deployed within a deep
Transformer architecture to provide an efﬁcient approxima-
tion of self attention. We show that our design choices and
modiﬁcations enable all key operations to be mapped to
popular deep learning libraries conveniently. The algorithm
maintains the performance proﬁle of other self-attention ap-
proximations in the literature but offers additional beneﬁt of
resource utilization, and is a step towards building Trans-
former models on very long sequences. Our code/supp is
available at https://github.com/mlpen/Nystromformer.
Acknowledgments. This work was supported in part by a
American Family Insurance grant via American Family In-
surance Data Science Institute at UW, NSF CAREER award
RI 1252725 and UW CPCP (U54AI117924). We thank
Denny Zhou, Hongkun Yu, and Adam Yu for valuable dis-
cussions. The paper also beneﬁted from comments regarding
typos and suggestions pointed out by Yannic Kilcher, Sebas-
tian Bodenstein and Github user thomasw21. We thank Phil
Wang and Lekton Zhang for making their implementation
available at https://github.com/lucidrains/nystrom-attention.

References
Baker, C. T. 1977. The numerical treatment of integral equations.
Clarendon press.
Bello, I. 2021. LambdaNetworks: Modeling long-range Interac-
tions without Attention. In International Conference on Learning
Representations.
Beltagy, I.; Peters, M. E.; and Cohan, A. 2020. Longformer: The
Long-Document Transformer. arXiv:2004.05150 .
Blanc, G.; and Rendle, S. 2018. Adaptive sampled softmax with
kernel based sampling. In Proceedings of the International Con-
ference on Machine Learning (ICML), 590–599.
Bremer, J. 2012. On the Nystr ¨om discretization of integral equa-
tions on planar curves with corners. Applied and Computational
Harmonic Analysis 32(1): 45–64.
Brown, T. B.; Mann, B.; Ryder, N.; Subbiah, M.; Kaplan, J.; Dhari-
wal, P.; Neelakantan, A.; Shyam, P.; Sastry, G.; Askell, A.; et al.
2020. Language models are few-shot learners. arXiv preprint
arXiv:2005.14165 .
Chen, T.; Xu, B.; Zhang, C.; and Guestrin, C. 2016. Training deep
nets with sublinear memory cost. arXiv preprint arXiv:1604.06174
.
Chen, Z.; Zhang, H.; Zhang, X.; and Zhao, L. 2018. Quora question
pairs. URL https://www.kaggle.com/c/quora-question-pairs.
Child, R.; Gray, S.; Radford, A.; and Sutskever, I. 2019. Gen-
erating long sequences with sparse transformers. arXiv preprint
arXiv:1904.10509 .
Choromanski, K.; Likhosherstov, V .; Dohan, D.; Song, X.; Gane,
A.; Sarlos, T.; Hawkins, P.; Davis, J.; Mohiuddin, A.; Kaiser, L.;
et al. 2020. Rethinking attention with performers. arXiv preprint
arXiv:2009.14794 .
Clark, K.; Luong, M.-T.; Le, Q. V .; and Manning, C. D. 2019.
ELECTRA: Pre-training Text Encoders as Discriminators Rather
Than Generators. In International Conference on Learning Repre-
sentations (ICLR).
Dai, Z.; Yang, Z.; Yang, Y .; Carbonell, J. G.; Le, Q.; and Salakhut-
dinov, R. 2019. Transformer-XL: Attentive Language Models be-
yond a Fixed-Length Context. In Proceedings of the Annual Meet-
ing of the Association for Computational Linguistics (ACL), 2978–
2988.
Devlin, J.; Chang, M.-W.; Lee, K.; and Toutanova, K. 2019. BERT:
Pre-training of Deep Bidirectional Transformers for Language Un-
derstanding. In Proceedings of the Conference of the North Ameri-
can Chapter of the Association for Computational Linguistics: Hu-
man Language Technologies (NAACL-HLT).
Dolan, W. B.; and Brockett, C. 2005. Automatically constructing
a corpus of sentential paraphrases. In Proceedings of the Third
International Workshop on Paraphrasing (IWP2005).
Drineas, P.; and Mahoney, M. W. 2005. On the Nystr ¨om method
for approximating a Gram matrix for improved kernel-based learn-
ing. Journal of Machine Learning Research (JMLR)6(Dec): 2153–
2175.
Fanuel, M.; Schreurs, J.; and Suykens, J. A. 2019. Nystr \” om
landmark sampling and regularized Christoffel functions. arXiv
preprint arXiv:1905.12346 .
Frostig, R.; Johnson, M. J.; and Leary, C. 2018. Compiling ma-
chine learning programs via high-level tracing. Systems for Ma-
chine Learning .
Howard, J.; and Ruder, S. 2018. Universal Language Model Fine-
tuning for Text Classiﬁcation. In Proceedings of the 56th Annual
Meeting of the Association for Computational Linguistics (ACL) ,
328–339.
Huang, Y .; Cheng, Y .; Bapna, A.; Firat, O.; Chen, D.; Chen, M.;
Lee, H.; Ngiam, J.; Le, Q. V .; Wu, Y .; et al. 2019. Gpipe: Efﬁ-
cient training of giant neural networks using pipeline parallelism.
In Advances in Neural Information Processing Systems (NeurIPS),
103–112.
Katharopoulos, A.; Vyas, A.; Pappas, N.; and Fleuret, F. 2020.
Transformers are RNNs: Fast Autoregressive Transformers with
Linear Attention. In Proceedings of the International Conference
on Machine Learning (ICML).
Kitaev, N.; Kaiser, L.; and Levskaya, A. 2019. Reformer: The Ef-
ﬁcient Transformer. In International Conference on Learning Rep-
resentations (ICLR).
Krizhevsky, A.; Hinton, G.; et al. 2009. Learning multiple layers of
features from tiny images. Technical Report TR-2009, University
of Toronto.
Kumar, S.; Mohri, M.; and Talwalkar, A. 2009. Ensemble Nystr¨om
method. In Advances in Neural Information Processing Systems
(NeurIPS), 1060–1068.
Lample, G.; Sablayrolles, A.; Ranzato, M.; Denoyer, L.; and J´egou,
H. 2019. Large memory layers with product keys. In Advances in
Neural Information Processing Systems (NeurIPS), 8548–8559.
Lan, Z.; Chen, M.; Goodman, S.; Gimpel, K.; Sharma, P.; and Sori-
cut, R. 2020. ALBERT: A lite BERT for self-supervised learning of
language representations. In International Conference on Learning
Representations (ICLR).
Lee, J.; Lee, Y .; Kim, J.; Kosiorek, A.; Choi, S.; and Teh,
Y . W. 2019. Set transformer: A framework for attention-based
permutation-invariant neural networks. In International Confer-
ence on Machine Learning, 3744–3753. PMLR.
Lewis, M.; Liu, Y .; Goyal, N.; Ghazvininejad, M.; Mohamed, A.;
Levy, O.; Stoyanov, V .; and Zettlemoyer, L. 2020. BART: Denois-
ing sequence-to-sequence pre-training for natural language genera-
tion, translation, and comprehension. In Proceedings of the Annual
Meeting of the Association for Computational Linguistics (ACL) ,
7871–7880. Association for Computational Linguistics.
Li, M.; Kwok, J. T.-Y .; and L ¨u, B. 2010. Making large-scale
Nystr¨om approximation possible. In Proceedings of the Interna-
tional Conference on Machine Learning (ICML), 631.
Linsley, D.; Kim, J.; Veerabadran, V .; Windolf, C.; and Serre, T.
2018. Learning long-range spatial dependencies with horizontal
gated recurrent units. In Advances in Neural Information Process-
ing Systems (NeurIPS), 152–164.
Liu, Y .; Ott, M.; Goyal, N.; Du, J.; Joshi, M.; Chen, D.; Levy, O.;
Lewis, M.; Zettlemoyer, L.; and Stoyanov, V . 2019. RoBERTa:
A robustly optimized BERT pretraining approach. arXiv preprint
arXiv:1907.11692 .
Maas, A.; Daly, R. E.; Pham, P. T.; Huang, D.; Ng, A. Y .; and Potts,
C. 2011. Learning word vectors for sentiment analysis. InProceed-
ings of the 49th Annual Meeting of the Association for Computa-
tional Linguistics (ACL): Human language technologies, 142–150.
Michel, P.; Levy, O.; and Neubig, G. 2019. Are sixteen heads really
better than one? In Advances in Neural Information Processing
Systems, 14014–14024.
Musco, C.; and Musco, C. 2017. Recursive sampling for the nys-
trom method. In Advances in Neural Information Processing Sys-
tems (NeurIPS), 3833–3845.

Nangia, N.; and Bowman, S. R. 2018. ListOps: A Diagnostic
Dataset for Latent Tree Learning. In Cordeiro, S. R.; Oraby, S.;
Pavalanathan, U.; and Rim, K., eds.,Proceedings of the Conference
of the North American Chapter of the Association for Computa-
tional Linguistics: Human Language Technologies (NAACL-HLT),
92–99. Association for Computational Linguistics.
Nemtsov, A.; Averbuch, A.; and Schclar, A. 2016. Matrix compres-
sion using the Nystr ¨om method. Intelligent Data Analysis 20(5):
997–1019.
Oglic, D.; and G ¨artner, T. 2017. Nystr ¨om method with kernel k-
means++ samples as landmarks. Journal of Machine Learning Re-
search (JMLR) 2652–2660.
Pan, V .; and Schreiber, R. 1991. An improved Newton iteration
for the generalized inverse of a matrix, with applications. SIAM
Journal on Scientiﬁc and Statistical Computing 12(5): 1109–1130.
Peters, M. E.; Neumann, M.; Iyyer, M.; Gardner, M.; Clark, C.;
Lee, K.; and Zettlemoyer, L. 2018. Deep contextualized word rep-
resentations. In Proceedings of the Conference of the North Ameri-
can Chapter of the Association for Computational Linguistics: Hu-
man Language Technologies (NAACL-HLT), 2227–2237.
Radev, D. R.; Muthukrishnan, P.; Qazvinian, V .; and Abu-Jbara, A.
2013. The ACL anthology network corpus. Lang. Resour. Evalua-
tion 47(4): 919–944. doi:10.1007/s10579-012-9211-2.
Radford, A.; Narasimhan, K.; Salimans, T.; and Sutskever, I. 2018.
Improving language understanding with unsupervised learning.
Technical report, OpenAI .
Rajpurkar, P.; Zhang, J.; Lopyrev, K.; and Liang, P. 2016. SQuAD:
100,000+ Questions for Machine Comprehension of Text. In Pro-
ceedings of the Conference on Empirical Methods in Natural Lan-
guage Processing (EMNLP), 2383–2392.
Rawat, A. S.; Chen, J.; Yu, F. X. X.; Suresh, A. T.; and Kumar,
S. 2019. Sampled softmax with random fourier features. In
Advances in Neural Information Processing Systems (NeurIPS) ,
13857–13867.
Razavi, M. K.; Kerayechian, A.; Gachpazan, M.; and Shateyi, S.
2014. A new iterative method for ﬁnding approximate inverses of
complex matrices. In Abstract and Applied Analysis.
Sanh, V .; Debut, L.; Chaumond, J.; and Wolf, T. 2019. DistilBERT,
a distilled version of BERT: smaller, faster, cheaper and lighter.
arXiv preprint arXiv:1910.01108 .
Shen, D.; Wang, G.; Wang, W.; Min, M. R.; Su, Q.; Zhang, Y .; Li,
C.; Henao, R.; and Carin, L. 2018a. Baseline Needs More Love: On
Simple Word-Embedding-Based Models and Associated Pooling
Mechanisms. In Proceedings of the 56th Annual Meeting of the
Association for Computational Linguistics (ACL), 440–450.
Shen, Z.; Zhang, M.; Zhao, H.; Yi, S.; and Li, H. 2018b. Efﬁ-
cient Attention: Attention with Linear Complexities.arXiv preprint
arXiv:1812.01243 .
Si, S.; Hsieh, C.-J.; and Dhillon, I. 2016. Computationally efﬁcient
Nystr¨om approximation using fast transforms. In Proceedings of
the International Conference on Machine Learning (ICML), 2655–
2663.
Si, S.; Hsieh, C.-J.; and Dhillon, I. S. 2017. Memory efﬁcient ker-
nel approximation. Journal of Machine Learning Research (JMLR)
18(1): 682–713.
Socher, R.; Perelygin, A.; Wu, J.; Chuang, J.; Manning, C. D.; Ng,
A. Y .; and Potts, C. 2013. Recursive deep models for semantic
compositionality over a sentiment treebank. In Proceedings of the
Conference on Empirical Methods in Natural Language Process-
ing (EMNLP), 1631–1642.
Tay, Y .; Dehghani, M.; Abnar, S.; Shen, Y .; Bahri, D.; Pham, P.;
Rao, J.; Yang, L.; Ruder, S.; and Metzler, D. 2020. Long Range
Arena: A Benchmark for Efﬁcient Transformers. arXiv preprint
arXiv:2011.04006 .
Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.; Jones, L.;
Gomez, A. N.; Kaiser, Ł.; and Polosukhin, I. 2017. Attention is
all you need. In Advances in Neural Information Processing Sys-
tems (NeurIPS), 5998–6008.
Vyas, A.; Katharopoulos, A.; and Fleuret, F. 2020. Fast transform-
ers with clustered attention. Advances in Neural Information Pro-
cessing Systems 33.
Wang, A.; Singh, A.; Michael, J.; Hill, F.; Levy, O.; and Bowman,
S. R. 2018. GLUE: A Multi-Task Benchmark and Analysis Plat-
form for Natural Language Understanding. In International Con-
ference on Learning Representations (ICLR).
Wang, A.; Singh, A.; Michael, J.; Hill, F.; Levy, O.; and Bowman,
S. R. 2019. GLUE: A Multi-Task Benchmark and Analysis Plat-
form for Natural Language Understanding. In Proceedings of the
International Conference on Machine Learning.
Wang, S.; Li, B.; Khabsa, M.; Fang, H.; and Ma, H. 2020. Lin-
former: Self-Attention with Linear Complexity. arXiv preprint
arXiv:2006.04768 .
Wang, S.; Zhang, C.; Qian, H.; and Zhang, Z. 2014. Improving the
modiﬁed nystr ¨om method using spectral shifting. In Proceedings
of the 20th ACM SIGKDD International Conference on Knowledge
Discovery and Data Mining (KDD), 611–620.
Wang, S.; and Zhang, Z. 2013. Improving CUR matrix decomposi-
tion and the Nystr ¨om approximation via adaptive sampling. Jour-
nal of Machine Learning Research (JMLR) 14(1): 2729–2769.
Wang, S.; Zhang, Z.; and Zhang, T. 2016. Towards more efﬁcient
SPSD matrix approximation and CUR matrix decomposition.Jour-
nal of Machine Learning Research (JMLR) 17(1): 7329–7377.
Williams, A.; Nangia, N.; and Bowman, S. R. 2018. A Broad-
Coverage Challenge Corpus for Sentence Understanding through
Inference. In Proceedings of the Conference of the North American
Chapter of the Association for Computational Linguistics: Human
Language Technologies (NAACL-HLT), 1112–1122.
Williams, C. K.; and Seeger, M. 2001. Using the Nystr ¨om method
to speed up kernel machines. In Advances in Neural Information
Processing Systems (NeurIPS), 682–688.
Zafrir, O.; Boudoukh, G.; Izsak, P.; and Wasserblat, M. 2019.
Q8BERT: Quantized 8bit BERT. In NeurIPS Workshop on Energy
Efﬁcient Machine Learning and Cognitive Computing 2019.
Zaheer, M.; Guruganesh, G.; Dubey, A.; Ainslie, J.; Alberti, C.;
Ontanon, S.; Pham, P.; Ravula, A.; Wang, Q.; Yang, L.; et al.
2020. Big bird: Transformers for longer sequences. arXiv preprint
arXiv:2007.14062 .
Zhang, K.; and Kwok, J. T. 2010. Clustered Nystr ¨om method
for large scale manifold learning and dimension reduction. IEEE
Transactions on Neural Networks 21(10): 1576–1587.
Zhang, K.; Tsang, I. W.; and Kwok, J. T. 2008. Improved Nystr¨om
low-rank approximation and error analysis. In Proceedings of
the International Conference on Machine Learning (ICML), 1232–
1239.
Zhu, Y .; Kiros, R.; Zemel, R.; Salakhutdinov, R.; Urtasun, R.; Tor-
ralba, A.; and Fidler, S. 2015. Aligning books and movies: To-
wards story-like visual explanations by watching movies and read-
ing books. In Proceedings of the IEEE International Conference
on Computer Vision (ICCV), 19–27.