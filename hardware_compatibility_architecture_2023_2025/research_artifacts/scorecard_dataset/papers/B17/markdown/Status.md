On extremal leaf status and internal status of
trees
Haiyan Guo∗, Bo Zhou†
School of Mathematical Sciences, South China Normal University
Guangzhou 510631, P.R. China
Abstract
For a vertexu of a treeT , the leaf (internal, respectively) status ofu
is the sum of the distances fromu to all leaves (internal vertices, respec-
tively) of T . The minimum (maximum, respectively) leaf status of a tree
T is the minimum (maximum, respectively) leaf statuses of all vertices of
T . The minimum (maximum, respectively) internal status of a treeT is
the minimum (maximum, respectively) internal statuses of all vertices of
T . We give the smallest and largest values for the minimum leaf status,
maximum leaf status, minimum internal status, and maximum internal
status of a tree and characterize the extremal cases. We also discuss these
parameters of a tree with given diameter or maximum degree.
Mathematics Subject Classiﬁcations: 05C12, 05C35
Keywords and phrases: minimum leaf status, maximum leaf status,
minimum internal status, maximum internal status, tree, diameter, maxi-
mum degree
1 Introduction
Let Gbe a connected graph of ordern≥2 with vertex setV(G). For u,v ∈V(G),
the distance between uand vin G, denoted by dG(u,v), is the length of a shortest
path connecting u and v in G. Let ∅̸= A⊆V(G). For u∈V(G), the A-status
of u in G is deﬁned as
sG(u,A) =
∑
v∈A
dG(u,v).
The minimum A-status of G is sA(G) = min {sG(u,A) : u ∈V(G)}, while the
maximum A-status of G is SA(G) = max{sG(u,A) : u∈V(G)}. The A-centroid
(or A-median) of G is deﬁned as {u∈V(G) : sG(u,A) = sA(G)}.
∗E-mail: ghaiyan0705@163.com
†Corresponding author. E-mail: zhoubo@scnu.edu.cn
1
arXiv:2008.00438v1  [cs.DM]  2 Aug 2020

Let sG(u) = sG(u,V (G)) for u ∈ V(G), s(G) = sV (G)(G) and S(G) =
SV (G)(G). Then sG(u) is the status (or transmission) ofuin G[4,8,18], s(G) is the
minimum status of G, and S(G) is the maximum status ofG. Both minimum and
maximum statuses have been studied extensively, and it should be noted that the
minimum (maximum, respectively) status appeared also in its normalized form
divided by n−1 that is called the proximity (remoteness, respectively) of the
graph, see, e.g., [1–3,5,6,9–13,15,17,20].
Let T be a tree. For u∈V(T), denote by NT (u) the set of vertices adjacent
to uin T and the cardinality of NT (u) is the degree of uin T, denoted by δT (u).
A vertex of degree one in a tree is called a leaf and a vertex of degree at least
two in a tree is called an internal vertex. Let L(T) and I(T) be the set of leaves
and the set of internal vertices of T, respectively.
Slater [16] studied structure of the A-centroid of a tree T with ∅̸= A⊆V(T).
For example, it was shown in [16, Theorem 5] that the A-centroid induces a path
in a tree for any subset A. The another related concept is called A-center, which
is deﬁned to be the set {u∈V(T) : eA(u,T)}, where eA(u,T) = max{dT (u,v) :
v ∈A}. It was shown in [16] that L(T)-center and L(T)-centroid have quite
diﬀerent properties. Wang [19] characterized the trees with maximum distance
between the L(T)-centroid and the centroid or the I(T)-centroid, and maximum
distance between the I(T)-centroid and the centroid, respectively. Here for two
subset A and B of vertices of a connected graph G, the distance between A and
B is smallest distance between a vertex from A and a vertex from B in G.
The minimum leaf status (internal status, respectively) of T is deﬁned to be
the minimum L(T)-status (I(T)-status, respectively), denoted by ls(T) (is(T),
respectively). That is,
ls(T) = sL(T)(T) and is(T) = sI(T)(T).
The maximum leaf status (internal status, respectively) of T is deﬁned to be the
maximum L(T)-status ( I(T)-status, respectively), denoted by LS(T) ( IS(T),
respectively). That is,
LS(T) = SL(T)(T) and IS(T) = SI(T)(T).
In this paper, we study the extremal properties of these four parameters of trees.
We give the smallest and largest values for the minimum leaf status, maximum
leaf status, minimum internal status, and maximum internal status of a tree and
characterize the extremal cases. We also discuss these parameters of trees with
given diameter or maximum degree.
We note related work of Dimitrov et al. [7], where, if restricted to trees, they
studied the extremal properties of ∑
u,v∈I(T) dT (u,v) and ∑
u,v∈V (T)
{u,v}∩L(T)̸=∅
dT (u,v) for
trees T.
2

2 Preliminaries
The diameter of a connected graph G is the maximum distance between two
vertices. Denote by Sn and Pn the star and the path of order n, respectively.
A double star is a tree with diameter 3, which is obtainable by adding an edge
between the centers of two nontrivial stars.
For a vertex u of a nontrivial tree T, the components of T −u are called the
branches of T at u. For A ⊆V(T), the A-branch-weight of u in T, denoted by
bwT (u,A), is deﬁned to be
max{|A∩V(B)|: B is a branch of T at u}.
For a tree T, a vertex in the A-centroid is called an A-centroid vertex. The
following lemma is a restatement of [16, Theorem 8].
Lemma 2.1. Let T be a tree of ordern≥2. Then u is an A-centroid vertex if
and only ifbwT (u,A) ≤bwT (v,A) for any v∈V(T).
For u,v ∈V(T), denote by nT (u,v|A) the number of vertices in A closer
to u than to v. Let T be a tree with u ∈V(T). For A = L(T),I(T), Wang
[19, Proposition 3.1] stated that u is an A-centroid vertex of T if and only if
nT (u,v|A) ≥nT (v,u|A) for any v∈NT (u).
We give a somewhat easy necessary and suﬃcient condition for a vertex of a
tree T being an A-centroid vertex for A= L(T),I(T).
Lemma 2.2.Let T be a tree of ordern≥3 with u∈V(T). ForA= L(T),I(T),
u is an A-centroid vertex ofT if and only ifbwT (u,A) ≤|A|
2 .
Proof. Let r = δT (u) and NT (u) = {u1,...,u r}. For i = 1 ,...,r , let Bi be
the branch of T at u containing ui and let ai = |A ∩V(Bi)|. Assume that
a1 ≥···≥ ar. Then, by deﬁnition, bwT (u,A) = a1.
Suppose that bwT (u,A) ≤|A|
2 , i.e., a1 ≤|A|
2 . For any v∈V(T)\(V(B1)∪{u}),
say v ∈V(Bi) with 2 ≤i ≤r, as T −V(Bi) is a subtree of a branch at v, we
have bwT (v,A) ≥|A∩(V(T) \V(Bi))|≥ ∑r
j=1 aj −ai ≥a1 = bwT (u,A). If
A = L(T), then ∑r
j=1 aj = |A|, so ∑r
j=2 aj ≥ |A|
2 , and for any v ∈ V(B1),
we have bwT (v,A) ≥|A∩(V(T) \V(B1))|= ∑r
j=2 aj ≥ |A|
2 ≥bwT (u,A). If
A= I(T), then ∑r
j=1 aj = |A|−1, so ∑r
j=2 aj ≥|A|
2 −1, and for any v∈V(B1),
we have bwT (v,A) ≥|A∩(V(T) \V(B1))|= 1 + ∑r
j=2 aj ≥ |A|
2 ≥bwT (u,A).
Therefore bwT (u,A) ≤bwT (v,A) for any v ∈V(T), which implies that u is an
A-centroid vertex of T by Lemma 2.1.
Conversely, suppose that u is an A-centroid vertex of T.
Case 1. A= L(T).
If |A|= 2, then T ∼= Pn and umay be any internal vertex. Then bwT (u,A) =
1 ≤|A|
2 . Suppose that |A|≥ 3. If bwT (u,A) > |A|
2 , i.e., a1 > |A|
2 , then ∑r
i=2 ai <
|A|
2 , so sT (u,L(T))−sT (u1,L(T)) = a1−∑r
i=2 ai >0, implying that sT (u,L(T)) >
sT (u1,L(T)), a contradiction. It follows that bwT (u,A) ≤|A|
2 .
3

