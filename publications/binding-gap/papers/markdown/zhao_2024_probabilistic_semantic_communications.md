1

A Joint Communication and Computation Design
for Semantic Wireless Communication with
Probability Graph

Zhouxiang Zhao, Zhaohui Yang, Xu Gan, Quoc-Viet Pham, Chongwen Huang,
Wei Xu, and Zhaoyang Zhang

3
2
0
2

c
e
D
2
2

]
T
I
.
s
c
[

2
v
5
7
9
3
1
.
2
1
3
2
:
v
i
X
r
a

Abstract—In this paper, we delve into the challenge of op-
timizing joint communication and computation for semantic
communication over wireless networks using a probability graph
framework. In the considered model, the base station (BS) ex-
tracts the small-sized compressed semantic information through
removing redundant messages based on the stored knowledge
base. Specifically, the knowledge base is encapsulated in a prob-
ability graph that encapsulates statistical relations. At the user
side, the compressed information is accurately deduced using the
same probability graph employed by the BS. While this approach
introduces an additional computational overhead for semantic
information extraction, it significantly curtails communication
resource consumption by transmitting concise data. We derive
both communication and computation cost models based on the
inference process of the probability graph. Building upon these
models, we introduce a joint communication and computation
resource allocation problem aimed at minimizing the overall
energy consumption of the network, while accounting for latency,
power, and semantic constraints. To address this problem, we
obtain a closed-form solution for transmission power under a
fixed semantic compression ratio. Subsequently, we propose an
efficient linear search-based algorithm to attain the optimal
solution for the considered problem with low computational
complexity. Simulation results underscore the effectiveness of our
proposed system, showcasing notable improvements compared to
conventional non-semantic schemes.

Index Terms—Semantic communication, knowledge graph,

probability graph, joint communication and computation.

I. INTRODUCTION

O VER the preceding decades, the evolution of mobile

communication technologies has played a pivotal role in
advancing human society. Shannon’s introduction of informa-
tion theory in the 1940s focused on quantifying the maximum
achievable data transmission rate through a communication
channel [1]. Subsequently, contemporary communication sys-
tems have predominantly been designed with an emphasis on
metrics related to transmission rates [2], [3]. However, the
escalating demand for intelligent applications in wireless com-
munication necessitates a shift from traditional architectures,

Z. Zhao, Z. Yang, X. Gan, C. Huang, and Z. Zhang are with College
of Information Science and Electronic Engineering, Zhejiang University, and
also with Zhejiang Provincial Key Laboratory of Info. Proc., Commun. &
Netw. (IPCAN), Hangzhou, China (e-mails: {zhouxiangzhao, yang zhaohui,
gan xu, chongwenhuang, ning ming}@zju.edu.cn).

Q. Pham is with School of Computer Science and Statistics, Trinity College

Dublin, Ireland (e-mail: viet.pham@tcd.ie).

W. Xu is with National Mobile Communications Research Laboratory,

Southeast University, Nanjing, China (e-mail: wxu@seu.edu.cn).

solely prioritizing high transmission rates, to novel architec-
tures geared towards task efficiency [4]–[6]. In the realm of
future wireless communications, mobile information networks
will confront
the challenge of accommodating tasks with
low latency and high efficiency [7]. This evolving landscape
has given rise to a new communication paradigm known as
semantic communication. Unlike Shannon’s theory, which did
not attribute significance to the semantic information of data,
deeming it largely irrelevant to communication, the concept
of semantic communication was introduced by Warren Weaver
[8]. Weaver’s three-layer communication framework delineates
the technical layer, concerned with traditional communication
and accurate transmission of symbols;
the semantic layer,
focused on conveying the meaning of communication sym-
bols; and the effectiveness layer, concentrated on how the
received meaning influences the receiver’s behavior. Semantic
communication represents an innovative architecture capable
of integrating user needs and information meaning into the
communication process [9], [10]. Unlike traditional commu-
nication systems dedicated solely to the reliable transmission
of bit streams without knowledge of the message’s meaning
or exchange goals, semantic communication systems prioritize
conveying meaning in the message [11], [12]. Consequently,
they can significantly reduce the required transmission channel
bandwidth [13]. In the context of future mobile communication
systems, semantic communication is anticipated to be a piv-
otal technology for the development of sixth-generation (6G)
networks [14], [15].

In recent studies, various investigations have delved into
diverse aspects of semantic communication. In [16], the au-
thors proposed a semantic communication system for text
transmission based on deep learning (DL). They introduced
a novel metric, sentence similarity, to assess the effectiveness
of semantic communication. Another contribution in [17]
focused on a DL-enabled semantic communication system
tailored for speech signals. The incorporation of an attention
mechanism, utilizing a squeeze-and-excitation network, aimed
to enhance the accuracy of speech signal recovery, particularly
for crucial
information. Additionally, work [18] addressed
the transmission of audio semantic information capturing
contextual features of audio signals. They introduced a wave-
to-vector architecture-based autoencoder, comprising convolu-
tional neural networks, to extract semantic information from
audio signals. Moreover, work [19] presented a lite distributed
semantic communication system named L-DeepSC, designed

2

constructing structured knowledge graphs from unstructured
textual data. NER identifies entities (people, places, organiza-
tions, etc.), while RE detects semantic relations between these
entities. The interpretability of knowledge graphs has spurred
research on the relationship between knowledge graphs and
semantics. Notably, [32] posited that knowledge graphs repre-
sent the next-generation infrastructure for semantic scholarly
knowledge, [33] suggested the potential use of knowledge
graphs in predicting semantic categories, and [34] integrated
knowledge graphs with semantic communication to enhance
communication credibility. Despite the effectiveness of knowl-
edge graphs in representing semantics, existing knowledge
graph-based semantic communication works [34]–[36] have
not established a knowledge base to further reduce commu-
nication load in semantic wireless communication networks.
While semantic communication techniques offer the advantage
of reducing transmitted data size, they introduce additional
computational overhead. Consequently, the allocation of re-
sources for both communication and computation remains an
underexplored area. To the best of our knowledge, this work
is the first to utilize a probability graph as the knowledge base
in semantic communication, considering both communication
and computation resource allocation.

The primary contribution of this paper lies in the develop-
ment of an innovative text information extraction system based
on probability graph, which takes into consideration both the
communication and computation energy consumption within
the semantic communication network. The key contributions
can be succinctly summarized as follows:

• We introduce a novel knowledge graph compression
method based on a probability graph shared by both the
base station (BS) and the user. The probability graph,
derived from knowledge graphs, extends the traditional
triple to a quadruple by incorporating the dimension of
relation probability. Leveraging this shared probability
graph allows the omission of redundant information in
the knowledge graph associated with the text, leading to
a reduction in transmitted data.

• We provide a computation energy cost model for inferring
the reduced information based on the probability graph.
This model serves as the foundation for addressing the
joint communication and computation resource allocation
problem in the semantic communication system. Our ap-
proach involves the simultaneous optimization of transmit
power and compression ratio. The formulated optimiza-
tion problem aims to minimize the overall communication
and computation energy consumption of the network,
while adhering to constraints related to latency, transmit
power, and semantic considerations.

• To solve the formulated problem, we develop an efficient
algorithm that computes the closed-form power allocation
for each omitted relation number. The proposed algorithm
is validated through numerical analysis, demonstrating
its effectiveness in optimizing resource allocation in the
semantic communication system.

The rest of this paper is organized as follows. The system
model and problem formulation are described in Section II.

Fig. 1. An example of knowledge graph.

for text transmission with low complexity. Operating at the
semantic level, this system facilitates data transmission from
Internet of Things (IoT) devices to the cloud/edge, thereby
improving transmission efficiency. In the domain of semantic-
oriented speech transmission, work [20] proposed an end-to-
end DL-based transceiver that extracts and encodes semantic
information from input speech spectrums at the transmitter,
delivering corresponding transcriptions from the decoded se-
mantic information at the receiver. Furthermore, work [21]
explored the mechanism of semantic noise and introduced a ro-
bust DL-enabled semantic communication system. Leveraging
a calibrated self-attention mechanism and adversarial training,
this system addresses semantic noise challenges. However,
it is noteworthy that the works mentioned above [16]–[21]
did not account for computation energy consumption in their
assessments of semantic communication systems. Previous
researches [22], [23] have demonstrated that efficient resource
allocation plays a crucial role in significantly improving the
performance of semantic communication.

Despite the progress made in semantic communication
research, the field is still in its early stages, facing challenges
that impede its development, notably the absence of unified
standards. One such challenge is semantic representation [24],
aimed at finding suitable ways to represent semantic infor-
mation. Existing studies [25], [26] utilize transmitted content
features for semantic representation, but this approach does not
align with the logic of human language and lacks validation
through interaction with human understanding. To address
these challenges, this paper adopts knowledge graphs [27],
[28] as a means of representing the semantic information of
text data. Knowledge graphs, structured forms of knowledge
with high information density, are pivotal
tools
for extracting semantic information [29]. Comprising entities
and relations, where entities represent real-world objects and
abstract concepts, and relations capture concrete relationships
between entities, knowledge graphs employ triples in the form
of (head, relation, tail) to represent knowledge, e.g., (ba-
nana, a kind of, fruit). Named entity recognition (NER) [30]
and relation extraction (RE) [31] are crucial techniques for

technical

HangzhouZhejiangprovincial capitalZJUlocated inWest LakesightHangzhou Asian Gameshost placeChu Kochenformer principalhometown1890.3.7born in2023.9.23opening day12.204 millionpermanent residentssubtropical monsoon climateclimateShanghaiadjoining105500km²area3

Fig. 2. The process of extracting semantic triples from text data.

the original knowledge graph based on the probability graph
shared with the BS.

A. Probability Graph Model

The semantic information within a knowledge graph is
conventionally expressed as triples in the form (head, relation,
tail). From a given piece of text data, multiple triples can be
extracted, collectively characterizing a knowledge graph. In
scenarios where multiple texts center around similar topics,
certain triples may share common head and tail entities while
differing in specific relations. For example, text data 1 might
contain (Tree, in front of, Car), while text data 2 might have
(Tree, behind, Car). In such cases, combining these triples
could be more informative and efficient. Thus, the represen-
tation could be {Tree, [(in front of, 0.5), (behind, 0.5)], Car},
with the numeric values indicating the frequency of occurrence
of each relation. When confronted with a substantial volume of
text data sharing similar topics, their corresponding knowledge
graphs can be amalgamated into a comprehensive probability
graph using a similar method. In this context, the edges in the
knowledge graph are not strictly determined relational edges
but probabilistic edges, combining the frequency of occurrence
of different relations, as illustrated in Fig. 4.

Before initiating wireless transmission, the BS constructs a
probability graph based on a significant number of historical
samples. Subsequently, the BS transmits this probability graph
to the user as common background knowledge. This process
occurs once, and wireless transmission commences afterward.
During the wireless transmission process, the BS transmits
is

the required text data to the user. The sample dataset

Fig. 3. An illustration of the considered semantic communication system.

The algorithm design is presented in Section III. Simulation
results are analyzed in Section IV. Future research directions
are introduced in Section V. Conclusions are drawn in Section
VI.

II. SYSTEM MODEL AND PROBLEM FORMULATION

Consider a semantic wireless communication system with
one BS and one user, as illustrated in Fig. 3. The BS
and the user share common background knowledge, which
is characterized by the probability graph. The BS needs to
transmit a substantial amount of text data with similar topics to
the user while accounting for limited wireless communication
resources. To achieve this goal,
the BS extracts semantic
information from the raw text data and compresses the se-
mantic information (represented by a knowledge graph) using
a probability graph shared with the user before transmitting it
through the wireless channel. Subsequently, the user recovers

Bruce Lee (November 27, 1940 -July 20, 1973), whose real name was Lee Chun-Fan, was born in San Francisco, California, USA…Bruce Lee was a pioneer of change in the world of martial arts, a pioneer of kung fu films, and the founder of Jeet Kune Do. His films in Hong Kong broke many records, including “TheWay ofThe Dragon”, which broke Asian box office records…Bruce Lee's wife, Linda Emery, a white Irish-American girl who was his classmate at the University of Washington, gave birth to a son on February 1, 1965, whom Bruce Lee named Brandon Lee…On April 19, 1969, Bruce Lee's daughter Shannon Leewas born…In 2008, she was the producer of the TV series “The Legend of Bruce Lee”.born inbirthplacestar inwifegraduation institutionfather ofproducerBruce Lee 1940/11/27born inSan FranciscobirthplaceLinda EmerywifeThe Way of The Dragonstar inUniversity of Washingtongraduation institutiongraduation institutionBrandon Leefather ofShannon Lee mother ofThe Legend of Bruce LeeproducerSemantic information extractionBase stationDownlink transmissionShared probability graphUserSemantic information recoveryOriginal knowledge graphCompressed dataShared probability graphRecovered knowledge graph4

Fig. 4.
communication system.

Illustration of the probability graph considered in the semantic

formulated as

T = {T1, T2, · · · , Tn, · · · , TN } ,

(1)

where N represents the total number of sample data, Tn
denotes the n-th sample data, and T denotes the sample
dataset.

The knowledge graph extracted from each sample data Tn

is represented by

Fig. 5. An illustration of the information compression based on the probability
graph.

Gn = (cid:8)ε1

n, ε2

n, · · · , εm

n , · · · , εM
n

(cid:9) ,

(2)

where εm
M denotes the total number of triples. The triple εm
expressed as

n denotes the m-th triple in knowledge graph Gn, and
n can be

n = (hm
εm

n , rm

n , tm

n ) ,

(3)

n represents the head entity of triple εm

n , and rm

n , tm
n represents
n represents the relation

where hm
the tail entity of triple εm
n and tm
between hm
n .

If no prior information is available, the probability that the

triple (cid:0)hs, ri

s, ts

(cid:1) holds can be written as
num (cid:0)N i
i=1 num (N i
s )

(cid:1) =

s, ts

(cid:80)I

p (cid:0)hs, ri

(cid:1)

s

,

(6)

where num (cid:0)N i
the triple (cid:0)hs, ri
probability of the triple (cid:0)hk, ri

(cid:1) is the number of elements in the set N i
s
s, ts

s . If
(cid:1) is known to be true, then the conditional

(cid:1) can be expressed as

k, tk

The probability graph shared by the BS and the user can be

represented by

p (cid:2)(cid:0)hk, ri

k, tk

(cid:1) | (cid:0)hs, ri

s, ts

(cid:1)(cid:3) =

(cid:1)

num (cid:0)N i
(cid:104)
N i

s ∩

k ∩ N i
s
(cid:16)(cid:83)I
i=1 N i
k

num

(cid:17)(cid:105) ,

G = {δ1, δ2, · · · , δs, · · · , δS} ,

(4)

where δs is the quadruple with relational probability, and S
is the total number of quadruples. Specifically, δs can be
calculated as

s, N i
s

s , N I
s

s, N 1
s

(cid:1)(cid:3) , ts

(cid:1) , · · · , (cid:0)ri

(cid:1) , · · · , (cid:0)rI

δs = (cid:8)hs, (cid:2)(cid:0)r1

(cid:9) ,
(5)
where hs is the head entity of quadruple δs, ts is the tail entity
of quadruple δs, ri
s is the i-th relation between hs and ts, I is
the total number of different relations between hs and ts, and
(cid:1) holds.
N i
For instance, if (cid:0)hs, ri
(cid:1) holds in samples T1, T4, and T7,
then N i

s is the set of samples in which the triple (cid:0)hs, ri

s = {1, 4, 7}.

s, ts

s, ts

Building upon equations (4) and (5), the construction of the
probability graph shared by the BS and the user is successfully
completed.

B. Probability Graph-enabled Information Compression

Once the set of quadruples has been obtained, it is possi-
ble to calculate the multidimensional conditional probability
distribution. The methodology will be elaborated upon in the
following.

s is the intersection of set N i

k ∩ N i
k is the union of set N 1

where N i
(cid:83)I
i=1 N i
Using a similar approach, it is appropriate to derive the mul-
(cid:1)
k, tk

tidimensional conditional probability of the triple (cid:0)hk, ri
given that N triples are known to be true:

k and set N i

k to N I
k .

(7)
s , and

p (cid:2)(cid:0)hk, ri

k, tk

(cid:1) | CN

(cid:3) =

num (cid:2)N i
(cid:104)
(∩N ⊂CN N ) ∩

k ∩ (∩N ⊂CN N )(cid:3)
i=1 N i
k

(cid:16)(cid:83)I

num

(cid:17)(cid:105) ,

(8)
where CN is a set of conditions that indicates the truth of N
triples, and ∩N ⊂CN N denotes the intersection of all sample
sets that satisfy the condition set CN .

When transmitting the knowledge graph that corresponds
to a specific text data, the multidimensional conditional prob-
ability distribution described above can be used to remove
semantic relations for the purpose of information compression,
as depicted in Fig. 5. The compression process can be achieved
using the following scheme.

Prior to transmitting the text data, the BS first applies natural
language processing techniques to extract the corresponding
knowledge graph denoted as G, which is expressed as

G = {ε1, ε2, · · · , εj, · · · , εJ } ,

(9)

TreeCarPedestrianSidewalkHatTree-Sidewalkoutsideinside0.30.7Hat-Pedestrianon the handon the head0.20.8Pedestrian-Caron the left sideon the right side0.40.6Tree-Carin front ofbehind0.50.5TreePedestrianCarHatSidewalkoutsidein front ofon the right sideon the handAfter compression based ontheprobabilitygraphTreePedestrianCarHatSidewalkin front ofon the hand5

For every εa in G1, we need to compute its conditional
in O1. Assume that εa
probability given each triple ϵb
corresponds to δa = (cid:0)ha, ri
(cid:1) in the shared probability
a, ta
graph G. The conditional probability can be represented as
p (cid:2)(cid:0)ha, ri
a|b for sim-
plicity. Consequently, we can construct a probability matrix
consisting of one-dimensional conditional probabilities1 for
(cid:0)ha, ri

(cid:3), which can be denoted by p1

(cid:1) as follows:

(cid:1) | ϵb

a, ta

a, ta

P 1
δa

=














p1
p1
p1
p1
. . .
. . .
1|1
2|1
i|1
I|1
p1
p1
p1
p1
. . .
. . .
1|2
2|2
i|2
I|2
...
...
...
...
. . .
. . .
p1
p1
p1
p1
. . .
. . .
1|b
2|b
i|b
I|b
...
...
...
...
. . .
. . .
i|B . . . p1
2|B . . . p1
1|B p1
p1

I|B














,

(14)

where I is the total number of different relations between ha
and ta in G, and B is the total number of elements in O1.
In the probability matrix P 1
, we begin with the first row and
δa
examine whether p1
i|b is the largest element within that row. If
it is indeed the largest, we take note of the column number and
exclude the relation ri
a when transmitting the corresponding
triple. However, if p1
i|b is not the largest element in any of
the rows, it indicates that the corresponding relation cannot
be omitted during transmission.

We repeat the aforementioned procedure for every triple in
G1, aiming to identify the triples that can be omitted. This
constitutes the first cycle in the second round. In the second
cycle, there will be fewer remaining triples that have not been
omitted. We create a new G1 using these unomitted triples and
form a new O1 for the newly omitted triples. We continue this
process until no new triples can be omitted, iterating through
multiple cycles if necessary.

In the third round, we incorporate two-dimensional condi-
tional probabilities as prior information. We derive the corre-
sponding G2 and O2 based on the previous round’s results.
Subsequently, we calculate a three-dimensional probability
matrix, denoted by P 2, which comprises two-dimensional
conditional probabilities.

This iterative process continues for subsequent rounds,
where each round utilizes conditional probabilities with one
additional dimension.

The comparison process remains largely unchanged for each
round and does not vary significantly. Therefore, it is not
reiterated here. However, it is important to note that as the
rounds progress, deeper comparisons require increased compu-
tational resources. Furthermore, conducting additional rounds
of comparison does not necessarily guarantee proportionate
benefits. Thus, the number of rounds to be compared can be
determined based on the specific communication needs and
available computational resources.

Once the semantic information compression is performed
by the BS, it transmits the conditions of each information
compression to the user, along with the compressed triples.
These compression conditions are represented as very short bit

Fig. 6. The flowchart of the comparison process.

where εj is the jth triple in G, and J is the total number of
triples in G. Specifically, the triple εj can be written in the
following form:

εj = (hj, rj, tj) .

(10)

Next, the knowledge graph G is compared with the shared
probability graph G, and the comparison process can be
divided into several rounds.

s, ts

In the initial round, there is no prior information. For any
εj, we need to examine if there exists δs in G where hj = hs
and tj = ts. If such a case is found, we proceed to investigate
whether there exists a relation ri
s within the relation set of δs
that matches rj. If a match is identified, we further determine
(cid:1) is
whether the corresponding relation probability p (cid:0)hs, ri
the highest among the set of relation probabilities denoted by
Ps. It is possible to represent Ps as
(cid:1) , · · · , p (cid:0)hs, ri
Ps = (cid:8)p (cid:0)hs, r1

(cid:1)(cid:9) .
(11)
(cid:1) happens to be the largest among the relation
If p (cid:0)hs, ri
probabilities in set Ps, we can exclude the relation rj from
the triple εj = (hj, rj, tj) during transmission. In this case,
only the head entity and tail entity need to be sent, reducing
the transmitted data volume. However, if there is no δs in G
satisfying hj = hs and tj = ts, or if such a δs exists but
there is no relation ri
s in its relation set that matches rj, then
the entire triple must be transmitted without omission. The
flowchart of the comparison process is shown in Fig. 6.

(cid:1) , · · · , p (cid:0)hs, rI

s , ts

s, ts

s, ts

s, ts

In the second round, one-dimensional conditional probabil-
ities can be employed as prior information. As certain triples
had their semantic relations omitted in the first round, these
triples can serve as conditions for the second round’s con-
ditional probability search. The second round of comparison
follows a similar process as the first round. We can denote the
set of triples that were not omitted in the first round and do
not necessarily require full transmission as

G1 = {ε1, ε2, · · · , εa, · · · , εA} .

(12)

The triples that can be inferred in the probability graph can
be omitted to save the communication burden. The set of of
omitted triples can be represented by

O1 = {ϵ1, ϵ2, · · · , ϵb, · · · , ϵB} .

(13)

1In the subsequent rounds,

they will be multi-dimensional conditional

probabilities.

StartLoad 𝜀𝑗and 𝔾Does δ𝑠∈𝔾exist such that ℎ𝑗=ℎ𝑠 and 𝑡𝑗=𝑡𝑠?Does 𝑟𝑠𝑖∈δ𝑠exist such that 𝑟𝑗=𝑟𝑠𝑖?Is 𝑝ℎ𝑠,𝑟𝑠𝑖,𝑡𝑠the highest in 𝑃𝑠?Omit 𝑟𝑗EndTransmit 𝜀𝑗in its entiretyPut 𝜀𝑗in the next roundYesYesYesNoNoNostreams, which are insignificant compared to the size of the
original data to be transmitted. Upon receiving the compressed
information, the user can reconstruct the omitted information
by leveraging the compressed conditions in conjunction with
the common background knowledge G.

C. Joint Communication and Computation Resource Alloca-
tion

The above reasoning process enables the exclusion of
certain portions of the knowledge graph from transmission,
thereby reducing communication delays. However, compress-
ing information through reasoning requires additional time
and energy for computation. To achieve improved results and
minimize the overall system energy consumption during the
communication process,
to consider the joint
allocation of communication and computation resources.

is crucial

it

The total latency of the semantic communication system
comprises two main components: the communication latency,
denoted by t1, and the computation latency, denoted by t2.
Note that the latency for processing and transmitting a text data
message is constrained by a limit, denoted by T . Therefore, in
order to meet the latency limit, the total process must adhere
to the condition that the sum of communication latency and
computation latency is less than or equal to T , i.e., t1+t2 ≤ T .
This ensures that the overall latency of the system remains
within the specified limit.

The communication time delay t1 is calculated as follows.
The transmission rate between the BS and the user can be
expressed as

c = B log2

1 +

,

(15)

(cid:18)

(cid:19)

ph
σ2

where B is the bandwidth of the system, p is the transmit
power of the BS, h is the channel gain between the BS and
the user, and σ2 is the noise power.

If the head entity, relation, and tail entity in each triple are
all encoded with the same number of bits R, then the total
number of bits of semantic information D in the text data can
be calculated as

size (D) = R (3M − E) ,

(16)

where M is the total number of triples in D, and E is the
number of triples in which the relation can be fully omitted.
Consequently, the communication latency can be written as

t1 =

size (D)
c

=

R (3M − E)
(cid:16)
1 + ph
σ2

B log2

(cid:17) .

(17)

The computation time delay t2 is calculated as follows.
The computational load of the proposed knowledge graph
semantic information compression system is directly related
to the number of comparisons in the compression process.
To simplify the analysis, we will only consider the first and
second rounds of comparison as described in the previous sub-
section. As it is infeasible to pre-determine the computational
resources required to omit E relations for a specific text data,
we employ a statistical approach to calculate the ratio of the
number of triples that can be omitted in each round to the total

6

number of remaining triples. Based on this ratio, we estimate
the computational resources required to omit E relations in a
statistical sense.

The ratio of the number of triples that can be omitted more
in each round to the total number of triples before this round
can be expressed as

Q = {q1, q2, · · · , qn, · · · , qN } ,

(18)

where q1 is the ratio of the number of triples that can be
omitted more in the first round to the total number of all triples,
q2 is the ratio of the number of triples that can be omitted more
in the first cycle of the second round to the number of triples
whose relation is not omitted, and qn is the ratio of the number
of triples that can be omitted more in the (n − 1)-th cycle of
the second round to the number of triples whose relation is
not omitted before this cycle.

We can express the number of semantic relations that can be
omitted in each round or cycle using a recursive formulation:






E1 = M q1,
E2 = (M − E1) q2,
E3 = (M − E1 − E2) q3,
...
EN = (M − E1 − E2 − · · · − EN −1) qN ,

,

(19)

where M is the total number of triples, and EN is the number
of relations which can be omitted in the (N − 1)-th cycle of
the second round.

Based on (19), the computation load to omit E relations in

M triples can be written as

l (E) =






, 0 ≤ E ≤ E1,
+ (E−E1)E1
q2
(cid:16) E1
− E1
q1

E
q1
E1
q1
E1
q1
q3
E1 + E2 < E ≤ E1 + E2 + E3,
...

, E1 < E ≤ E1 + E2,
(cid:17)
E1 + (E−E2−E1)E2

+

,

(cid:17)

+

E1 +

(cid:16) E1
q1

(cid:16) E1
E1
− E1
q1
q1
· · · + (E−EN −1−···−E1)EN −1
,
n=1 En < E ≤ (cid:80)N
(cid:80)N −1
n=1 En.

qN

.

(cid:17)

E2+

− E1 − E2

(20)
The piecewise function (20) of the computation load is
derived from the number of comparisons required to omit E
relations. We calculate the average cost of one single omission
at different round. The derivation process for l (E) is shown
in Fig. 7.

It can be observed that l (E) is an increasing segmented
function, where each segment is a linear function with respect
to E. Consequently, the computation latency can be written as

t2 =

τ1l (E)
f

,

(21)

where τ1 is a constant coefficient, and f is the computation
capacity.

Based on the transmission time model, the communication

energy consumption can be written as

e1 = t1p.

(22)

7

Fig. 7.

Illustration of the insight of l (E).

Besides, the computation energy consumption can be written
as

e2 = τ1τ2l (E) f 2,

(23)

where τ1 and τ2 are constant coefficients.

Based on the considered model, our aim is to minimize
the total energy consumption of the semantic communication
system, which can be formulated as

min
p,E

s.t.

e1 + e2,

(24)

R(3M − E)
(cid:16)
1 + ph
σ2

B log2

(cid:17) +

τ1l (E)
f

0 ≤ p ≤ pmax,
0 ≤ E ≤ M, E ∈ N.

≤ T,

(24a)

(24b)

(24c)

Constraint (24a) limits the total delay of communication
and computation, while constraint (24b) represents that the
transmit power p of the BS does not exceed a maximum
limit pmax. Constraint (24c) limits the total number of omitted
relations E to a non-negative integer that does not exceed the
total number of triples M . The objective of the optimization
problem is to minimize the total energy consumption of the
semantic communication system.

III. ALGORITHM DESIGN

In problem (24), two variables need to be optimized: the
transmit power p of the BS and the total number of triples E
that omit semantic relations. Increasing the transmit power p
of the BS can reduce communication delay through increasing
the transmission rate.However, the increasing of power does

not necessarily lead to reduced energy consumption in com-
munication. Conversely, increasing the total number of triples
E that omit semantic relations can reduce communication
delays, as fewer bits need to be transmitted. This can result
in lower energy consumption in communication. However,
it also increases computation delays, as more processing
resource is required to compress the semantic information. The
computation may consume more energy, offsetting the gains
made in communication.

To minimize the total energy consumption of the system
while satisfying all constraints, it is crucial to carefully select
suitable values for the BS transmit power p and the total
number of triples E that omit semantic relations. A balance
needs to be struck, considering the specific requirements,
constraints, and trade-offs involved in communication and
computation energy consumption.

A. Optimal Transmit Power

To facilitate the analysis of the problem, we initially assume
a fixed total number E of triples that omit semantic relations
and examine the influence of the BS transmit power p on the
overall system. We simplify constraint (24a) and separate the
transmit power p of the BS to derive

(cid:32)
2

p ≥

R(3M −E)
(cid:18)
τ1l(E)
f

T −

B

(cid:19)

(cid:33)

− 1

h
σ2 .

(25)

According to the right side of formula (25), it can be observed
that when T − τ1l(E)

f > 0, that is

l (E) <

T · f
τ1

,

(26)

……𝑀triples………𝐸1=𝑀𝑞1relations omittedFirst round………𝐸2=𝑀−𝐸1𝑞2 relations omittedSecond round first cycleRequire𝑀=𝐸1𝑞1comparisonsRequire𝐸1𝑞1−𝐸1𝐸1comparisonsSecond round second cycle…………𝐸3=𝑀−𝐸1−𝐸2𝑞3Every omission costs 𝐸1/𝑞1𝐸1=1𝑞1comparisons averagelyEvery omission costs 𝐸1𝑞1−𝐸1𝐸1𝐸2=𝐸1𝑞2comparisons averagelyRequire𝐸1𝑞1−𝐸1−𝐸2𝐸2comparisonsEvery omission costs 𝐸1𝑞1−𝐸1−𝐸2𝐸2𝐸3=𝐸2𝑞3comparisons averagely……Second round 𝑵−𝟏thcycle…………𝐸1+𝐸2+⋯+𝐸𝑁−1+𝐸𝑁 relations omittedthe right side of equation (25)

When

(cid:32)
2

R(3M −E)
(cid:18)
τ1l(E)
f

T −

B

(cid:19)

(cid:33)

− 1

h
σ2 > 0.

(cid:32)
2

R(3M −E)
(cid:18)
τ1l(E)
f

T −

B

(cid:19)

(cid:33)

− 1

h
σ2 ≤ pmax,

we have s(x) > 0 when x > 0. Therefore, when x > 0,
h′(x) > 0, the function h(x) increases monotonically on the
domain x > 0.

It can be obtained that when E is fixed,

the objective

function

f (p) =

R(3M − E)p
(cid:16)
1 + ph
σ2

B log2

(cid:17) + τ1τ2l (E) f 2

(37)

(27)

(28)

8

we can combine constraint (24a) with constraint (24b) to get

(cid:32)
2

R(3M −E)
(cid:18)
τ1l(E)
f

T −

B

(cid:19)

(cid:33)

− 1

h
σ2 ≤ p ≤ pmax.

(29)

Expanding the objective function of the optimization prob-

lem, we can further obtain

F (p, E) = e1 + e2 =

R(3M − E)p
(cid:16)
1 + ph
σ2

B log2

(cid:17) + τ1τ2l (E) f 2. (30)

When E is fixed, the objective function becomes a function
with respect to p. We denote this function by f (p), and we
will analyze its monotonicity within the domain of definition
(28) as follows.

When E is fixed,

the second term of f (p), which is
τ1τ2l (E) f 2, is a constant. Therefore, we only need to analyze
the monotonicity of the first term. To simplify this analysis,
term of f (p) by the constant
we can multiply the first
σ2·R(3M −E) . Let’s denote this new expression as g (p), and it
can be written as

h·B

increases monotonically when p > 0.

In summary, when the total number of triples that omit
semantic relations E is fixed, a smaller transmit power p
for the BS leads to better results, provided that the other
constraints are satisfied. The optimal transmit power for the
BS, satisfying constraints (26) and (28), is denoted as

(cid:32)

poptimized =

B

2

R(3M −E)
(cid:18)
τ1l(E)
f

T −

(cid:19)

(cid:33)

− 1

h
σ2 .

(38)

If constraint (26) cannot be satisfied, it indicates that the
value of E is too large, and the computation delay alone
exceeds the total latency limit. Therefore, this value of E
is undesirable. Additionally, since l(E) is a monotonically
increasing function, all values larger than this undesirable E
are also undesirable. On the other hand, if constraint (26) is
satisfied but constraint (28) cannot be satisfied, it means that
the maximum transmit power of the BS becomes the limiting
factor. In this case, the optimized transmit power poptimized is
equal to the maximum transmit power pmax.

g (p) =

ph
σ2
1 + ph
σ2

(cid:16)

(cid:17) .

log2

(31)

B. Algorithm Analysis

It is evident that the monotonicity of g (p) is the same as that
of f (p). Let’s denote ph
σ2 as x and rewrite the new function as

h (x) =

x
log2 (1 + x)

.

(32)

It is straightforward to observe that the monotonicity of the
function f (p) for p > 0 is equivalent to the monotonicity of
the function h(x) for x > 0.

Now, we analyze the monotonicity of the function h (x).
First, taking the derivative of h (x) with respect to x, we have
log2(1 + x) −

x
(ln 2)(1+x)

.

(33)

h′(x) =

[log2(1 + x)]2

To analyze the monotonicity of h(x), we need to find the sign
of its derivative. Notice that the denominator of h′(x) is always
positive when x > 0, so we only need to analyze the sign of
its numerator.

Let

s(x) = log2(1 + x) −

x
(ln 2)(1 + x)

.

Then, the derivative of s (x) with respect to x is

s′(x) =

x
(ln 2)(1 + x)2 .

(34)

(35)

Since x > 0, s′(x) > 0, so s(x) increases monotonically on
x > 0. Due to the fact that

s(0) = log2(1 + 0) −

0
(ln 2)(1 + 0)

= 0,

(36)

It follows that for each fixed value of E, we can determine
the optimal value of the corresponding BS transmit power
p. Given that the total number of triples that omit semantic
relations, E, is a natural number and has an upper bound, it is
advisable to design the algorithm based on traversing different
values of E. The specific flow of the algorithm is outlined in
Algorithm 1.

Algorithm 1 Joint Communication and Computation Opti-
mization Algorithm for Text Semantic Compression
1: Initialize poptimized = pmax, Eoptimized = 0, and objmin =

inf.

if Constraint (26) is not satisfied then

end if
if Constraint (28) is not satisfied then

p = pmax
obj = F (p, E)

Break

2: for E = 0 : M do
3:
4:
5:
6:
7:
8:
9:
10:
11:
12:
13:
14:
end if
15:
16: end for

else

end if
if obj < objmin then

Obtain p according to equation (38)
obj = F (p, E)

(objmin, poptimized, Eoptimized) = (obj, p, E)

According to Algorithm 1, the complexity of solving prob-
lem (24) lies in the total number of triples to be transmitted.
The total complexity of solving the joint communication and
computation optimization problem is O(M ), where M is the
total number of triples.

To verify the correctness of the algorithm design, we utilized
the official nonlinear programming solver fmincon() pro-
vided by MATLAB to solve this optimization problem. The re-
sults obtained from our algorithm were found to be consistent
with the results obtained using fmincon(). Moreover, our
algorithm demonstrated significantly faster speed compared to
using fmincon(), thereby demonstrating the correctness and
efficiency of our proposed algorithm.

IV. SIMULATION RESULTS
In the simulations, the maximum transmit power of the BS
is 30 dBm. Unless specified otherwise, we set the bandwidth
of the BS B = 10 MHz, total number of triples M = 100,
and total latency limit T = 1 ms. The values of most of the
simulation parameters are set based on [22]. The main system
parameters are summarized in Table I.

TABLE I
MAIN SYSTEM PARAMETERS

Parameter

Bandwidth of the BS B
Maximum transmit power of the BS pmax
Path loss h
Total number of triples M
Total latency limit T
Computation capacity f

Value

10 MHz
30 dBm
10−9
100
1 ms
1 GHz

To evaluate the performance of the proposed joint com-
munication and computation optimization system based on
probability graph, labeled as ‘JCCPG’, we designed two base-
line algorithms for comparison. ‘Traditional’ involves directly
triples with the same total delay, without
transmitting all
considering the maximum transmission power limit. ‘Simpli-
fied JCCPG’ optimizes the allocation of communication and
computation resources based solely on the results of the first
round of comparison.

Fig. 8 illustrates the variation trend of the total communica-
tion and computation energy consumption in the system with
respect to the total number of transmitted triples. As the total
number of transmitted triples increases, the energy consump-
tion of all algorithms in the system also increases due to the
increased transmission and computation requirements. How-
ever, ‘JCCPG’ and ‘Simplified JCCPG’ exhibit a significantly
smaller growth rate compared to ‘Traditional’. This indicates
the robustness of the proposed algorithm. Furthermore, the
total system energy consumption of ‘JCCPG’ is consistently
lower than that of both ‘Traditional’ and ‘Simplified JCCPG’.
This advantage becomes more pronounced as the total number
of transmitted triples increases. These findings highlight the
significant advantage of the proposed algorithm in transmitting
the large-scale data.

To gain a comprehensive understanding of the proposed ‘JC-
CPG’ system, the energy consumption of ‘JCCPG’ for com-
munication and computation is illustrated in Fig. 9. The figure

9

Fig. 8. Total communication and computation energy vs. total number of
transmitted triples.

Fig. 9. Communication and computation energy consumption of ‘JCCPG’
vs. total number of transmitted triples.

clearly demonstrates that the energy consumed by computation
is significantly lower than that consumed by communication.
This observation somehow suggests that computation exhibits
greater energy efficiency compared to communication. More-
over, the future holds promise for considerable advancements
in the computation capacity of terminal devices, accompanied
by progressively more energy-efficient CPUs. Consequently,
the integration of communication and computation is poised
to become a prominent trend in the future as it possesses the
potential to overcome the limitations of traditional communi-
cation methods.

Fig. 10 illustrates the relationship between the total com-
munication and computation energy consumption and the BS
bandwidth. As the bandwidth of the BS increases, the total
system energy consumption of all algorithms decreases. This
is because a larger bandwidth provides more communication

020406080100120M00.511.522.533.54Totalcommunicationandcomputationenergy10-5JCCPGTraditionalSimplified JCCPG020406080100120M00.20.40.60.811.21.41.61.82Energy consumption10-5TotalCommu.Comp.10

Fig. 10. Total communication and computation energy vs. bandwidth of the
system.

Fig. 11. Total communication and computation energy vs. total latency limit.

resources, resulting in shorter communication delay between
the BS and the user. In ‘JCCPG’, the reduced communi-
cation latency allows for longer computation latency, ulti-
mately reducing the overall energy consumption of the system.
When the bandwidth of the BS is large, the total energy
consumption of the three algorithms tends to be similar. This
is because when communication resources are abundant, the
transmit power of the BS can be reduced. As a result, the
communication energy consumption of all algorithms is small,
and the proportion of computation becomes a relatively small
factor. Therefore, the total energy consumption of the three
algorithms does not differ significantly. However, when the
bandwidth of the BS is small, indicating a poor communica-
tion environment, the proposed algorithm leverages the joint
optimization of communication and computation, leading to a
significant reduction in the total energy consumption of the
system.

Fig. 11 depicts the impact of the total delay constraint on
the total communication and computation energy consumption
of the system. When the total delay limit T is small, ‘JCCPG’
exhibits a significant advantage over ‘Traditional’. This is
because in order to achieve the same total delay as ‘JC-
CPG’, ‘Traditional’ needs to substantially increase the transmit
power of the BS, resulting in higher energy consumption for
communication. In contrast, ‘JCCPG’ reduces the amount of
information to be transmitted through computation, thereby
reducing the system’s reliance on high transmit power and
ultimately decreasing the total energy consumption. As the
total delay limit T increases to a certain value,
the total
system energy consumption of the three algorithms remains
unchanged. This is because the total delay limit T no longer
acts as a constraint that impedes the reduction of total energy
consumption in the system. At this point, the algorithms have
optimized their communication and computation resources to
achieve the minimum energy consumption within the given

delay constraint.

In conclusion, the simulation results demonstrate that the
proposed communication and computation joint optimiza-
tion system, ‘JCCPG’, achieves lower total communication
and computation energy consumption compared to ‘Tradi-
tional’ and ‘Simplified JCCPG’. Particularly in scenarios with
poor communication conditions or when dealing with larger
amounts of data to be transmitted,
the proposed scheme
exhibits significant advantages. These findings highlight the
effectiveness of the proposed approach in reducing energy
consumption and optimizing resource allocation in semantic
communication systems.

V. FUTURE WORK

In the future, the model considered in this paper can be
further developed. This section outlines some directions that
could potentially enhance the model’s capabilities.

Firstly, there’s a prospect for dynamic refinement of the
shared probability graph between the BS and the user during
the communication process. Post
transmission of semantic
information for a given text data, the user could reconstruct an
identical knowledge graph to the one possessed by the BS. By
treating this knowledge graph as a new sample, both the BS
and the user can collaboratively update the shared probability
graph. The synchronicity in their approach ensures that the
updated probability graph remains consistent. Consequently,
there’s no need for the BS to transmit the updated graph
to the user after each update. The shared probability graph
thus retains its single transmission requirement prior to formal
text data transmission. Additionally, the notion of “forgetting”
can be integrated into this update process. Essentially, more
recent messages carry greater significance. This insight can
be operationalized by assigning higher weight
to recently
transmitted knowledge graphs during probability graph up-
dates. This approach ensures gradual retention of more recent,
impactful information, aligning with the concept of age of

68101214161820Bandwidth(MHz)01234567Totalcommunicationandcomputationenergy10-5JCCPGTraditionalSimplified JCCPG10-310-210-1Total time limit(S)1.41.61.822.22.42.62.833.23.4Total communication and computation energy10-5JCCPGTraditionalSimplified JCCPGinformation (AoI) [37], [38], a vibrant
communication research.

theme in wireless

Secondly, the current model doesn’t harness the semantic
correlations between distinct triples while calculating the mul-
tidimensional conditional probability. In practice, triples ex-
hibit varying degrees of correlation, and leveraging the seman-
tic information within the triples can enhance the efficiency
of multidimensional conditional probability calculations. One
possible way is to use existing large language models (LLMs)
such as BERT [39], GPT [40], etc., to embed triples. This
transforms the triples into vectors, with cosine similarity
serving as the correlation coefficient. LLMs are extensively
trained on copious amounts of high-quality data, showcasing
their remarkable proficiency in processing textual information.
Integrating LLMs into the domain of semantic communication
stands as a potentially challenging yet promising research
direction.

Thirdly, the present wireless communication model is a
point-to-point configuration. Future endeavors could embrace
more complex scenarios, like single-base station multi-user or
multi-base station multi-user environments. This would entail
devising optimization problems that better mirror real-world
settings and exploring solutions in conjunction with commu-
nication techniques such as non-orthogonal multiple access
(NOMA) [41] and rate splitting multiple access (RSMA).
These advancements would align more closely with actual
communication dynamics and open up new dimensions of
research.

VI. CONCLUSION

In this paper, we have proposed a novel probability graph-
based semantic information compression system designed
for scenarios where the BS and the user share common
background knowledge. By leveraging probability graph, we
established a framework to represent and compress shared
knowledge between the communicating parties. The proposed
system operates by extracting semantic information from spe-
cific text data at the BS, which is then transformed into a
knowledge graph. Using the shared probability graph, the BS
selectively omits certain relation information during transmis-
sion. The compressed semantic data, along with the shared
probability graph and predefined rules, enable the user to
automatically restore the missing information upon reception.
This approach effectively reduces communication resource
consumption while introducing additional computational re-
source requirements. Considering the inherent limitations of
wireless resources, we further addressed the challenge of
joint communication and computation resource allocation. We
formulated an optimization problem aiming at minimizing the
total communication and computation energy consumption of
the network, while satisfying constraints related to latency,
transmit power, and semantic requirements. To solve this
problem, we employed an efficient algorithm that demonstrates
both correctness and efficiency. Simulation results validate the
effectiveness of the proposed system. Specifically, the total
communication and computation energy consumption of our
system outperforms that of baseline algorithms in various

11

scenarios. This highlights the significant advantages of our
approach, particularly in scenarios with poor communication
conditions or larger data volumes to be transmitted.

In conclusion, our work presented a comprehensive frame-
work for probability graph-based semantic information com-
pression, addressing resource optimization challenges in se-
mantic communication systems. The proposed system show-
cases promising results, indicating its potential for improving
communication efficiency, especially in challenging scenarios
characterized by limited resources and substantial data vol-
umes.

REFERENCES

[1] C. E. Shannon, “A mathematical theory of communication,” The Bell

system technical journal, vol. 27, no. 3, pp. 379–423, 1948.

[2] E. G. Larsson, O. Edfors, F. Tufvesson, and T. L. Marzetta, “Massive
mimo for next generation wireless systems,” IEEE communications
magazine, vol. 52, no. 2, pp. 186–195, 2014.

[3] C. Huang, A. Zappone, G. C. Alexandropoulos, M. Debbah, and
C. Yuen, “Reconfigurable intelligent surfaces for energy efficiency in
wireless communication,” IEEE Transactions on Wireless Communica-
tions, vol. 18, no. 8, pp. 4157–4170, 2019.

[4] W. Xu, Z. Yang, D. W. K. Ng, M. Levorato, Y. C. Eldar, and M. Debbah,
“Edge learning for b5g networks with distributed signal processing:
Semantic communication, edge computing, and wireless sensing,” IEEE
journal of selected topics in signal processing, vol. 17, no. 1, pp. 9–39,
2023.

[5] Z. Chen, Z. Zhang, and Z. Yang, “Big ai models for 6g wireless
networks: Opportunities, challenges, and research directions,” arXiv
preprint arXiv:2308.06250, 2023.

[6] L. Lin, Z. Zhao, Z. Yang, and Z. Zhang, “Joint communication and
learning design of differential privacy for federated learning over multi-
cell networks,” in 2023 IEEE Int. Conf. Commun. (ICC Workshops),
May. 2023, pp. 770–775.

[7] D. G¨und¨uz, Z. Qin, I. E. Aguerri, H. S. Dhillon, Z. Yang, A. Yener, K. K.
Wong, and C.-B. Chae, “Beyond transmitting bits: Context, semantics,
and task-oriented communications,” IEEE Journal on Selected Areas in
Communications, vol. 41, no. 1, pp. 5–41, 2022.

[8] W. Weaver, “Recent contributions to the mathematical theory of com-
munication,” ETC: a review of general semantics, pp. 261–281, 1953.
[9] C. Chaccour, W. Saad, M. Debbah, Z. Han, and H. V. Poor, “Less data,
more knowledge: Building next generation semantic communication
networks,” arXiv preprint arXiv:2211.14343, 2022.

[10] Z. Zhao, Z. Yang, Y. Hu, L. Lin, and Z. Zhang, “Semantic information
extraction for text data with probability graph,” in 2023 IEEE/CIC Int.
Conf. Commun. China (ICCC Workshops), Aug. 2023.

[11] Z. Weng, Z. Qin, and G. Y. Li, “Semantic communications for speech
signals,” in ICC 2021-IEEE International Conference on Communica-
tions. Montreal, QC, Canada: IEEE, 2021.

[12] Z. Zhao, Z. Yang, Q.-V. Pham, Q. Yang, and Z. Zhang, “Semantic
communication with probability graph: A joint communication and
computation design,” in 2023 IEEE 98th Veh. Tech. Conf. (VTC2023-
Fall), Oct. 2023.

[13] Q. Lan, D. Wen, Z. Zhang, Q. Zeng, X. Chen, P. Popovski, and
K. Huang, “What is semantic communication? a view on conveying
meaning in the era of machine intelligence,” Journal of Communications
and Information Networks, vol. 6, no. 4, pp. 336–371, 2021.

[14] Z. Qin, X. Tao, J. Lu, W. Tong, and G. Y. Li, “Semantic communications:
Principles and challenges,” arXiv preprint arXiv:2201.01389, 2021.
[15] B. G¨uler, A. Yener, and A. Swami, “The semantic communication
game,” IEEE Transactions on Cognitive Communications and Network-
ing, vol. 4, no. 4, pp. 787–802, 2018.

[16] H. Xie, Z. Qin, G. Y. Li, and B.-H. Juang, “Deep learning enabled
semantic communication systems,” IEEE Transactions on Signal Pro-
cessing, vol. 69, pp. 2663–2675, 2021.

[17] Z. Weng and Z. Qin, “Semantic communication systems for speech
transmission,” IEEE Journal on Selected Areas in Communications,
vol. 39, no. 8, pp. 2434–2444, 2021.

[18] H. Tong, Z. Yang, S. Wang, Y. Hu, W. Saad, and C. Yin, “Federated
learning based audio semantic communication over wireless networks,”
in 2021 IEEE Global Communications Conference (GLOBECOM).
IEEE, 2021.

12

[41] Y. Saito, Y. Kishiyama, A. Benjebbour, T. Nakamura, A. Li, and
K. Higuchi, “Non-orthogonal multiple access (noma) for cellular future
radio access,” in 2013 IEEE 77th vehicular technology conference (VTC
Spring).

IEEE, 2013.

[19] H. Xie and Z. Qin, “A lite distributed semantic communication system
for internet of things,” IEEE Journal on Selected Areas in Communica-
tions, vol. 39, no. 1, pp. 142–153, 2020.

[20] T. Han, Q. Yang, Z. Shi, S. He, and Z. Zhang, “Semantic-preserved
communication system for highly efficient speech transmission,” IEEE
Journal on Selected Areas in Communications, vol. 41, no. 1, pp. 245–
259, 2022.

[21] X. Peng, Z. Qin, D. Huang, X. Tao, J. Lu, G. Liu, and C. Pan, “A
robust deep learning enabled semantic communication system for text,”
in GLOBECOM 2022-2022 IEEE Global Communications Conference.
IEEE, 2022, pp. 2704–2709.

[22] Z. Yang, M. Chen, Z. Zhang, and C. Huang, “Energy efficient semantic
communication over wireless networks with rate splitting,” IEEE Journal
on Selected Areas in Communications, vol. 41, no. 5, pp. 1484–1495,
2023.

[23] L. Yan, Z. Qin, R. Zhang, Y. Li, and G. Y. Li, “Resource allocation for
text semantic communications,” IEEE Wireless Communications Letters,
vol. 11, no. 7, pp. 1394–1398, 2022.

[24] T. L. Griffiths and M. Steyvers, “A probabilistic approach to semantic
representation,” in Proceedings of the Twenty-Fourth Annual Conference
of the Cognitive Science Society. Routledge, 2019, pp. 381–386.
[25] F. N. Al-Wesabi, “A hybrid intelligent approach for content authenti-
cation and tampering detection of arabic text transmitted via internet.”
Computers, Materials & Continua, vol. 66, no. 1, 2021.

[26] G. Kordopatis-Zilos, S. Papadopoulos, and I. Kompatsiaris, “Geotagging
text content with language models and feature mining,” Proceedings of
the IEEE, vol. 105, no. 10, pp. 1971–1986, 2017.

[27] S. Ji, S. Pan, E. Cambria, P. Marttinen, and P. S. Yu, “A survey on
knowledge graphs: Representation, acquisition, and applications,” IEEE
Transactions on Neural Networks and Learning Systems, vol. 33, no. 2,
pp. 494–514, 2022.

[28] M. Nickel, K. Murphy, V. Tresp, and E. Gabrilovich, “A review of
relational machine learning for knowledge graphs,” Proceedings of the
IEEE, vol. 104, no. 1, pp. 11–33, 2016.

[29] P. A. Bonatti, S. Decker, A. Polleres, and V. Presutti, “Knowledge
graphs: New directions for knowledge representation on the semantic
web (dagstuhl seminar 18371),” in Dagstuhl reports, vol. 8, no. 9.
Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik, 2019.

[30] J. Li, A. Sun, J. Han, and C. Li, “A survey on deep learning for
named entity recognition,” IEEE Transactions on Knowledge and Data
Engineering, vol. 34, no. 1, pp. 50–70, 2022.

[31] M. Xie, J. Wang, and X. Zhang, “Joint model of triple relation extraction
with label embeddings,” in 2021 International Conference on Asian
Language Processing (IALP), 2021, pp. 105–110.

[32] M. Y. Jaradeh, A. Oelen, K. E. Farfar, M. Prinz, J. D’Souza,
G. Kismih´ok, M. Stocker, and S. Auer, “Open research knowledge
graph: next generation infrastructure for semantic scholarly knowledge,”
in Proceedings of the 10th International Conference on Knowledge
Capture, 2019, pp. 243–246.

[33] M. Atef Mosa, “Predicting semantic categories in text based on knowl-
edge graph combined with machine learning techniques,” Applied Arti-
ficial Intelligence, vol. 35, no. 12, pp. 933–951, 2021.

[34] F. Zhou, Y. Li, X. Zhang, Q. Wu, X. Lei, and R. Q. Hu, “Cognitive
semantic communication systems driven by knowledge graph,” in ICC
2022 - IEEE International Conference on Communications, 2022, pp.
4860–4865.

[35] S. Jiang, Y. Liu, Y. Zhang, P. Luo, K. Cao, J. Xiong, H. Zhao, and
J. Wei, “Reliable semantic communication system enabled by knowledge
graph,” Entropy, vol. 24, no. 6, p. 846, 2022.

[36] L. Hu, Y. Li, H. Zhang, L. Yuan, F. Zhou, and Q. Wu, “Robust semantic
communication driven by knowledge graph,” in 2022 9th International
Conference on Internet of Things: Systems, Management and Security
(IOTSMS), 2022.

[37] R. D. Yates, Y. Sun, D. R. Brown, S. K. Kaul, E. Modiano, and
S. Ulukus, “Age of information: An introduction and survey,” IEEE
Journal on Selected Areas in Communications, vol. 39, no. 5, pp. 1183–
1210, 2021.

[38] A. Kosta, N. Pappas, V. Angelakis et al., “Age of information: A new
concept, metric, and tool,” Foundations and Trends® in Networking,
vol. 12, no. 3, pp. 162–259, 2017.

[39] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pre-training
of deep bidirectional transformers for language understanding,” arXiv
preprint arXiv:1810.04805, 2018.

[40] B. D. Lund and T. Wang, “Chatting about chatgpt: how may ai and gpt
impact academia and libraries?” Library Hi Tech News, vol. 40, no. 3,
pp. 26–29, 2023.

