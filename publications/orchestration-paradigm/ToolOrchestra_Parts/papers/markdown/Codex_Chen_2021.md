1
2
0
2

l
u
J

8
2

]
h
p
-
p
e
h
[

1
v
2
8
3
3
1
.
7
0
1
2
:
v
i
X
r
a

SciPost Physics

Submission

High-energy logarithmic corrections to the QCD component of
same-sign W-pair production

Jeppe R. Andersen1, Bertrand Ducloué2(cid:63), Conor Elrick2, Andreas Maier3, Graeme Nail2 and
Jennifer M. Smillie2

1 Institute for Particle Physics Phenomenology, University of Durham, Durham, DH1 3LE, UK
2 Higgs Centre for Theoretical Physics, University of Edinburgh, Peter Guthrie Tait Road,
Edinburgh, EH9 3FD, UK
3 Deutsches Elektronen-Synchrotron DESY, Platanenallee 6, 15738 Zeuthen, Germany
* bertrand.ducloue@ed.ac.uk

July 29, 2021

Proceedings for the XXVIII International Workshop
on Deep-Inelastic Scattering and Related Subjects,
Stony Brook University, New York, USA, 12-16 April 2021
doi:10.21468/SciPostPhysProc.?

Abstract

We describe the calculation of the QCD contribution to same-sign W -pair production, pp → e±ν
α2+k
resumming all contributions scaling as α4
) [1]. These leading logarithmic
W
s
contributions are enhanced by typical cuts used for Vector Boson Scattering (VBS) studies.
We show that while the cross sections are little affected by these corrections, other more
exclusive observables relevant for experimental studies are affected more signiﬁcantly.

logk(ˆs/p2
⊥

µ±νµ j j,

e

1 Introduction

O

α2
s

(α2
W

Vector boson scattering (VBS) represents a key test of the standard model and has been the topic
of many experimental and theoretical studies (see e.g. [2] for a recent review). In addition to
the electroweak (EW) contribution of interest for such studies, other topologies may contribute
to the same ﬁnal state pp → V V + 2 j. This includes in particular the QCD contribution which
). To try to increase the relative importance of the EW contribution compared
starts at
to the QCD one, analyses typically implement so-called VBS cuts which require a large rapidity
separation and/or invariant mass between the leading jets in the event [3–5]. It turns out that this
is precisely the region where logarithmic corrections in log(ˆs/p2
) become important and need to
t
be resummed to all orders since in these kinematics the combination α
) is not necessarily
small. Therefore, while the VBS cuts are effective at increasing the EW fraction, they also make it
more difﬁcult to accurately evaluate the remaining QCD contribution. Here we will discuss how
these high energy contributions can be resummed to leading logarithmic (LL) accuracy in the HEJ
framework.

s log(ˆs/p2
t

1

SciPost Physics

Submission

µ (pi, po, p(cid:96), p¯(cid:96)) deﬁned in Eq. (2) which
Figure 1: Schematic illustration of the current jW
describes the production of a W boson from a quark line with an off-shell gluon (shown
as a zigzag line).

2 Construction of the Amplitudes

In this work we focus on same-sign W -pair production, pp → W ±W ±+ ≥ 2 j, where one W boson
decays in the electron channel and the other one in the muon channel. We start with the leading
order (LO) process:

q(pa

)Q(pb

±
) → (W
1

→)(cid:96)(p(cid:96)

1

)¯(cid:96)(p¯(cid:96)

1

±
)(W
2

→)(cid:96)(cid:48)(p(cid:96)

2

)¯(cid:96)(cid:48)(p¯(cid:96)

2

)q

(cid:48)(p1

)Q

(cid:48)(p2

),

(1)

with q and Q representing different quark or anti-quark ﬂavours. There are 8 Feynman diagrams
contributing at this order, corresponding to the possible ways to assign the W s to the different
quark lines. To describe the emission of a W boson from a quark line, we deﬁne the following
current:

µ (pi, po, p(cid:96), p¯(cid:96)) =
jW

1

(cid:2)¯u

−(p(cid:96))γαv

−(p¯(cid:96))(cid:3)

g 2
W
2
(cid:18) ¯u−(po

×

+ iΓ
(p(cid:96) + p¯(cid:96))2 − m2
W
)γα(/po
+ /p(cid:96)
+ /p¯(cid:96)
+ p(cid:96) + p¯(cid:96))2
(po

W mW
)γµu−(pi

¯u−(po

)

+

)γµ(/pi
(pi

− /p(cid:96)
− /p¯(cid:96)
− p(cid:96) − p¯(cid:96))2

)γαu−(pi

)

(cid:19)

,

(2)

as schematically represented in Fig. 1. This current is in fact the same as the one appearing in single
W plus jets production [6, 7]. The exact LO amplitude for the process (1) is implemented in the
HEJ event generator as a contraction of two such currents. In order to achieve leading-logarithmic
). Using the
accuracy, this must be supplemented with higher order corrections starting at
methods of the HEJ framework [8], this takes the form of Lipatov vertices describing real gluon
emissions between the two extremal partons and exponential factors for t-channel propagators,
arising from the virtual corrections and the integration of unresolved real emissions. We refer
to [1] for more details. These corrections capture the leading logarithmic behaviour at high energy.
Let us stress that while some approximations are made within the matrix element beyond leading
order, the phase space is integrated over in an exact way using Monte Carlo techniques, which
gives full ﬂexibility to implement the same cuts as experimental analyses.