Case 2. A= I(T).
If |A|= 1, then T ∼= Sn and u is the center. If |A|= 2, then T is a double
star and u may be either internal vertices. So we have bwT (u,A) = 0 ,1 ≤|A|
2
if |A|= 1 ,2. Suppose that |A|≥ 3. If bwT (u,A) > |A|
2 , i.e., a1 > |A|
2 , then∑r
i=2 ai < |A|
2 −1, so sT (u,I(T)) −sT (u1,I(T)) = a1 −1 −∑r
i=2 ai > 0, a
contradiction. It follows that bwT (u,A) ≤|A|
2 .
By combining Cases 1 and 2, we have bwT (u,A) ≤|A|
2 .
A leaf peripherian vertex of a tree T on n vertices is a vertex of T with
maximum leaf status. Note that every vertex of Pn is a leaf peripherian vertex
and LS(Pn) = n−1. In the following lemma, we show that a leaf peripherian
vertex of a tree that is not a path must be a leaf.
Lemma 2.3. Let T be a tree that is not a path. Letu ∈V(T). If u is a leaf
peripherian vertex ofT, then u∈L(T).
Proof. We prove the lemma by contradiction. Suppose thatuis a leaf peripherian
vertex of T but u /∈ L(T). Then δT (u) ≥ 2. Let r = dT (u) and NT (u) =
{u1,...,u r}, where r ≥2. For i = 1 ,...,r , let Bi be the branch of T at u
containing ui, Li = L(T) ∩V(Bi) and ai = |Li|. Assume that a1 ≤···≤ ar.
Suppose ﬁrst that r= 2 and a2 = a1. As T is not a path, we havea2 = a1 ≥2.
Let v∈L1 and let z be the unique vertex adjacent to v in T. Then
sT (u,L(T)) =
∑
w∈L1\{v}
dT (u,w) + dT (u,v) +
∑
w∈L2
dT (u,w),
sT (v,L(T)) =
∑
w∈L1\{v}
dT (v,w) +
∑
w∈L2
(dT (v,u) + dT (u,w)),
and so
sT (v,L(T)) −sT (u,L(T))
=
∑
w∈L1\{v}
(dT (v,w) −dT (u,w)) −dT (u,v) +
∑
w∈L2
dT (v,u)
>
∑
w∈L1\{v}
(dT (z,w) −dT (u,w)) −dT (u,v) +
∑
w∈L2
dT (v,u)
≥ −
∑
w∈L1\{v}
dT (z,u) −dT (u,v) +
∑
w∈L2
dT (v,u)
= −
∑
w∈L1\{v}
(dT (v,u) −1) −dT (u,v) +
∑
w∈L2
dT (v,u)
=
∑
w∈L1\{v}
1
= a1 −1
> 0.
4

Thus sT (v,L(T)) >sT (u,L(T)). This implies that ucan not be a leaf peripherian
vertex of T, a contradiction.
Suppose next that r= 2 and a2 >a1, or r≥3. Then
sT (u,L(T)) =
∑
v∈L1
dT (u,v) +
r∑
j=2
∑
v∈Lj
dT (u,v),
sT (u1,L(T)) =
∑
v∈L1
(dT (u,v) −1) +
r∑
j=2
∑
v∈Lj
(dT (u,v) + 1),
and so
sT (u1,L(T)) −sT (u,L(T)) =
∑
v∈L1
(−1) +
r∑
j=2
∑
v∈Lj
1
=
r∑
i=2
ai −a1
> 0.
Thus sT (u1,L(T)) > sT (u,L(T)). This implies that u is not a leaf peripherian
vertex of T, also a contradiction.
Therefore, u∈L(T), as desired.
A internal peripherian vertex of a tree T is a vertex of T with maximum
internal status.
Lemma 2.4. Let T be a tree. Suppose thatu is a internal peripherian vertex of
T. Then u∈L(T).
Proof. We prove the lemma by contradiction. Suppose that u /∈L(T). Then
δT (u) ≥2.
If there is a vertex v ∈ NT (u) with δT (v) = 1, then it is obvious that
sT (v,I(T)) > sT (u,I(T)), a contradiction. So δT (v) ≥2 for any v ∈NT (u).
Let r= δT (u) and NT (u) = {u1,...,u r}, where r≥2. For i= 1,...,r , let Bi be
the branch of T at ucontaining ui, Ii = I(T) ∩V(Bi) and ai = |Ii|. Assume that
a1 ≤···≤ ar. Let z ∈I1. Then
sT (u,I(T)) =
∑
w∈I1\{z}
dT (u,w) + dT (u,z) +
r∑
i=2
∑
w∈Ii
dT (u,w),
sT (z,I(T)) =
∑
w∈I1\{z}
dT (z,w) + dT (z,u) +
r∑
i=2
∑
w∈Ii
(dT (z,u) + dT (u,w)),
and so
sT (z,I(T)) −sT (u,I(T))
5

=
∑
w∈I1\{v}
(dT (z,w) −dT (u,w)) +
r∑
i=2
∑
w∈Ii
dT (z,u)
≥ −dT (z,u)(a1 −1) + dT (z,u)
r∑
i=2
ai
= dT (z,u)
(
−a1 + 1 +
r∑
i=2
ai
)
> 0.
Thus sT (z,I(T)) >sT (u,I(T)), a contradiction.
A tree is called starlike if it has at most one vertex of degree greater than 2.
So, a star and a path are both particular starlike trees.
A diametric path of a tree is a longest path in this tree (whose length equals the
diameter). Evidently, the terminal vertices of a diametric path of any nontrivial
tree are leaves.
A caterpillar is a tree such that the deletion of all leaves outside a diametric
path (if any exists) yields a path.
A leaf edge in a tree is an edge incident with a leaf.
For a tree T with uw∈E(T) and vw ̸∈E(T), if T′= T −uw+ vw is a tree,
then we also say that T′ is obtained from T by moving the edge uw from uto v.
A hanging path at a vertex u of a tree T is a path uu1 ...u ℓ with δT (u) ≥3,
δT (uℓ) = 1 and if ℓ≥2, δT (ui) = 2 for i= 1,...,ℓ −1.
Let P be a path in a tree T. For v ∈V(T) \V(P), the distance between v
and P is deﬁned to be dT (v,P ) = min{dT (v,w) : w∈V(P)}.
3 Minimum leaf status
Theorem 3.1. Let T be a tree of ordern. Then
ls(T) ≥n−1
with equality if and only ifT is starlike.
Proof. Let T be a tree of order n that minimizes the minimum leaf status. Let
ube an L(T)-centroid vertex. Suppose that there is a vertex v, diﬀerent from u,
with degree at least 3. Denote by v0,v1,...,v r−1 all the neighbors of v, where v0
lies on the unique path connecting u and v in T, and r= δT (v). Let
T′= T −{vvi : i= 1,...,r −2}+ {uvi : i= 1,...,r −2}.
Let V′ be the set of leaves in the branch of T at u containing v, and V′′ the set
of leaves of all the branches of T at v containing one of v1,v2,...,v r−2. Then
sT (u,L(T)) −sT′(u,L(T′)) = sT (u,V ′) −sT′(u,V ′)
6

=
∑
w∈V ′′
(dT (u,w) −dT′(u,w))
=
∑
w∈V ′′
dT (u,v)
= |V′′|dT (u,v)
> 0,
and so ls(T) = sT (u,L(T)) > sT′(u,L(T′)) ≥ls(T′), a contradiction. Thus,
all vertices diﬀerent from u are of degree 1 or 2. That is, there is at most one
vertex of degree at least 3, or T is starlike. By Lemma 2.2, in a starlike tree T
of order n, the vertex of maximum degree is an L(T)-centroid vertex, and thus
ls(T) = |E(T)|= n−1.
For integers n, a and b with 2 ≤a,b ≤ n−2
2 , Tn;a,b be the tree of order n
obtained from two stars Sa+1 and Sb+1 by connecting their centers by a path of
length n−a−b−1. For convenience, let Tn,a = Tn;a,a.
Theorem 3.2. Let T be a tree of ordern≥6. Then
ls(T) ≤
⌊(n+ 1)2
8
⌋
with equality if and only if T ∼= Tn,⌈n
4 ⌉ if n is even or n ≡ 3 (mod 4) , and
T ∼= Tn,n−1
4
,Tn,n+3
4
if n≡1 (mod 4) .
Proof. Let T be a tree of order n that maximizes the minimum leaf status.
Let x be an L(T)-centroid vertex. Let r = δT (x) and NT (x) = {x1,...,x r}.
For i = 1 ,...,r , let Bi be the branch of T at x containing xi and let ai =
|L(T) ∩V(Bi)|. Assume that a1 ≥···≥ ar.
By Theorem 3.1, T can not be a starlike tree and thus there are at least two
vertices of degree at least three, and it is obvious that one such vertex lies in
some branch of T at x.
Claim 1. If a branch of T at x contains a vertex of degree at least three in T,
then there is exactly one such vertex in this branch, and its neighbors in T are
all leaves except one lying on the unique path connecting to x.
Assume that B1 is a branch of T at xwith a vertex of degree at least three in
T. Let P = v0v1 ...v p be a longest path in T from a leaf of T in B1 to x, where
vp = x, vp−1 = x1 and p≥2. Then δT (vi) ≥3 for some i= 1,...,p −1. Suppose
that i> 1. Then p≥3. Let T′ be the tree obtained from T by moving all edges
outside P incident with vi from vi to v1. By Lemma 2.2, x is an L(T′)-centroid
vertex. It is evident that ls(T′) > ls(T), a contradiction. Thus, v1 is the only
vertex in B1 with degree at least three in T and all its neighbors are leaves of T
except the one lying on the path connecting to x. This proves Claim 1.
Claim 2. T is obtainable by connecting the centers of two copies of Sa1+1 by a
path, where a1 ≥2.
Suppose ﬁrst that r = 2. Then, by Lemma 2.2, both B1 and B2 contain a
vertex of degree at least three in T, and by Claim 1, there is exactly one vertex
7

of degree at least three in each of B1 and B2, and its neighbors in T are all leaves
except one lying on the path connecting to x. So, T is obtainable by connecting
the centers of two stars, say Sa1+1 and Sa2+1, by a path, where a1 ≥a2 ≥2.
Suppose that a1 > a2. Let z be the vertex in B1 with degree a1 + 1 in T. Then
bwT (x,L(T)) = a1 >a2 = bwT (z,L(T)). So x is not an L(T)-centroid vertex by
Lemma 2.1, a contradiction. Thus a1 = a2.
Suppose next that r≥3. Assume that B1 is a branch of T at x containing a
vertex of degree at least three in T. By Claim 1, there is exactly one such vertex
v1, and the neighbors of v1 in T are all leaves except the one lying on the path
between v1 and x. Let z ∈L(T) ∩V(Br), k = dT (x,z) and ℓ = dT (x,v1). By
Lemma 2.1, a1 = bwT (x,L(T)) ≤bwT (v1,L(T)) = ∑r
i=2 ai.
Suppose that a1 <∑r
i=2 ai. Suppose ﬁrst that ar = 1. Let
T′= T −xx1 + x1z.
Note that ∑r
i=1 ai = |L(T)|. As a1 < ∑r
i=2 ai, we have 2 a1 < |L(T)|, so a1 ≤
|L(T)|−1
2 = |L(T′)|
2 . Then, by Lemma 2.2, x is an L(T′)-centroid vertex. Thus
ls(T′) −ls(T) = sT′(x,L(T′)) −sT (x,L(T))
= ( k+ ℓ+ 1)a1 −k−(ℓ+ 1)a1
= ( a1 −1)k
> 0.
That is, ls(T′) >ls(T), a contradiction. Suppose next that ar ≥2. Let z1,...,z ar
be the leaves of T in Br, where z1 = z. By Claim 1, these leaves are adjacent to a
common vertex, say vr. We consider a1 ≤∑r−1
i=2 ai and a1 >∑r−1
i=2 ai separately.
In the former case, let
T′= T −xx1 −{vrzi : i= 2,...,a r}+ {zizi+1 : i= 1,...,a r −1}+ x1zar .
As a1 ≤|L(T)|−ar
2 = |L(T)′|
2 , x is an L(T′)-centroid vertex by Lemma 2.2, so
ls(T′)−ls(T) = (k+ar −1 +ℓ+ 1)a1 −kar −(ℓ+ 1)a1 = (k+ar −1)a1 −kar >0,
i.e., ls(T′) >ls(T), a contradiction. In the latter case, let
T′= T −{xxi : i= 2,...,r −1}+ {xrxi : i= 2,...,r −1}.
By Lemma 2.2, xr is an L(T′)-centroid vertex. Then ls(T′)−ls(T) = a1 −ar >0,
also a contradiction. Therefore, a1 = ∑r
i=2 ai.
If |V(Bi)|>1 for some 2 ≤i≤r, then for the tree
T′′= T −{xxj : j = 2,...,r with j ̸= i}+ {xixj : j = 2,...,r with j ̸= i},
as x is an L(T′′)-centroid vertex by Lemma 2.2, we have ls(T′′) > ls(T). This
contradiction shows that |V(B2)|= ··· = |V(Br)|= 1. This proves Claim 2.
8

By Claim 2, T ∼= Tn,a1 . Then the diameter of T is d= n+ 1 −2a1, and any
internal vertex is an L(T)-centroid vertex. Let v be the neighbor of some leaf.
So
ls(T) = sT (v,L(T)) = a1 + a1(d−1) = a1d= a1(n+ 1 −2a1) := f(a1),
which is strictly increasing when a1 ≤n+1
4 and strictly decreasing when a1 ≥n+1
4 .
If n≡3 (mod 4), then f(a1) ≤f
(n+1
4
)
= (n+1)2
8 =
⌊
(n+1)2
8
⌋
with equality if and
only if a1 = n+1
4 . If n ≡2 (mod 4), then f(a1) ≤f
(n+2
4
)
= n(n+2)
8 =
⌊
(n+1)2
8
⌋
with equality if and only if a1 = n+2
4 . If n ≡0 (mod 4), then f(a1) ≤f
(n
4
)
=
n(n+2)
8 =
⌊
(n+1)2
8
⌋
with equality if and only if a1 = n
4 . If n ≡1 (mod 4), then
f(a1) ≤f
(n−1
4
)
= f
(n+3
4
)
= (n−1)(n+3)
8 =
⌊
(n+1)2
8
⌋
with equality if and only if
a1 = n−1
4 or n+3
4 . So, we have T ∼= Tn,a, where
a=