(α3
s

O

While the amplitude as described above already has the correct LL behaviour, its accuracy can
be further improved by supplementing it with subleading terms providing LO accuracy at each
order in α
s up to the point where this is computationally feasible. This ﬁxed order matching is
implemented using the methods of HEJ2 [9,10] which is available at https://hej.hepforge.org. In
practice we have used Sherpa [11] to generate the ﬁxed-order input for this study, including LO
contributions up to 6 jets.

In addition, we also rescale the HEJ2 predictions to match the inclusive cross section obtained
at NLO. However, as explained in the following section, the inclusive cross sections are very close
in this particular setup and the matching therefore has a negligible impact.

2

=+SciPost Physics

Submission

Cross Section (fb) without VBS cuts, σ

HEJ2 W +W +
NLO W +W +
HEJ2 W −W −
NLO W −W −

1.428 ± 0.002
1.41 ± 0.05
0.6586 ± 0.0003
0.68 ± 0.02

VBS

incl with VBS cuts, σ
0.1219 ± 0.0004
0.12 ± 0.07
0.0402 ± 0.0001
0.04 ± 0.01

σ

incl

VBS

/σ
0.0854 ± 0.0003
0.08 ± 0.02
0.0610 ± 0.0002
0.06 ± 0.02

Table 1: Cross section obtained at LO+LL accuracy using HEJ2 compared with the result
at NLO accuracy, both before and after the additional VBS cuts given in the text.

3 Impact of the LL Corrections

We now turn to the HEJ2 predictions adapted to the 13 TeV LHC kinematics. The cuts on the jets
and leptons are the same as in a recent CMS analysis of this process [4]. In addition to the inclusive
cuts, CMS also considered additional so-called VBS cuts to try to increase the EW/QCD ratio:
m j1 j2

) < 0.75, where zl is the Zeppenfeld variable [12]:

| > 2.5 and max(zl

> 500 GeV, |∆η

j1 j2

η

l

=

zl

− 1
2
|η

j1

(η

+ η

j1
− η

|

j2

)

j2

.

(3)

In Table 1 we show the comparison of the cross sections obtained with HEJ2 and at NLO using
Sherpa [11] with the extension of OpenLoops [13]. We observe a very close agreement between
the two calculations, both before and after the VBS cuts. However, this agreement does not hold
for less inclusive observables as can be seen for example in Fig. 2 where we show the exclusive
jet rates obtained both before and after the additional VBS cuts. In the inclusive case one can
observe a steady decrease at each multiplicity. On the other hand, after imposing the VBS cuts,
the relative importance of the higher multiplicities is signiﬁcantly enhanced, with the 2-jet and
3-jet rates being very similar in the HEJ2 predictions, while the 3-jet rate is even larger than the 2-
jet one in the NLO calculation. These results show the importance of the higher-order corrections
resummed by HEJ2.

From now on we focus on the results with the additional VBS cuts. In Figs. 3 and 4 we show the
comparison of the HEJ2 and NLO calculations as a function of the pseudorapidity separation and
invariant mass of the leading jets, the transverse momentum of the leading jet and the Zeppenfeld
variable. One can see that the good agreement of the HEJ and NLO cross sections does not apply to
some distributions such as the transverse momentum of the leading jet and the invariant mass of
the leading jets. In these cases the logarithmic corrections give predictions which are substantially
larger than those predicted at NLO. On the other hand, the pseudorapidity separation of the lead-
ing jets and the Zeppenfeld variable show a close agreement between the two calculations, which
indicates that these observables are less sensitive to the logarithmic corrections studied here.

4 Conclusions

We have presented a calculation of the process pp → e±ν
)),
focusing on typical cuts used in VBS analyses. These cuts select regions of the phase space where
the high energy logarithms become important, and the HEJ2 exclusive event generator provides a
convenient framework to resum these contributions to all orders. While the inclusive cross sections