⌈n
4 ⌉ if n is even or n≡3 (mod 4)
n−1
4 ,n+3
4 if n≡1 (mod 4)
and ls(T) =
⌊
(n+1)2
8
⌋
.
Theorem 3.3.Let T be a tree of ordern with diameterd, where3 ≤d≤n−1.
Then
ls(T) ≤



(n−d+1)d
2 if n−d is odd
(n−d)d
2 + 1 if n−d is even
with equality if and only ifT ∼= Tn,n−d+1
2
when n−dis odd, andT ∼= Tn; n−d
2 ,n−d+2
2
,
or d ≥4 and T is isomorphic to a tree obtained fromTn−1,n−d
2
by adding a leaf
edge at a vertex of degree two whenn−d is even.
Proof. If d = n−1, then the result is trivial as n−d = 1 is odd, T ∼= Pn and
ls(T) = n−1 = (n−d+1)d
2 .
Suppose that d ≤n−2. Let T be a tree of order n with diameter d that
maximizes the minimum leaf status. Let x be an L(T)-centroid vertex. Let
r = δT (x) and NT (x) = {y1,...,y r}. For i= 1,...,r , let Bi be the branch of T
at x containing yi and let ai = |L(T) ∩V(Bi)|.
Suppose that r = 2. By Lemma 2.2, a1,a2 ≤ |L(T)|
2 . So a1 = a2 = |L(T)|
2 .
Choose a vertex w ∈V(B1) with δT (w) ≥3 such that dT (x,w) is as small as
possible. Then bwT (w,L(T)) = a2 = |L(T)|
2 . So w is an L(T)-centroid vertex by
Lemma 2.2. Therefore, we may assume that r ≥3. Let P := x0x1 ...x d be an
arbitrary diametric path of T.
Claim 1. x is in some diametric path.
Suppose this is not true. That is, xlies outside any diametric path. Then, for
some i with 3 ≤i≤d−3, one has dT (x,P) = dT (x,xi) ≤min{i−2,d −i−2}.
9

Assume that xi ∈Br. Suppose that aj >ar for some j with 1 ≤j ≤r−1. Let
T′ be the tree obtained from T by moving the edges xyk with 1 ≤k ≤r−1
and k ̸= j from x to yr. Note that the diameter of T′ is d and L(T′) = L(T).
As aj >ar, we have bwT′(yr) = max{a1,...,a r−1}= bwT (x). By Lemma 2.2, yr
is an L(T′)-centroid vertex. So ls(T) = sT (x,L(T)) < sT (x,L(T)) + aj −ar =
sT′(yr,L(T′)) = ls(T′). This contradiction shows that aj ≤ar for 1 ≤j ≤r−1.
Suppose that, for some 1 ≤j ≤r−1, aj < ar, and either δT (yj) ≥2 or
δT (yj) = 1 and ar < |L(T)|
2 .
Let T′′be the tree obtained fromT by moving the edgesxyk with 1 ≤k≤r−1
and k̸= jfrom xto yj. Evidently, the diameter of T′′is d. Let T0 be the maximal
subtree of T −xyj containing yj. Note that the branches of T′′−yj are Bk with
1 ≤k≤r−1 and k̸= j, T[{x}∪V(Br)], and if δT (yj) ≥2, the branches of T0 at
yj. As ak ≤ar for 1 ≤k≤r−1, bwT′′(yj) = max{ak : k= 1,...,r,k ̸= j}= ar.
If δT (yj) ≥2, then bwT′′(yj) = ar = bwT (x) ≤|L(T)|
2 = |L(T′′)|
2 by Lemma 2.2.
If δT (yj) = 1 and ar < |L(T)|
2 , then bwT′′(yj) = ar ≤|L(T)|−1
2 = |L(T′′)|
2 . In either
case, yj is an L(T′′)-centroid vertex by Lemma 2.2. So ls(T) = sT (x,L(T)) <
sT (x,L(T)) + ar −aj = sT′′(yj,L(T′′)) = ls(T′′), a contradiction. Therefore
a1 = ··· = ar, or δT (yj) = 1 for 1 ≤j ≤r−1 and ar = |L(T)|
2 . We show both
cases are impossible.
Case 1. δT (yj) = 1 for 1 ≤j ≤r−1 and ar = |L(T)|
2 .
Obviously, r−1 = |L(T)|
2 . Let w be a vertex in Br with δT (w) ≥3 such that
dT (w,x) is as small as possible. Note that bwT (w) = |L(T)|
2 . So w is an L(T)-
centroid vertex by Lemma 2.2. Suppose that w ̸= xi. Let w′ be the neighbor
of w in the branch of T at w containing xi. Let T′ be the tree obtained from
T by moving edges incident with w outside the path connecting x and xi from
w to w′. Then bwT′(w′) = |L(T)|
2 = |L(T′)|
2 . Thus w′ is an L(T′)-centroid vertex
by Lemma 2.2. It is evident that sT′(w′,L(T′)) > sT (w,L(T)), implying that
ls(T′) = sT′(w′,L(T′)) > sT (w,L(T)) = ls(T), a contradiction. It thus follows
that w = xi. Let T′′ = T −xy1 + x1y1. As bwT′′(xi) ≤|L(T′′)|
2 , xi is an L(T′′)-
centroid vertex by Lemma 2.2. Then ls(T′′) = sT′′(xi,L(T′′)) > sT (xi,L(T)) =
sT (x,L(T)) = ls(T), a contradiction. So Case 1 can not occur.
Case 2. a1 = ··· = ar.
Let w be a vertex in Br with δT (w) ≥3 such that dT (x,w) is as small as
possible. Let T′ = T −{xyj : 2 ≤ j ≤ r −1}+ {wyj : 2 ≤ j ≤ r −1}.
Note that bwT′(w) = bwT (x) = a1 < |L(T)|
2 = |L(T′)|
2 . So w is an L(T′)-centroid
vertex by Lemma 2.2. Thus ls(T′) −ls(T) = sT′(w,L(T′)) −sT (x,L(T)) =
a1dT (x,w) −ardT (x,w) = 0, i.e., ls(T′) = ls(T).
Suppose that w ̸= xi. Let t = δT′(w) and NT′(w) = {w1,...,w t}. For j =
1,...,t , let B′
j be the branch of T at wcontaining wj and let bj = |L(T′)∩V(B′
j)|.
Assume that x ∈ V(B′
1) and xi ∈ V(B′
t). Let T′′ = T′ −{wwi : 2 ≤ j ≤
t−1}+ {wtwi : 2 ≤j ≤t−1}. Obviously, bwT′′(wt) = b1 = a1, so wt is an
L(T′′)-centroid vertex by Lemma 2.2. Note also that b1 = a1 = ar > bt. Then
ls(T′′) = sT′′(wt,L(T′′)) = sT′(w,L(T′)) + b1 −bt > sT′(w,L(T′)) = ls(T′) =
10

ls(T), a contradiction. Thus w= xi. Let n1 (n2, respectively) be the number of
leaves in the branch of T′ at xi containing xi−1 (xi+1, respectively). Let z1 be
the neighbor of xi in the path connecting xi and x in T′. Assume that n1 ≥n2.
Suppose that n1 > n2. Denote by T1 the tree obtained from T′ by moving the
edges xiz1,xiy2,...,x iyr−1 from xi to xi+1. By Lemma 2.2, bwT1 (xi+1) = a1 =
bwT′(xi) ≤|L(T′)|
2 = |L(T1)|
2 , and so xi+1 is an L(T1)-centroid vertex. Thus ls(T1) =
sT1 (xi+1,L(T1)) ≥sT′(xi,L(T′))+ n1 −n2 >sT′(xi,L(T′)) = ls(T′) = ls(T). This
contradiction shows that n1 = n2. Let T2 = T′−{xiz1,xiy2}+ {xi−1z1,xi+1y2}.
Note that there aren1+a1 leaves in the branch ofT2 at xi containing x0 and n2+a2
(= n1 + a1) leaves in the branch of T2 at xi containing xd. Thus bwT2 (xi) = a1 +
n1 ≤|L(T2)|
2 , implying that xi is an L(T2)-centroid vertex by Lemma 2.2. It follows
that ls(T2) = sT2 (xi,L(T2)) = sT′(xi,L(T′)) + 2a1 >sT′(xi,L(T′)) = ls(T′), also
a contradiction. So Case 2 can not occur.
Now Claim 1 follows by combining the above two cases.
By Claim 1, we may assume that xi = x, where 1 ≤i≤d−1. Denote by a
the number of leaves in the branch of T at xi containing xi−1.
Claim 2. T is a caterpillar.
Suppose that T is not a caterpillar. Then d(w,P ) ≥2 for some leaf w of T
outside P. Let u be the unique neighbor vertex of w. Assume that d(w,xj) =
d(w,P ) and j ≤i. We want to show that j = i. Suppose that j < i. Choose j
such that i−j is as small as possible. If j < i−1 and δT (xk) ≥3 for some k
with j < k < i, then by moving the leaf edges at xk to x1, we get a tree T′ for
which x is still an L(T′)-centroid by Lemma 2.2, so ls(T′) > ls(T), which is a
contradiction. Thus δT (xj+1) = ··· = δT (xi−1) = 2 if j <i−1. Denote by T′the
tree obtained from T by moving all the leaf edges at ufrom uto x1. If xi is also
an L(T′)-centroid vertex, then, as dT (x1,xi) ≥dT (u,xi) and u∈L(T′), we have
ls(T′) = sT′(xi,L(T′)) >sT (xi,L(T)) = ls(T), a contradiction. Thus xi is not an
L(T′)-centroid vertex. Note that the branches of T′at xi containing no xj are just
the branches of T at xi not containing xj, and that xi is an L(T)-centroid vertex.
By Lemma 2.2, a+ 1 = bwT′(x) > |L(T′)|
2 and a ≤|L(T)|
2 . So |L(T)|+1
2 = |L(T′)|
2 <
a+ 1 ≤ |L(T)|
2 + 1, i.e., a = |L(T)|
2 . Then bwT (xj,L(T)) = bwT′(xj,L(T′)) =
|L(T)|−a = |L(T)|
2 , so xj is an L(T)-centroid vertex and also an L(T′)-centroid
vertex by Lemma 2.2. Thus ls(T′) = sT′(xj,L(T′)) >sT (xj,L(T)) = ls(T), also
a contradiction. This shows that j = i.
By the choice of T, each internal vertex of T on P diﬀerent from x1,xd−1,xi
has degree two. Otherwise, as above, by moving the leaf edges from these vertices
to x1 or xd−1 would result in a tree with larger minimum leaf status. Note that the
number of leaves in the branch of T at xi containing xi−1 is a. Let p= δT (u) −1.
Let k be the number of leaves in the branch of T at xi containing w. Let n0 be
the maximum number of leaves in a branch of T at xi containing no xi−1 and w.
Suppose that a+ p≤|L(T)|+1
2 . Let T′be the tree obtained from T by moving the
leaf edges at ufrom uto x1. By Lemma 2.2, bwT′(xi) = max{a+p,k−p+1,n0}≤
max
{
a+ p,|L(T)|
2
}
≤ |L(T)|+1
2 , and so xi is an L(T′)-centroid vertex. Then we
11

have ls(T′) = sT′(xi,L(T′)) > sT (xi,L(T)) = ls(T), a contradiction. It thus
follows that a+ p> |L(T)|+1
2 , i.e., p> |L(T)|+1
2 −a. We form a tree T′′ by moving⌊
|L(T)|+1
2
⌋
−aleaf edges at ufrom uto x1 and the remaining leaf edges at ufrom
u to xd−1. Note that bwT′′(xi) =
⌊
|L(T)|+1
2
⌋
≤|L(T′′)|
2 . Thus xi is also an L(T′′)-
centroid vertex by Lemma 2.2. So ls(T′′) = sT2 (xi,L(T2)) > sT (xi,L(T)) =
ls(T), a contradiction. This completes the proof Claim 2.
By Claim 2, T is a caterpillar. Then |L(T)|= n−d+ 1. Note that a =
δT (x1) −1. Let b= δT (xd−1) −1.
Case 1. n−d is odd.
We want to showi= 1 or d−1. Suppose that this is not true. By the choice of
T, each vertex from x2,...,x d−2 diﬀerent from xi has degree two in T. Note that
the number of leaves at xi in T is n−d+ 1−a−b. By Lemma 2.2, a,b ≤n−d+1
2 .
Suppose that a < n−d+1
2 . We form a tree T′ by moving n−d+1
2 −a leaf edges
at xi from xi to x1. Evidently, ls(T′) = sT′(xi,L(T′)) > sT (xi,L(T)) = ls(T),
a contradiction. So a = n−d+1
2 . Similarly, b = n−d+1
2 . Thus T ∼= Tn,n−d+1
2
and
ls(T) = (n−d+1)d
2 .
Case 2. n−d is even.
If i = 1 or d−1, then with a similar argument as in Case 1, we have T ∼=
Tn; n−d
2 ,n−d+2
2
and ls(T) = (n−d)d
2 + 1. Suppose that i ̸= 1 ,d −1. Then d ≥4.
By the choice of T, each vertex from x2,...,x d−2 diﬀerent from xi has degree
two in T. By Lemma 2.2, a,b ≤ n−d
2 . Suppose that a < n−d
2 . Then a tree
T′ can be formed by moving n−d
2 −a leaf edges at xi from xi to x1. Thus
ls(T′) = sT′(xi,L(T′)) > sT (xi,L(T)) = ls(T), a contradiction. Thus a = n−d
2 .
Similarly, b = n−d
2 . Thus T is isomorphic to a tree obtained from Tn−1,n−d
2
by
adding a leaf edge at a vertex of degree two, ls(T) = (n−d)d
2 + 1.
The result follows by combining the above two cases.
4 Maximum leaf status
Theorem 4.1. Let T be a tree of ordern. Then
LS(T) ≥n−1
with equality if and only ifT ∼= Pn.
Proof. If T ∼= Pn, then LS(T) = n−1.
Suppose that T is not a path. Then n≥4. Let xbe a leaf peripherian vertex
of T. By Lemma 2.3, x∈L(T). So LS(T) = sT (x,L(T)) = ∑
y∈L(T)\{x}dT (x,y).
Let ube a vertex of degree at least three such thatdT (x,u) is as small as possible.
Then the unique path from x to any other leaf of T contains the path from x to
u. On the other hand, every edge of T lies on some path connecting x and some
other leaf of T. So
LS(T) =
∑
y∈L(T)\{x}
dT (x,y)
12