µ±νµ+ ≥ 2 j at

logk(ˆs/p2
t

αk+2
s

(α4
W

O

e

3

SciPost Physics

Submission

(a)

(b)

Figure 2: Exclusive jet rates for pp → W ±W ±+ ≥ 2 j, without (a) and with (b) the
additional VBS cuts.

(a)

(b)

Figure 3: Differential distributions in the pseudorapidity separation (a) and invariant
mass (b) of the two leading jets.

4

pp→(W→eνe)(W→µνµ)+jetsLHC@13TeVanti-kt,R=0.4,pj;⊥>50GeV,|ηj|<4.70.20.40.60.81.01.21.4dσdNjets[fb]NLOHEJ23456Njets0.00.51.01.5RatiotoNLOpp→(W→eνe)(W→µνµ)+jetsLHC@13TeVanti-kt,R=0.4,pj;⊥>50GeV,|ηj|<4.70.020.040.060.080.100.12dσdNjets[fb]NLOHEJ23456Njets0.00.51.01.5RatiotoNLOpp→(W→eνe)(W→µνµ)+jetsLHC@13TeVanti-kt,R=0.4,pj;⊥>50GeV,|ηj|<4.710−510−410−310−210−1dσd∆ηj1j2[fb]NLOHEJ345678∆ηj1j20.00.51.01.5RatiotoNLOpp→(W→eνe)(W→µνµ)+jetsLHC@13TeVanti-kt,R=0.4,pj;⊥>50GeV,|ηj|<4.710−710−610−510−410−3dσdmj1j2[fb/GeV]NLOHEJ5001000150020002500300035004000mj1j2[GeV]0.00.51.01.5RatiotoNLOSciPost Physics

Submission

(a)

(b)

Figure 4: Differential distributions in the transverse momentum of the leading jet (a)
and in the Zeppenfeld variable for the electron (b).

obtained in this approach are very similar compared to those at NLO, signiﬁcant differences can be
observed in several distributions relevant for experimental studies, such as the exclusive jet rates,
the invariant mass of the leading jets and the transverse momentum of the hardest jet. These
results show that the logarithmic corrections proportional to αk
) can be sizeable at the
13 TeV LHC and should be taken into account in order to accurately model the QCD contribution
to vector boson scattering.

s logk(ˆs/p2

t

Acknowledgements

We are grateful to our collaborators within HEJ for useful discussions throughout this project. The
predictions presented in section 3 were produced using resources from PhenoGrid which is part
of the GridPP Collaboration [14, 15].

Funding information We are pleased to acknowledge funding from the UK Science and Technol-
ogy Facilities Council, the Royal Society, the ERC Starting Grant 715049 “QCDforfuture” and the
Marie Skłodowska-Curie Innovative Training Network MCnetITN3 (grant agreement no. 722104).

References

[1] J. R. Andersen, B. Ducloué, C. Elrick, A. Maier, G. Nail and J. M. Smillie, Logarithmic
corrections to the QCD component of same-sign W-pair production for VBS studies (2021),
2107.06818.

[2] R. Covarelli, M. Pellen and M. Zaro,

raveling the electroweak sector,

the LHC: Un-
Int. J. Mod. Phys. A 36(16), 2130009 (2021),

Vector-Boson scattering at

5

pp→(W→eνe)(W→µνµ)+jetsLHC@13TeVanti-kt,R=0.4,pj;⊥>50GeV,|ηj|<4.710−610−510−410−3dσdpj1;⊥[fb/GeV]NLOHEJ2004006008001000pj1;⊥[GeV]0.00.51.01.5RatiotoNLOpp→(W→eνe)(W→µνµ)+jetsLHC@13TeVanti-kt,R=0.4,pj;⊥>50GeV,|ηj|<4.70.050.100.150.200.250.300.35dσdze[fb]NLOHEJ0.00.10.20.30.40.50.60.7ze0.60.81.01.21.4RatiotoNLOSciPost Physics

Submission

doi:10.1142/S0217751X2130009X, 2102.10991.

[3] M. Aaboud et al., Observation of electroweak production of a same-sign W boson pair in
(cid:112)
s = 13 TeV with the ATLAS detector, Phys. Rev.

association with two jets in pp collisions at
Lett. 123(16), 161801 (2019), doi:10.1103/PhysRevLett.123.161801, 1906.03203.

[4] A. M. Sirunyan et al., Measurements of production cross sections of WZ and same-sign WW
s = 13 TeV, Phys. Lett.

boson pairs in association with two jets in proton-proton collisions at
B 809, 135710 (2020), doi:10.1016/j.physletb.2020.135710, 2005.01173.

(cid:112)

[5] A. M. Sirunyan et al., Measurements of production cross sections of polarized same-sign W
s = 13 TeV, Phys. Lett.

boson pairs in association with two jets in proton-proton collisions at
B 812, 136018 (2021), doi:10.1016/j.physletb.2020.136018, 2009.09429.

(cid:112)

[6] J. R. Andersen, T. Hapola and J. M. Smillie, W Plus Multiple Jets at the LHC with High Energy

Jets, JHEP 1209, 047 (2012), doi:10.1007/JHEP09(2012)047, 1206.6763.

[7] J. R. Andersen, J. A. Black, H. M. Brooks, E. P. Byrne, A. Maier and J. M. Smillie, Combined
subleading high-energy logarithms and NLO accuracy for W production in association with
multiple jets, JHEP 04, 105 (2021), doi:10.1007/JHEP04(2021)105, 2012.10310.

[8] J. R. Andersen and J. M. Smillie, Constructing All-Order Corrections to Multi-Jet Rates, JHEP

1001, 039 (2010), doi:10.1007/JHEP01(2010)039, 0908.2786.

[9] J. R. Andersen, T. Hapola, M. Heil, A. Maier and J. M. Smillie,

Dijets: Higher-Order Matching for High-Energy Predictions,
doi:10.1007/JHEP08(2018)090, 1805.04446.

Higgs-boson plus
JHEP 08, 090 (2018),

[10] J. R. Andersen, T. Hapola, M. Heil, A. Maier and J. Smillie, HEJ 2: High Energy Resummation
for Hadron Colliders, Comput.Phys.Commun. 245 (2019), doi:10.1016/j.cpc.2019.06.022,
1902.08430.

[11] E. Bothmann et al., Event Generation with Sherpa 2.2, SciPost Phys. 7(3), 034 (2019),

doi:10.21468/SciPostPhys.7.3.034, 1905.09127.

[12] D. L. Rainwater, R. Szalapski and D. Zeppenfeld, Probing color singlet exchange in Z + two
jet events at the CERN LHC, Phys. Rev. D 54, 6680 (1996), doi:10.1103/PhysRevD.54.6680,
hep-ph/9605444.

[13] F. Buccioni, S. Pozzorini and M. Zoller, On-the-ﬂy reduction of open loops, Eur. Phys. J. C

78(1), 70 (2018), doi:10.1140/epjc/s10052-018-5562-1, 1710.11452.

[14] The GridPP Collaboration, GridPP: Development of the UK Computing Grid for Particle Physics,

J. Phys. G 32, N1 (2006), doi:10.1088/0954-3899/32/1/N01.

[15] D. Britton et al., GridPP: the UK grid for particle physics, Phil. Trans. R. Soc. A 367, 2447

(2009), doi:10.1098/rsta.2009.0036.

6