≥ dT (x,u)(|L(T)|−1) + n−1 −dT (x,u)
≥ |L(T)|−2 + n−1
> n −1.
So the result follows.
For integers n, a with 1 ≤a≤n−2, let Pn,a be the tree of order n obtained
by identifying the center of a star Sa+1 and a terminal vertex of a path Pn−a.
Particularly, Pn,1 = Pn and Pn,n−2 = Sn.
Theorem 4.2. Let T be a tree of ordern≥4. Then
LS(T) ≤
⌊n2
4
⌋
with equality if and only ifT ∼= Pn,n
2
for even n, and T ∼= Pn,n−1
2
,Pn,n+1
2
for odd
n.
Proof. If n = 4, then T ∼= P4 or S4 (= P4,2) and LS(P4) = 3 < 4 = LS(P4,2).
If n = 5, then T ∼= P5, P5,2 or S5 (= P5,3) and LS(P5) = 4 < 6 = LS(P5,2) =
LS(P5,3). So the result holds if n= 4,5.
Suppose that n≥6. Let T be a tree of order nthat maximizes the maximum
leaf status. Note that the maximum leaf status of Pn,n
2
for even n, and Pn,n−1
2
or
Pn,n+1
2
for odd n is
⌊
n2
4
⌋
. If T ∼= Pn, then LS(T) = n−1 <
⌊
n2
4
⌋
. If T ∼= Sn,
then LS(T) = 2(n−2) <
⌊
n2
4
⌋
. So T is neither a path nor a star.
Let x be a leaf peripherian vertex of T. By Lemma 2.3, x ∈L(T). Let
P := x0 ...x r be a longest path of T starting from x0 = x. Then 3 ≤r≤n−2.
Note that δT (xi) ≥3 for some iwith 1 ≤i≤r−1. By the choice of T, δT (xi) = 2
for i= 1,...,r −2, as, otherwise, by moving an edge outside P from xi to xr−1 we
get a tree T′, for which we have LS(T′) ≥sT′(x,L(T′)) >sT (x,L(T)) = LS(T),
which is a contradiction. As P is a longest path from x, all neighbors of xr−1
except xr−2 are leaves. Let a= δT (xr−1) −1. Then T ∼= Pn,a, and
LS(T) = sT (x,L(T)) = a(n−a)
which is maximized to ⌊n2
4 ⌋if and only if a= n
2 if n is even, and a= n−1
2 ,n+1
2 if
n is odd.
Theorem 4.3.Let T be a tree of ordern with diameterd, where2 ≤d≤n−1.
Let t=
⌈
2(n−1−d)
d
⌉
for even d and t=
⌈
2(n−1−d)
d−1
⌉
for oddd. Then
LS(T) ≥n−1 +
⌈dt
2
⌉
with equality if and only ifT is a tree with a diametric path between two leaves
x and y and exactly t hanging paths at vertices of the diametric path such that
LS(T) = sT (x,L(T)) = sT (y,L(T)) for evendtand LS(T) = max{sT (x,L(T)),sT (y,L(T))}
and |sT (x,L(T)) −sT (y,L(T))|= 1 for odddt.
13

Proof. Let P := v0v1 ...v d be a diametric path in T. Let L∗(T) = L(T)\{v0,vd}.
Note that ∑
w∈L∗(T)
dT (w,P ) ≥|E(T)|−d= n−1 −d
with equality if and only if each vertex outside P has degree one or two in T.
For convenience, denote by t= ⌈2(n−1−d)
d ⌉for even d and t= ⌈2(n−1−d)
d−1 ⌉for odd
d. By a result of Qiao and Zhan [14], |L(T)|≥ t+ 2. So |L∗(T)|≥ t. Then
LS(T) ≥ max{sT (v0,L(T)),sT (vd,L(T))}
≥ sT (v0,L(T)) + sT (vd,L(T))
2
= d+
∑
w∈L∗(T)
dT (v0,w) + dT (vd,w)
2
= d+ |L∗(T)|d
2 +
∑
w∈L∗(T)
dT (w,P ) (4.1)
≥ d+ dt
2 + n−1 −d
= n−1 + dt
2 .
So
LS(T) ≥n−1 +
⌈dt
2
⌉
.
Suppose that LS(T) = n−1 +
⌈dt
2
⌉
. By the proof of (4.1), each vertex
outside P has degree one or two in T. Note also that |L∗(T)|= t. Otherwise,
|L∗(T)|≥ t+ 1. So, by (4.1),
n−1 +
⌈dt
2
⌉
= LS(T) ≥d+ |L∗(T)|d
2 + n−1 −d≥n−1 + d(t+ 1)
2 ,
a contradiction. So T is a tree with a diametric path P and exactly t hanging
paths at vertices of P.
If dtis even, then the three inequalities in (4.1) must be equalities, soLS(T) =
sT (v0,L(T)) = sT (vd,L(T))
Suppose next that dt is odd. From (4.1), we have
max{sT (v0,L(T)),sT (vd,L(T))}− sT (v0,L(T)) + sT (vd,L(T))
2 ≤1
2,
i.e., |sT (v0,L(T)) −sT (vd,L(T))|= 0,1. As |L∗(T)|= t, we have |sT (v0,L(T)) −
sT (vd,L(T))|= 1 by (4.1).
From (4.1), we also have LS(T) = max{sT (v0,L(T)),sT (vd,L(T))}, as other-
wise,
n−1 +
⌈dt
2
⌉
= LS(T)
14

> max{sT (v0,L(T)),sT (vd,L(T))}
= sT (v0,L(T)) + sT (vd,L(T)) + 1
2
= n−1 +
⌈dt
2
⌉
,
a contradiction.
Conversely, if T is a tree with a diametric path between two leaves x and y
and exactly thanging paths at vertices of the diametric path such that LS(T) =
sT (x,L(T)) = sT (y,L(T)) for even dt and |sT (x,L(T)) −sT (y,L(T))|= 1 and
LS(T) = max{sT (x,L(T)),sT (y,L(T))}for odd dt, then
LS(T) = max {sT (x,L(T)),sT (y,L(T))}
=
⌈sT (x,L(T)) + sT (y,L(T))
2
⌉
= n−1 +
⌈dt
2
⌉
,
as desired.
We give an example on trees of order 15 with diameter 8. The three trees in
Fig. 1 are the ones that minimize the maximum leaf status.
Fig. 1: Three trees of order 15 with diameter 8.
Theorem 4.4.Let T be a tree of ordern with diameterd, where2 ≤d≤n−1.
Then
LS(T) ≤d(n−d)
with equality if and only ifT ∼= Pn,n−d.
Proof. The result is trivial if d= 2,n −1. Suppose that 3 ≤d≤n−2. Let T be
a tree of order n with diameter d that maximizes the maximum leaf status.
Let x be a leaf peripherian vertex of T. By Lemma 2.3, x∈L(T). We want
to show that x lies on some diametric path of T. Suppose that this is not true.
That is, x lies outside any diametric path. Let P := x0x1 ...x d be an arbitrary
diametric path of T. Then dT (x,P) = dT (x,xi) for some iwith 2 ≤i≤d−2 and
1 ≤dT (x,xi) ≤min{i−1,d −i−1}. By the choice of T, any vertex in the path
Q connecting x and xi except x and xi (if any exists) has degree two in T, as,
otherwise, we move an edge outsideQfrom this vertex to xi to form a tree T′, and
for T′, its diameter is still d, but LS(T′) ≥sT′(x,L(T′)) >sT (x,L(T)) = LS(T),
15

which is a contradiction. Let r= δT (xi). Denote by z1,...,z r the neighbors of xi
in T, where z1 lies on the path Q, z2 = xi−1 and z3 = xi+1. For i= 1,...,r , let
Bi be the branch of T at xi containing zi, and let ai = |V(Bi) ∩L(T)|. Suppose
that r ≥4. Let T′ = T −xiz1 + xi−1z1. and T′′ = T −xiz1 + xi+1z1. Note the
diameters of T′ and T′′ are both d. By direct calculation,
sT′(x,L(T′)) −sT (x,L(T)) =
r∑
j=3
∑
w∈V (Bj)∩L(T)
1 −
∑
w∈V (B2)∩L(T)
1
=
r∑
j=3
aj −a2
=
r∑
j=2
aj −2a2,
and similarly,
sT′′(x,L(T′′)) −sT (x,L(T)) =
r∑
j=2
aj −2a3.
So sT′(x,L(T′))−sT (x,L(T))+ sT′′(x,L(T′′))−sT (x,L(T)) = 2 ∑r
j=4 aj >0, im-
plying that either LS(T′) ≥sT′(x,L(T′)) >LS (T) or LS(T′′) ≥sT′′(x,L(T′′)) >
LS(T), a contradiction. It follows that r = 3. Suppose that there is a leaf of T
diﬀerent from x such that it is not adjacent to x1 or xd−1. Choose such a leaf y
of T such that dT (y,P ) is as large as possible. Assume that dT (y,P ) = dT (y,xj),
where 2 ≤j ≤d−2 with j ̸= i. Assume that j < i. Let y′ be the unique
neighbor of y in T. By moving the leaf edges at y′from y′to x1 we get a tree T′,
for which we have LS(T′)−LS(T) ≥sT′(x,L(T′))−sT (x,L(T)) ≥dT (x,y′) >0,
so LS(T′) > LS(T), a contradiction. This shows that δT (xk) = 2 for any
2 ≤k≤d−2 with k̸= i.
Let ℓ= dT (x,xi). Assume that i≤⌊d
2 ⌋. By the choice of T, δT (x1) = 2 and
δT (xd−1) = n−d−ℓ. So LS(T) = sT (x,L(T)) = ℓ+ i+ (ℓ+ d−i)(n−d−ℓ−1)
and sT (x0,L(T)) = ( n −d −ℓ −1)d + ℓ + i. But sT (x0,L(T)) −LS(T) =
(n−d−ℓ−1)(i−ℓ) >0, a contradiction. Thus x lies on some diametric path
of T.
Let P′ := xv1 ...v d be a diametric path starting from x. By the choice of T
and the argument as above, all leaves of T diﬀerent from x are adjacent to vd−1,
i.e., T ∼= Pn,n−d. The result follows by noting that LS(T) = d(n−d).
5 Minimum internal status
Proposition 5.1. Let T be a tree of ordern≥3.
(i) is(T) ≥0 with equality if and only ifT ∼= Sn.
(ii) If T ≇ Sn, then is(T) ≥1 with equality if and only ifT is a double star.
16

(iii) If T ≇ Sn, and T is not a double star, thenis(T) ≥2 with equality if and
only if T is a caterpillar of diameter4.
Proof. Item (i) follows from the fact that Sn is the only tree with exactly one
internal vertex. Item (ii) follows as the double stars are the only trees with exactly
two (adjacent) internal vertices. Item (iii) follows as for any tree T of diameter
at least 4 contains three internal vertices inducing a path P3 in T, and if T has
more than 3 internal vertices, then the subtree induced by internal vertices in T
contains S4 or P4 so that is(T) ≥3.
Furthermore, we have
Proposition 5.2. Suppose that T is a tree of ordern with diameter d, where
2 ≤d≤n−1. Then
is(T) ≥
⌊(d−1)2
4
⌋
with equality if and only ifT is caterpillar.
Proof. By Lemma 2.2, an I(T)-centroid vertex is an internal vertex of T.
Let P := v0 ...v d be a diametric path in T. Obviously, {v1,...,v d−1}induces
in T a path Pd−1. If T is a caterpillar, then is(T) = s(Pd−1). Suppose that
T is not a caterpillar, i.e., I(T) \V(P) ̸= 0. For any i = 1 ,...,d −1, we
have sT (vi,I(T)) ≥s(Pd−1) + ∑
w∈I(T)\V (P) dT (w,vi) > s(Pd−1). Suppose that
w ∈I(T) \V(P). Assume that dT (w,vj) = dT (w,P ) for some 2 ≤j ≤d−2.
Then we have
sT (w,I(T)) ≥sT (w,I(T) ∩V(P)) >sT (vj,I(T) ∩V(P)) ≥s(Pd−1).
Therefore, is(T) ≥s(Pd−1) =
⌊
(d−1)2
4
⌋
with equality if and only if T is caterpillar.
Theorem 5.1. Let T be a tree of ordern≥3. Then
is(T) ≤
⌊(n−2)2
4
⌋
with equality if and only ifT ∼= Pn.
Proof. By Lemma 2.2, an I(T)-centroid vertex is an internal vertex of T, so
is(T) equals to the minimum status of T′, i.e., is(T) = s(T′), where T′ is the
tree obtained from T by deleting all leaves. Let k = |L(T)|. By Proposition 2.1
in [1], we have
is(T) = s(T′) ≤
⌊(n−k)2
4
⌋
≤
⌊(n−2)2
4
⌋
with equalities if and only if k= 2 and T ∼= Pn.
17

6 Maximum internal status
Similarly to Proposition 5.1, we have
Proposition 6.1. Let T be a tree of ordern≥3. The following statements are
true.
(i) IS(T) ≥1 with equality if and only ifT ∼= Sn.
(ii) If T ≇ Sn, then IS(T) ≥3 with equality if and only ifT is a double star.
(iii) If T ≇ Sn, and T is not a double star, thenIS(T) ≥6 with equality if and
only if T is a caterpillar of diameter4.
Furthermore, we have
Proposition 6.2. Suppose that T is a tree of ordern with diameter d, where
2 ≤d≤n−1. Then IS(T) ≥d(d−1)
2 with equality if and only ifT is caterpillar.
Proof. Let P := v0v1 ...v d be a diametric path in T. Let I∗(T) = I(T) \
{v1,...,v d−1}. Then
IS(T) ≥ max{sT (v0,I(T)),sT (vd,I(T))}
≥ sT (v0,I(T)) + sT (vd,I(T))
2
=
2 ∑d−1
i=1 i+ ∑
w∈I∗(T)(dT (v0,w) + dT (vd,w))
2
≥ d(d−1)
2
with equality if and only if I∗(T) = ∅, i.e., T is a caterpillar.
Let T be a tree with u∈V(T). For positive integer p, we denote by Tu;p the
tree consisting of T and a path P := uu1 ...u p such that u is the only common
vertex of T and the path P. In this case, we also say that P is ‘hanging’ a path
of length pat uin Tu;p, though it is really a hanging path of length pat uin Tu;p
only when δT (u) ≥2.
Let Gu;0 = G. For nonnegative integer p and q, let Gu;p,q = (Gu;p)u;q.
Lemma 6.1. Let T be a nontrivial tree withu ∈V(T) Let p and q be positive
integers with p ≥q. Then IS(Tu;p+1,q−1) = IS(Tu;p,q) if q ≥2 and T is a star
with centeru, otherwise IS(Tu;p+1,q−1) >IS (Tu;p,q).
Proof. Let H = Tu;p,q and H′ = Tu;p+1,q−1. Let u0u1 ...u p and v0v1 ...v q be
the two ‘hanging’ paths at u in H, where u0 = v0 = u. Let x be a internal
peripherian vertex of H. Let L∗(T) = L(T) if u̸∈L(T) and L∗(T) = L(T) \{u}
otherwise. Then x∈L(H) = L∗(T) ∪{up,vq}by Lemma 2.4. As p≥q, we have
sH(up,I(H)) ≥sH(vq,I(H)). So we may assume that x ∈L∗(T) ∪{up}. Let
I∗(T) = I(T) if u∈I(T) and I∗(T) = I(T) ∪{u}otherwise.
18

Case 1. x∈L∗(T).
If q≥2, then
sH(x,I(H)) =
∑
w∈I∗(T)
dH(x,w) +
p−1∑
i=1
(dH(x,u) + i) +
q−1∑
i=1
(dH(x,u) + i)
=
∑
w∈I∗(T)
dH(x,w) + dH(x,u)(p+ q−2) +
p−1∑
i=1
i+
q−1∑
i=1
i,
and
sH′(x,I(H′)) =
∑
w∈I∗(T)
dH′(x,w) +
p∑
i=1
(dH′(x,u) + i) +
q−2∑
i=1
(dH′(x,u) + i)
=
∑
w∈I∗(T)
dH′(x,w) + dH′(x,u)(p+ q−2) +
p∑
i=1
i+
q−2∑
i=1
i.
Then sH′(x,I(H′))−sH(x,I(H)) = p−q+1 >0 and thusIS(H′) ≥sH′(x,I(H′)) >
sH(x,I(H)) = IS(H).
If q= 1, then
sH(x,I(H)) =
∑
w∈I∗(T)
dH(x,w) +
p−1∑
i=1
(dH(x,u) + i)
=
∑
w∈I∗(T)
dH(x,w) + dH(x,u)(p−1) +
p−1∑
i=1
i,
and
sH′(x,I(H′)) =
∑
w∈I∗(T)
dH′(x,w) +
p∑
i=1
(dH′(x,u) + i)
=
∑
w∈I∗(T)
dH′(x,w) + dH′(x,u)p+
p∑
i=1
i.
Then sH′(x,I(H′))−sH(x,I(H)) = dH(x,u)+p> 0 and thusIS(H′) ≥sH′(x,I(H′)) >
sH(x,I(H)) = IS(H).
Case 2. x= up.
Let q≥2. Then
sH(x,I(H)) =
∑
w∈I∗(T)
(p+ dH(u,w)) +
p−1∑
i=1
i+
q−1∑
i=1
(p+ i)
=
∑
w∈I∗(T)
(p+ dH(u,w)) + p(q−1) +
p−1∑
i=1
i+
q−1∑
i=1
i,
19

and
sH′(x,I(H′)) =
∑
w∈I∗(T)
(p+ 1 +dH′(u,w)) +
p∑
i=1
i+
q−2∑
i=1
(p+ 1 +i)
=
∑
w∈I∗(T)
(p+ 1 +dH′(u,w)) + (p+ 1)(q−2) +
p∑
i=1
i+
q−2∑
i=1
i.
Then sH′(x,I(H′)) −sH(x,I(H)) = |I∗(T)|−1. If |I∗(T)|≥ 2, then IS(H′) ≥
sH′(x,I(H′)) >sH(x,I(H)) = IS(H). If |I∗(T)|= 1, then IS(H′) = sH′(x,I(H′)) =
sH(x,I(H)) = IS(H).
Let q= 1. Then
sH(x,I(H)) =
∑
w∈I∗(T)
(p+ dH(u,w)) +
p−1∑
i=1
i,
and
sH′(x,I(H′)) =
∑
w∈I∗(T)
(p+ 1 +dH′(u,w)) +
p∑
i=1
i.
Then sH′(x,I(H′))−sH(x,I(H)) = |I∗(T)|+p> 0, and soIS(H′) ≥sH′(x,I(H′)) >
sH(x,I(H)) = IS(H).
The result follows by combing the above two cases and noting that|I∗(T)|= 1
if and only if T is a star with center u.
Theorem 6.1. Let T be a tree of ordern≥3. Then
IS(T) ≤n2 −3n+ 2
2
with equality if and only ifT ∼= Pn.
Proof. Let T be a tree of order n that maximizes the maximum internal status.
Suppose that T is not a path. Let x ∈ L(T). Then we choose a vertex of
degree at least three, say u, such that dT (x,u) is as large as possible. Then
there are two hanging paths P and Q at u in T. By Lemma 6.1, we can obtain
a tree T′ so that IS(T′) > IS(T), a contradiction. Thus T ∼= Pn. Evidently,
IS(Pn) = ∑n−2
i=1 i= n2−3n+2
2 .
Theorem 6.2. Let T be a tree of ordern with maximum degree∆, where 2 ≤
∆ ≤n−1. Then IS(T) ≤1
2 (n−∆)(n−∆ + 1) with equality if and only ifT is
a starlike tree with at least∆ −2 hanging paths being of length one.
Proof. It is trivial if ∆ = 2. Suppose that ∆ ≥3. Let T be a tree of order
n with maximum degree ∆ that maximizes the maximum internal status. Let
u be a vertex of degree ∆. If there is a vertex diﬀerent from u with degree at
20

least three, then we may choose such a vertex v by requiring that dT (u,v) is as
large as possible. This implies that there are two hanging paths at v in T. By
Lemma 6.1, there is a tree of order n with maximum degree ∆ having larger
maximum internal status, which is a contradiction. That is, u is the only vertex
of degree at least three. In other words, T is a starlike tree. By Lemma 6.1
again, ∆ −2 hanging paths are of length one. Thus T is a starlike tree with at
least ∆ −2 hanging paths being of length one. The result follows by noting that
IS(T) = IS(Pn,∆−1) = ∑n−∆
i=1 i= 1
2 (n−∆)(n−∆ + 1).
Acknowledgement. This work was supported by National Natural Science Foun-
dation of China (No. 11671156).
References
[1] M. Aouchiche, P. Hansen, Proximity and remoteness in graphs: results and
conjectures, Networks 58 (2011) 95–102.
[2] M. Aouchiche, P. Hansen, Proximity, remoteness and distance eigenvalues of
a graph, Discrete Appl. Math. 213 (2016) 17–25.
[3] M. Aouchiche, P. Hansen, Proximity, remoteness and girth in graphs, Dis-
crete Appl. Math. 222 (2017) 31–39.
[4] F. Buckley, F. Harary, Distance in Graphs, Addison-Wesley Publishing Com-
pany, Redwood City, CA, 1990.
[5] P. Dankelmann, Proximity, remoteness and minimum degree, Discrete Appl.
Math. 184 (2015) 223–228.
[6] P. Dankelmann, New bounds on proximity and remoteness in graphs, Com-
mun. Comb. Optim. 1 (2016) 29–41.
[7] D. Dimitrov, B. Ikica, R. ˇSkrekovski, Maximum external Wiener index of
graphs, Discrete Appl. Math. 257 (2019) 331–337.
[8] A.A. Dobrynin, R. Sharafdini, Stepwise transmission irregular graphs, Appl.
Math. Comput. 371 (2020) 124949.
[9] K. Durant, S. Wagner, Stephan, On the centroid of increasing trees, Discrete
Math. Theor. Comput. Sci. 21 (2019) Paper 8, 29 pp.
[10] C. Liang, B. Zhou, H. Guo, Minimum status, matching and domination of
graphs, Comput. J., Doi: 10.1093/comjnl/bxaa057.
[11] C. Lin, W.H. Tsai, J.L. Shang, Y.J. Zhang, Minimum statuses of connected
graphs with ﬁxed maximum degree and order, J. Comb. Optim. 24 (2012)
147–161.
21

[12] A.N.C. Kang, D.A. Ault, Some properties of a centroid of a free tree, Infor-
mation Processing Lett. 4 (1975/76) 18–20.
[13] Z. Peng, B. Zhou, Minimun status of trees with given parameters, RAIRO
Oper. Res., Doi: 10.1051/ro/2020015.
[14] P. Qiao, X. Zhan, Relation between the number of leaves of a tree and its
diameter, arXiv:1904.12150v1.
[15] R. Rissner, R.E. Burkard, Bounds on the radius and status of graphs, Net-
works 64 (2014) 76–83.
[16] P.J. Slater, Centers to centroids in graphs, J. Graph Theory 2 (1978) 209–
222.
[17] J. Sedlar, Remoteness, proximity and few other distance invariants in graphs,
Filomat 27 (2013) 1425–1435.
[18] D. Vukiˇ cevi´ c, G. Caporossi, Network descriptors based on betweenness cen-
trality and transmission and their extremal values, Discrete Appl. Math. 161
(2013) 2678–2686.
[19] H. Wang, Centroid, leaf-centroid, and internal-centroid, Graphs Combin. 31
(2015) 783–793.
[20] B. Zelinka, Medians and peripherians of a tree, Arch Math. 4 (1968) 87–95.
22