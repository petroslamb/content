The Birth of Quantum Mechanics: A
Historical Study Through the Canonical
Papers
Eren Volkan K¨ u¸ c¨ uk
Department of Physics and Astronomy, Universit¨ at Heidelberg
Heidelberg, Germany
eren.kucuk@stud.uni-heidelberg.de
Abstract
This paper explores the historical development of the theory of
quantum mechanics between 1900 and 1927 by chronological exami-
nation of the foundational papers and ideas. Beginning with Planck’s
introduction of energy quantisation in blackbody radiation, we follow
the emergence of Einstein’s light quanta hypothesis, Bohr’s atomic
model, and the statistical implications of indistinguishable particles.
Special emphasis is placed on the transition from the Old Quantum
Theory to modern quantum mechanics, particularly through Heisen-
berg’s matrix mechanics and Schr¨ odinger’s wave mechanics. This
study aims to provide a structured historical account, offering insights
into the conceptual transformations that led to quantum mechanics
while making the development accessible to physicists, historians of
science, and advanced students interested in the origins of modern
quantum theory.
Keywords: history of physics, quantum theory, matrix mechanics,
wave mechanics.
1 Introduction
The development of quantum physics stands as one of the most profound
revolutions in the history of science. Before the advent of quantum theory,
1
arXiv:2503.13630v4  [physics.hist-ph]  14 Aug 2025

classical physics, governed by Newtonian mechanics and Maxwell’s electro-
dynamics, was considered to provide a complete description of nature. How-
ever, towards the late 19th and early 20th centuries, several inconsistencies
emerged that could not be resolved within the classical framework. One of
the most significant issues was black body radiation, where classical predic-
tions failed to match experimental observations [1–4]. Another problem was
the photoelectric effect, a detailed experimental study of which had been
done by Philip Lenard [5], which challenged the classical wave theory of
light. After Rutherford suggested his atom model [6], the stability of atoms
also posed a major dilemma since, according to classical electrodynamics,
accelerating electrons in orbit around the nucleus should continuously emit
radiation and spiral into the nucleus, contradicting the observed stability of
matter. Another problem was that the spectral lines in atomic emission and
absorption spectra exhibited some patterns that classical mechanics could
not explain (Jammer, 1989, ch.2.1). These anomalies indicated a fundamen-
tal flaw in classical theories, necessitating a new framework for understanding
microscopic phenomena. These were, in fact, the cries of a newly arriving
revolution in our understanding of the universe. This paper explores the
historical development of these theoretical concepts, tracing the key ideas
and discoveries that led to the formulation of quantum mechanics until the
development of wave mechanics and uncertainty principle.
For a physicist, a thorough understanding of the thought processes of the
minds who put these concepts forward is instrumental, if not a must, in
seeing its problems and scope and ultimately improving further on these
considerations. Therefore, the aim of this work is to present a concise history
of the development of the theory of quantum physics through the study of
the ”canonical” papers to varying degrees. This study roughly follows the
structure of Max Jammer’s seminal work, The Conceptual Development of
Quantum Mechanics [7], which provides a comprehensive historical analysis
on the subject matter. Being an immensely detailed and profound work,
which also gets into the details of many experimental studies 1 and some
1Since the goal of this study is to understand the development of theoretical ideas
2

additional philosophical discussions related to the field in comparison to the
present work, it is highly recommended for further study.
Of course, for a work of this scope, the omission of numerous significant
works was unavoidable. Throughout the work, we put special emphasis on
the papers of Heisenberg, Born, Jordan, Dirac, de Broglie, and Schr¨ odinger.
We tried to be as concise as possible and sometimes let the calculations speak
for themselves whenever the results were clear. The calculations are presented
as concisely as possible by a selection and summarisation of the ideas and
computations from the relevant pages. Since this criterion of ”relevance”
is attributed to the papers and then to the parts of the papers somewhat
subjectively by the author, they are, of course, open to criticism.
2 The Black Body Radiation
The birth of quantum theory is generally considered as Planck’s papers on
black body radiation [8, 9]. There were two equations for such an object’s
radiation’s energy density: The Rayleigh-Jeans law [3, 10] (cast in its usual
form),
u(f, T) = 8π
c2 f2kT, (1)
where 8πf 2/c2 represents the density of modes 2; and Wien’s law [2],
u(f, T) = αf3e−βf/T , (2)
where α and β are constants. These equations worked well for long and short
wavelengths, respectively, but blew up in other regimes and didn’t match up,
where the former also foresaw the so-called UV catastrophe [4]. 3 The main
rather than experiments (although the significance of which for the formation of these
ideas are not ignored) the relevant experiments were not studied in detail.
2As usual f is the frequency, and c is the speed of light in vacuum, k is the Boltzmann
constant, and T is the temperature in Kelvin scale.
3The form of the equation put forward by Rayleigh in [3], with the exponential cutoff
inserted at the end, did not pose such a problem. But Rayleigh thought of the expression
as an approximate result, which is in part theoretical and in part empirical, that worked
for large wavelengths, as he says in [3]:
3

problem was that according to classical electromagnetism and statistical me-
chanics, a black body, which is an idealised perfect absorber of any frequency
of electromagnetic radiation in thermal equilibrium (which can theoretically
be represented by radiation in a cavity with perfectly reflecting walls with a
hole [1]), the total energy of radiation was infinite according to the Rayleigh-
Jeans law. Since each distinct frequency mode of the oscillators in a black
body may radiate in totally arbitrary amplitudes, they should have had equal
average energies according to classical electrodynamics. The reason for that
was the equipartition theorem, which attained an equal amount of energy on
average for every degree of freedom of the electromagnetic field. So, for in-
finitely many frequency modes f, which all have an equal amount of average
energy, gave rise to an infinite total energy.
In 1900, Planck proposed a new expression that fit the data better [9]. In the
following paper [8], he used statistical mechanics and classical electromag-
netism to derive the formula more rigorously, and it was in that paper that
he proposed the quantisation of energy states. Planck solved the problem by
introducing energy quantisation for the field and leaving out the equiparti-
tion theorem. Thereby, oscillations of high frequency had higher energy so
that they were harder to excite or, equivalently, far less improbable for the
field to shine in. It is important to observe that Planck introduced energy
quantisation to be able to perform the calculation, which was concerned with
statistical entropy and thus with the possible arrangments of the energies of
the oscillators. That, in turn, worked as a cut-off for high frequencies, and
UV catastrophe was eliminated.
...The suggestion is that (4) rather than, as according to (2),
λ−5 dλ
may be the proper form when λθ [θ is the temperature] is great. If we
introduce the exponential factor, the complete expression will be
c1θλ−4e−c2/λθdλ.
In his 1905 paper [11], which is the topic of the next section, Einstein stated that the
classical theory inevitably leads to the Rayleigh-Jeans law (without the empirically inserted
cutoff) and showed that it blows up in high frequencies. For more information, see [12].
4

From statistical mechanics, the partition function for a single mode f for the
continuous energy levels is
Z =
X
n
e−βE(fn) ≈
Z ∞
0
e−βE dE = 1/β, (3)
where fn represents the discrete frequency mode for the standing waves of
the cavity, representing the black body (note that β is not a constant this
time). The average energy for a mode is,
E = − 1
Z
∂Z
∂β = 1/β = kT, (4)
(as equipartition of energy foresees) and since there are an infinite number
of modes (frequencies), the total energy is infinite.
If one assumes that energy levels of a modefn are dependent on the frequency
as Em,n = mhfn just as Planck did, where m ∈ N, the partition function is
Z =
X
m
e−βEm(fn) =
X
m
e−βmhfn = 1
1 − e−βhfn
. (5)
In that case, for high f, the probability for higher energy states exponentially
diminishes. Therefore, the average energy per mode is
E = − 1
Z
∂Z
∂β = hfn
eβhfn − 1. (6)
Since the energy density of states is represented by 8πf 2/c2, the total energy
is
Etot =
Z ∞
0
8πf 2
c2 E(f, T)d f= 8π
c2
Z ∞
0
hf3
eβhf − 1d f= σT 4 (7)
which is the Stefan-Boltzmann law.
One can observe that Rayleigh-Jeans and Wien’s laws are short and long-
wavelength regimes approximations of Planck’s law. For low frequencies
hf/kT ) << 1,
eβhf − 1 ≈ 1 + hf/kT ) − 1 =⇒ u = 8π
c2 f2kT ; (8)
whereas for hf/kT ) >> 1,
u(f, T) = 8πf 2
c2 hfe−f/kT ), (9)
where α = 8πh/c2, and β = 1/k.
5

3 Einstein’s Paper on Radiation Quanta
The work of Planck marked the entry of quantum concepts into mainstream
physics. The next step of great significance was Einstein’s theory of radi-
ation quanta and the explanation of the photoelectric effect [11], published
in the same year as his two other significant works on Brownian motion 4,
and special relativity. The main problem which led Einstein to the following
considerations was the apparent inconsistency of the concepts of discreteness
of energy states, whereas the radiation itself was still considered continuous
through classical electrodynamics. He also showed that the classical consid-
erations inevitably led to the Rayleigh-Jeans law, without the exponential
cutoff, which resulted in the UV-catastrophe presented in the previous sec-
tion.
Einstein started his contemplations by stating that the entropy of the radi-
ation in the cavity can be represented as a function of the radiation density,
uν, and ν:
S = V
Z ∞
0
φ(u, ν)dν, (10)
where V is the volume of the cavity. Considering that energy is conserved
and entropy is at its maximum,
δ
Z
φdν = 0,
δ
Z
udν = 0.
(11)
Therefore,
Z ∂φ
∂u δudν = λ
Z
δudν =⇒
Z ∂φ
∂u − λ

δudν = 0. (12)
Since this equality has to hold for any variation of u,
∂φ
∂u = λ, (13)
4This work of Einstein, although not directly related to the development of quantum
mechanics, since posed a proof of the existence of atoms, it seemed relevant to study it in
an appendix. Therefore, for more information on the paper, see the first appendix.
6

which means, ∂φ
∂u is independent of ν. The differential entropy is
S =
Z ∞
0
∂φ
∂u dudν, (14)
for V = 1. Since the derivative is independent of ν, as we have shown, we
have
dS = ∂φ
∂u dE = T−1dE, (15)
where the last inequality is valid for reversible systems.
Wien’s radiation law, which is valid for large values of ν, states
uν = αν3e−β ν
T =⇒ T−1 = ∂uφ = − 1
βν ln ρ
αν3 . (16)
By direct integration, we get
φ = − ρ
βν

ln ρ
αν3 − 1

. (17)
For a radiation in volume V and frequency range ν + dν,
S = V φdν= −V ρdν
βν

ln V ρdν
V αν3dν − 1

. (18)
Since the energy density scales as ρ ∝ 1/V , energy V ρdνstays constant if
we change the volume reversibly to V0. The entropy difference in this case is
S −S0 = − E
βν

ln E
V αν3dν − 1

+ E
βν

ln E
V0αν3dν + 1

= E
βν ln V0
V . (19)
This is just the entropy change for an ideal gas, which is the first sign that ra-
diation behaves like particles in this case. Afterwards, Einstein this time used
the statistical model of entropy (before which he used the thermodynamical
one),
S = k ln W. (20)
He thought a volume of n particles that don’t interact with each other (so
that ”the radiation may be considered as the most disordered process imag-
inable”). For the same process, the entropy difference gives
S − S0 = k ln
V
V0
n
= nk ln
V
V0

. (21)
7

Comparing this to (19), it can be seen that we must have
nk = n R
N = E
βν =⇒= E/n = Rβν
N , (22)
which is the energy per radiation quanta of frequency ν within the range
of validity of Wien’s radiation formula. Afterwards, he showed that the
photoelectric effect is explained by these results.
Lastly, we have to mention a nuance: Notice that what Planck suggested is
the quantisation of energy, whereas Einstein’s is the quantisation of electro-
magnetic waves directly. Einstein thought that classical electrodynamics was
an approximation of many light quanta and sufficiently long time intervals.
He saw the irreconcilability of Planck’s law, which he took for granted, and
classical electrodynamics, whereas Planck did not accept the idea of quanta
of radiation. Planck viewed quantisation as a mathematical convenience,
whereas Einstein argued that light itself is quantised, laying the foundation
for quantum mechanics. Therefore, the concept of quanta became a topic of
discussion firstly as a mathematical convenience and/or as the atom of light.
4 Emergence of the Old Quantum Theory
Both Einstein’s and Planck’s papers stimulated a discussion in the physics
community. The concept of quanta has taken place in many papers in the
succeeding years, some of which are chosen to be discussed in this section.
In 1911, Ehrenfest and Kamerlingh considered the statistical mechanics of
quantised radiation, showing that the statistical behaviour of distinguishable
quanta leads to the Rayleigh-Jeans formula, while indistinguishable quanta
result in the form of Planck’s radiation law. They showed that for N unit
volumes and P quanta, if the quanta are distinguishable as in Einstein’s
conception, we have
W1/W2 = NP
1 /NP
2 , (23)
which leads to the Rayleigh-Jeans formula; whereas if the quanta are indis-
8

tinguishable, as in Planck’s theory 5, we have
W1/W2 =
N1 − 1 + P
P

/
N2 − 1 + P
P

, (24)
which leads to Planck’s law of radiation [15]. Today, we understand that
the discrepancy arises because photons, like all bosons, are indistinguish-
able particles. Thus, Planck’s formula correctly accounts for their quantum
statistics. However, at the time, the concept of indistinguishable quantum
particles had not yet been fully developed. Although their work did not yet
formulate Bose-Einstein statistics, it foreshadowed the necessity of treating
quantum particles as indistinguishable; an idea later formalised by Bose and
Einstein in the 1920s [14].
The same year, in the first Solvay Conference, Planck contributed with a
paper [16] in which he proposed the idea that h was the quantum of action.
The consideration is as follows: Planck started with the classical theory of
Gibbs, that the probability of finding the system in the state corresponding
to the element dpdq in phase space was
e−βE dpdqR
e−βE dpdq. (25)
For the harmonic oscillator, the calculation yields the famous result kT .
Planck, then, stated that if we postulate that E can only take on discrete
values E = nϵ, the calculation yields
U = ϵ
eβϵ − 1. (26)
Therefore, Planck made the statement that not only the average energy of the
oscillators is determined with respect to the preceding result, but directly the
energy itself of the oscillators at any moment can take on the energy values
according to it. According to these considerations, Planck proposed that
5Of course, although Planck did introduce the concept of quantised energy levels, he
did not initially interpret radiation itself as being composed of quanta. Later, the papers
of Bose and Einstein showed that treating radiation as a gas of indistinguishable quanta
(photons) naturally leads to the same distribution that Planck had derived through dif-
ferent means [13, 14].
9

h is the finite extension of the elementary area in phase space. Therefore,
the subsequent ellipses in the phase space of the harmonic oscillator (the
trajectories) have a difference of area
Z E+ϵ
E
dpdq = h, (27)
or equivalently, all ellipses enclose an area of
Z
dpdq = nh. (28)
Therefore, he rendered the idea of the ”quanta of the phase space” more
fundamental than the idea of energy quanta, which he then considered to be
only a consequence of the postulate. Thus, the problems of quantum me-
chanics were to be solved by first solving the problem classically and then
applying the quantum of action condition. This postulate was to become
one of the cornerstones of the Old Quantum Theory and, as we will see, be
included implicitly in the foundations of matrix mechanics. It is also inter-
esting to note that Planck started his account by stating that the framework
of classical mechanics is too narrow to take into account the phenomena that
are outside of our ”coarse senses” . 6 Here, we observe that the concept of
quanta has taken a more fundamental place than it had before.
In the subsequent year, Poincare proved that the only way to achieve a
radiation law of finite total energy was through the concept of quanta [17].
The general idea is summarised as follows (Prentis, 1995, p.340):
The global structure of the memoir is as follows. Poincar´ e be-
gins with a physical model consisting of a system of Hertzian res-
onators interacting with a system of atoms. The atoms, by virtue
of their collisions with the resonators, mediate the exchange of
energy between the resonators. For both physical reasons and
6From [16], p.93: ”Nous devons reconnaˆ ıtre aujourd’hui que cette esp´ erance n’´ etait pas
justifi´ ee et que le cadre de la Dynamique classique, mˆ eme en tenant compte de l’extension
apport´ ee par le principe de relativit´ e de Lorentz-Einstein, est trop ´ etroit pour contenir les
ph´ enom` enes physiques non directement accessibles ` a nos moyens grossiers de perception.”
10

mathematical rigour, Poincare felt that it was necessary to clearly
understand how a unique thermodynamic equilibrium state could
emerge from an explicit consideration of some mechanism of inter-
action between the resonators. He felt that the other theoretical
studies of blackbody radiation were flawed because they neglected
such an interaction, and their arguments included too many as-
sumptions related to the existence of equilibrium. He focuses on
the partition of energy between the resonators and the atoms in
thermal equilibrium. Poincar´ e’s clever choice to study the parti-
tion of energy allows him to avoid the usual arguments based on
entropy, temperature, and other equilibrium concepts. From his
formulation of statistical mechanics, Poincar´ e is able to relate this
macroscopic partition of energy to the microscopic dynamical be-
haviour of a resonator. Having established this basic micro-macro
connection, he then determines what kind of constraint must be
imposed on the motion (energetics) of the resonators in order
to account for the observed partition of energy (radiation law).
In three separate proofs, Poincar´ e discovers that this dynamical
constraint is precisely the hypothesis of quanta.
4.1 Bohr’s Quantization of States in Atoms
The next year, Niels Bohr, at the time still a young researcher, published a
paper which was concerned primarily with the structure and spectrum of the
hydrogen atom. According to the results of Rutherford [6], electrons were
scattered around the positively charged nucleus. 7 Yet the laws of classical
electrodynamics dictate that in such a system, electrons should radiate all
their energy while spiralling down into the nucleus, wherefore there is no
classical stable solution for such a system. To get rid of this problem, and
taking inspiration from the regularities in the hydrogen spectrum which is
7It turns out that Rutherford did not really suggest an ”atom model”, yet merely stated
that there is a positively charged nucleus, without really touching upon how electrons move
about it. For a discussion on the misconception on the atom models, see the discussion of
Renstrøm and Bomark (2022) [arXiv:2212.08572].
11

made explicit by Balmer’s formula, he applied Planck’s quantization to the
orbits and postulated that there are stationary states around the nucleus
[18].8 In these discrete orbitals, the motion of the electron was governed by
classical physics, but the transitions between the states were not, but occur
as jumps between the discrete orbits. The theory was successful in explaining
the spectra of the hydrogen atom, and mono-electronic ions in general, but
the theory struggled to account for more complex systems.
One of the most consulted principles, the correspondence principle as it is
called later, in the Old Quantum Theory, which signifies the state of the
theory before the next leap of understanding with primarily Heisenberg, de
Broglie, and Schr¨ odinger, was stated in the same paper. According to the
results, the ratio of the frequency of revolution of the electron in subsequent
orbits converges to 1 as the orbital number increases. In his later paper in
1918, Bohr stated the principle more explicitly (Bohr, 1918):
We shall show, however, that the conditions which will be used
to determine the values of the energy in the stationary states are
of such a type that the frequencies calculated by (1), in the limit
where the motions in successive stationary states comparatively
differ very little from each other, will tend to coincide with the
frequencies to be expected on the ordinary theory of radiation
from the motion of the system in the stationary states. 9
So, for large quantum numbers, the radiation is expected to obey the results
of classical electrodynamics. Bohr’s correspondence principle was crucial
because it ensured that quantum mechanics would reproduce classical results
in the limit of large quantum numbers, providing a bridge between old and
new physics.
Later, Born suggested that the transition between classical to quantum me-
8Before him, Planck’s postulate had been applied to the oscillation of the electrons in
the atom model of J.J. Thomson. See [7], p.75.
9The translation is from [19], p.10.
12

chanical equations can be achieved by replacing differentials with difference
equations according to the rule [20],
τ ∂Φ(n, τ)
∂n ↔ Φn+τ,n − Φn,n−τ . (29)
This follows from the following logic: The transition frequency from n to
n′ = n − τ coincides with the τth harmonic of the classical motion in state n
for large n, that is
νn,n−τ = ν(n, τ) = τν (n, 1) = τν, (30)
where, in Jacobi-Hamilton formulation, in terms of action-angle variables, 10
we also have
∂H
∂J = ν. (31)
Now, since J = nh, this equation becomes
ν(n, τ) = τ ∂H
∂J = τ
h
∂H
∂n = ν. (32)
Since we also have
νn,n−τ = H(nh) − H([n − τ]h)
h , (33)
for an arbitrary function of stationary states Φ( n, τ), we have the relation
(29).
4.2 Sommerfeld’s Elaborations of Bohr’s and Planck’s
Results
Later, in 1915, Sommerfeld derived the results of Bohr using the quantum
of action for three degrees of freedom of the electron [21, 22], for which the
equations I
prdr = nrh,
I
pθdθ = nθh,
I
pϕdϕ = nϕh, (34)
should hold. He studied the problem relativistically, and derived the rela-
tivistic correction to the spectrum of the hydrogen atom,
Enk = −Z2Rhc
 1
n2
α2Z2
n4
n
k − 3
4

, (35)
10See section B.2 in the appendix.
13

where n = nr + nϕ, Z is the atom number, and R is the Rydberg constant.
This formula accounted for the energy splitting of the spectral lines and
yielded the fine structure of the hydrogen atom, which is
α = 2πe2
hc . (36)
Despite their partial success, these considerations did not save the quantum
theory from its inconsistencies. As Jammer puts it, the theory at that state
was ”a lamentable hodgepodge of hypotheses, principles, theorems, and com-
putational recipes rather than a logically consistent theory,” (Jammer, 1966,
p.208). The general method for solving a problem was first solving it classi-
cally, and then applying the ”principles”, as correspondance or quantum of
action principle, applications of which most of the time asked for educated
guesses. In short, the theory needed a logically consistent framework.
The lack of a consistent, logically sound framework in the Old Quantum The-
ory prompted Heisenberg to seek a new foundation for quantum mechanics,
one based not on classical analogies (which were primarily concerned with
unobservable properties of the systems such as position and velocity) but
on directly observable quantities. Instead of these concepts, he insisted on
placing at the core of the theory what he called the observable variables like
energy and frequency, from which arise the so-called matrix mechanics [23].
5 Matrix Mechanics
Throughout the paper, Heisenberg has in mind an electron in an atom which
undergoes periodic motion. A time-dependent quantity xn(t), related to the
electron in the nth state, can be expressed as a Fourier series in classical
physics as
xn(t) =
+∞X
τ=−∞
x(n, τ) =
+∞X
τ=−∞
x(n, τ) exp [2πiν(n, τ)t], (37)
where τth component has the frequency ν(n, τ) = τν (n, 1). So it follows that
ν(n, τ) + ν(n, τ′) = ν(n, τ+ τ′). (38)
14

The quantum mechanical analogue to this is
νn,n−τ′ + νn−τ′,n−τ = νn,n−τ , (39)
which follows from Bohr’s postulates. By the correspondence principle, since
a quantum theoretic frequency is related to the classical frequency as
ν(n, τ) ↔ νn,n−τ . (40)
At that point, he argued that the corresponding amplitude in the quantum
case should be
x(n, τ) ↔ xn,n−τ . (41)
Then the set {xn,n−τ exp [2πiνn,n−τ t]} may be chosen as the representative of
xn(t) in the quantum case. Now, in the classical case
xn(t)2 =
"X
τ
x(n, τ) exp [2πiν(n, τ)t]
#"X
τ′
x(n, τ′) exp [2πiν(n, τ′)t]
#
=
X
ττ ′
x(n, τ)x(n, τ′) exp [2πiν(n, τ+ τ′)t]
(42)
by (38). By changing variables as τ → τ − τ′, we get
+∞X
τ=−∞
x2(n, τ) exp [2πiν(n, τ)t], (43)
where
x2(n, τ) =
+∞X
τ′=−∞
x(n, τ′)x(n, τ− τ′). (44)
Therefore, according to (39), the corresponding quantum quantity must be
x2
n(t) ↔ {x2
n,n−τ exp [2πiνn,n−τ t]}. (45)
To get the correct phase factor, one must replace the terms like n, n− τ′ ×
n, n− (τ − τ′) by n, n− tau′ × n − τ′, n− τ. Accordingly, we have
x2
n,n−τ =
X
τ′
xn,n−τ′xn−τ′,n−τ . (46)
15

The generalization of this rule as xn(t)ηn yields a noncommutative algebra,
since, in general
X
τ′
xn,n−τ′yn−τ′,n−τ ̸=
X
τ′
yn,n−τ′xn−τ′,n−τ . (47)
As it was said in earlier chapters, in the old theory, to solve the quantum
problems, one had had to first calculate the equation of motion classically
and then impose the quantum of action condition
I
pdq = nh, (48)
which worked for some basic problems but was hard to work out for most
others. So, for a generic equation of motion ¨ x + f(x) = 0, p = m ˙x, and by
the correspondence principle
τ ∂Φ(n, τ)
∂n ↔ Φn+τ,n − Φn,n−τ , (49)
Heisenberg showed that
I
pdq =
Z 1/ν
0
m ˙x2dt = 2π2m
X
τ
τν (n, τ)|x(n, τ)|2 = nh
=⇒ h = 2π2m
X
τ
τ d
dn(ν(n, τ)|x(n, τ)|2) = h
↔ 2π2m
X
τ
νn+τ,n|xn+τ,n|2 − νn,n−τ |xn,n−τ |2 = h,
(50)
where x(n, τ) = x∗(n, −τ) since xn(t) has to be real, 11 is the quantum con-
dition for such a system. Therefore, by solving the equation of motion and
applying the quantisation rule that he derived, he argued that the frequencies
and the transition amplitudes, which are observable, can be calculated from
this mathematical scheme. Afterwards, he went on to apply the scheme to
the quantum simple anharmonic oscillator. 12
11Consider the elements corresponding to τ = a and τ = −a in the sum,
x(n, a) exp [2πiν(n, a)t] + x(n, −a) exp [2πiν(n, −a)t]
=x(n, a) exp [2πiν(n, a)t] + {x(n, a) exp [2πiν(n, a)t]}∗, (51)
which real.
12The details of the derivation are not clear in Heisenberg’s paper, [23]. For a clearer
account, see [24].
16

5.1 Born and Jordan’s Contributions
It was Jordan and Born with whom Heisenberg improved the theory into
matrix mechanics [25, 26]. The two profound papers that they published in-
cluded many results, taking the theory into its full-fledged matrix mechanics
form. Starting with the quantum of action principle and by the Fourier ex-
pansions of p and q, through a similar calculation to which was just presented,
they got the canonical commutation relation.
Let
p = (p(nm)e2πiv(nm)t), q= (q(nm)e2πiν(nm)t), (52)
which are Hermitian. We also assume that the following relations hold
q(nm)q(mn) = |q(nm)|2,
ν(nm) = ν(mn),
ν(jk) + ν(kl) + ν(lj) = 0.
(53)
By using the second and third relations, we get
ν(jk) = −ν(kl) − ν(lj) = ν(jl) − ν(kl)
=⇒hν(jk) = h(ν(jl) − ν(kl)) = Wj − Wk.
(54)
Consider a matrix of the form g(pq) = ( g(nm)e2πiν(nm)t) ≡ (g(nm)). The
time derivative yields
˙g = 2πi(ν(nm)g(nm)). (55)
Since ν(nm) ̸= 0 for n ̸= m, if ˙g = 0, then g is necessarily diagonal.
Now, using (48) and (29), along with the fact that
d = pq − qp ⇒ ˙d = 0, (56)
(by another matrix theory-related result in the paper), so that the matrix d
is diagonal, we have the canonical commutation relation:
pq − qp = − ih
4πI. (57)
17

Subsequently, they also derive that
˙g = −2πi
h [g, H], (58)
and thus, for g = H, that the energy is conserved (for ∂tH = 0 of course),
which also entails the result that H is diagonal on the base which it shares
with p, q.
Soon after, Wiener and Born introduced the operator algebra into quantum
theory [27]. For y(t) = P
m yme2πiWmt/h and x(t) = P
m xn(t)e2πiWnt/h, we
have
xn(t) = lim
T→∞
1
2T
Z T
−T
x(t)e−2πiWnt/hdt, (59)
and, wherefore, the transformation ym = P
n qmnxn(t) entails the equation
y(t) = lim
T→∞
1
2T
Z T
−T
"X
mn
qmne2πi(Wmt−Wns)/h
#
x(s)ds. (60)
Writing
q = lim
T→∞
1
2T
Z T
−T
"X
mn
qmne2πi(Wmt−Wns)/h
#
| {z }
q(s,t)
ds, (61)
the former expression can be put into the form
y(t) = qx(t). (62)
As an example, direct calculation with the linear operator D = d/dt, yields
y(t) = Dqx(t) ⇒ ∂q(t, s)
∂t = 2πi
h
X
mn
qmnWme2πi(Wmt−Wns)/h. (63)
Therefore
(Dq)mn = 2πi
h qmnWm, (qD)mn = 2πi
h qmnWn
| {z }
By partial integration
=⇒ [D, q]x = 2πi
h (Wm − Wn)qmnx = 2πiνmnqmnx.
(64)
18

Hence, by definition of q in (61), the equation just derived entails
=⇒ [D, q] = ˙q.13 (65)
By (58), we also have the familiar result D = d/dt = 2πi
h H.
5.2 The Correspondance Between the Classical and
Quantum
At about the same time, the G¨ ottingen school put the matrix mechanics for-
ward, Dirac found a mathematical equivalence between classical and quan-
tum mechanics [28]. Dirac started by defining d/dv as the ”most general
operator”. By assumption, it obeys the following rules:
I.
d
dv(x + y) = dx
dv + dy
dv, (67)
II.
d(xy)
dv = xdy
dv + dx
dv y, (68)
where x, yobey the matrix product rule, (xy)mn = P
k xmkykn. Then, by the
first rule,
(Dx)mn = (dx
dt )mn ≡
X
m′n′
anm,n′m′xn′m′. (69)
Therefore, the second rule can be written as
X
n′m′k
anm,n′m′xn′kykm′ =
X
kn′k′
ank,n′k′xn′kykm′ +
X
kk′m′
xnkakm,k′m′yk′m′. (70)
Comparing the amplitudes, Dirac reduced (69) to
(dx
dv )mn =
X
k
xnkakm − ankxkm (71)
13In operator algebra, for an arbitrary function x, this equation can also be derived as
[D, q]x = d(qx)
dt − q dx
dt = dq
dt x + q dx
dt − q dx
dt = ˙qx. (66)
19

or
dx
dv = [x, a], (72)
which showed that the most general operation on a ”quantum variable” x,
subject to the rules presented at the beginning, is performed by ”taking
the difference of its Heisenberg products with some other quantum variable”
(Dirac, 1925, p.647).
To see what this equation corresponds to in classical mechanics, Dirac made
use of the correspondence principle (29), which resulted in
[x, y] ↔ ih
2π{x, y}, (73)
where
{x, y} = ∂x
∂q
∂y
∂p − ∂y
∂q
∂x
∂q (74)
is the Poisson bracket. 14 In classical mechanics, for a system described by
the set of coordinates {qi, pi}, the canonical commutation relations are
{qk, pl}qp =
X
i
∂qk
∂qi
∂pl
∂pi
− ∂qk
∂pi
∂pl
∂qi
= δkl, (79)
14Suppose f(p, q, t) is a solution to a system defined by the Hamiltonian H(p, q, t). The
chain rule reads d f
dt = ∂f
∂q
dq
dt + ∂f
∂p
dp
dt + ∂f
∂t . (75)
If the system is described by p and q s.t. they obey Hamilton’s equations
˙q = ∂H
∂p ,
˙p = −∂H
∂q ,
(76)
we have
˙f = {f, H} + ∂tH. (77)
From this, for an operatorQ, using Dirac’s correspondence principle, we get the Heisenberg
equation of motion
˙Q = 2πi
h [Q, H] + ∂tH. (78)
For more information on canonical transformations and Poisson brackets, see the second
appendix and [29].
20

where {pk, pl} = {pk, pl} = 0. Such coordinates are called canonical coor-
dinates, and the transformations that transform one canonical set of coor-
dinates to another (i.e., the coordinates which obey the canonical commu-
tation rules) are called the canonical transformations. The Poisson brackets
of canonical coordinates are invariant under these transformations, and so
are the equations of motion. The problems in quantum mechanics can be
thus reduced to finding suitable canonical coordinates (ones with the most
constants of motion) and then transforming the equations of motion using
the Dirac correspondence principle, as is shown in [25]. It is interesting to see
that the canonical transformations correspond to unitary transformations in
quantum mechanics.
In conclusion, the main mathematical connection between classical and quan-
tum mechanical equations, in the case of matrix mechanics, was the corre-
spondence principle. It was included in the main formulation of the theory
by Heisenberg and made an implicit feature by the contributions of Born
and Jordan in matrix mechanics in the equations (57) and (58). The same
principle appeared in the correspondence between the commutation relations
and Poisson brackets, as shown in (73). At that point, we can as well say
that one of the foundational postulates of quantum theory was this principle.
However, in wave mechanics, we will not see the principle in direct use. In-
stead, the main postulate of the theory will be that particles have some kind
of an ”intrinsic periodic phenomena” which causes them to act like waves.
6 Wave Mechanics
6.1 Preliminary Considerations
A significant work on the reconciliation of wave and particle phenomena was
from Hamilton, whose main concern while studying mechanics and deriving
his equations was to find a general method to explain optical phenomena, as
Lagrange did for mechanics [30].15 Yet his main interest was in mathematical
15From [30], p.5: ”Those who have meditated on the beauty and utility, in theoretical
mechanics, of the general method of Lagrange—who have felt the power and dignity of
21

laws governing both phenomena rather than a direct statement about the
corpuscular nature of light or wave nature of matter [31].
The analogy in mathematical form can be summarised as follows: The prin-
ciple equation in ray optics is Fermat’s principle of least time,
δT = δ
Z n
c ds = 0, (80)
whereas in mechanics, it is the Maupertuis’ principle of least action,
δS = δ
Z p
2m(E − U)ds, (81)
which are just special cases of Hamilton’s principle of stationary action,
δS = δ
Z
Ldt = 0, (82)
where L is the Lagrangian. This analogy can be grounded by observing that
the wave equation converges to the Eikonal equation for large wavelengths,
which is the fundamental equation of geometrical optics. The calculation is
as follows: For ψ = Aeik0W , where A and W are slowly varying functions of
position, the wave equation ∆ ψ + n2k2
0u = 0 reads
∆(Aeik0W ) + n2k2
0Aeik0W = 0. (83)
For simplicity, let’s take A and W as functions of only x. Therefore,
∂
∂x

∂xAeik0W + Aik0∂xW eik0W 
+ n2k2
0Aeik0W = 0 (84)
=⇒ ∂2
xA + ∂xA∂xW ik0 + ∂xA∂xW ik0
+ A∂2
xW ik0 − A(∂xW)2k2
0 = −n2k2
0A
(85)
that central dynamical theorem which he deduced, in the M’echanique Analytique, from
a combination of the principle of virtual velocities with the principle of D’Alembert—and
who have appreciated the simplicity and harmony which he introduced into the research
of the planetary perturbations, by the idea of the variation of parameters, and the dif-
ferentials of the disturbing function, must feel that mathematical optics can only then
attain a coordinate rank with mathematical mechanics, or with dynamical astronomy, in
beauty, power, and harmony, when it shall possess an appropriate method, and become
the unfolding of a central idea.”
22

=⇒ (∂xW)2 = n2, (86)
where we neglected the lower powers of k0 by the assumption we made.
Therefore, as geometrical optics is the long wavelength approximation of
undulatory optics, maybe the particle phenomena were just a similar ap-
proximation of the wave phenomena.
The phenomena of radiation as a wave or particle were still topics of dis-
cussion. Some phenomena, like black body radiation and the photoelectric
effect, were explained by corpuscular theory, whereas others, like refraction,
diffraction, etc., were explained by wave mechanics. It was Louis de Broglie
who first introduced the idea of associating waves with particles in the con-
text of quantum theory [32]. It seems like he wasn’t aware of Hamilton’s
optical-mechanical analogy, but he was deeply impressed by the works of
Marcel Brillouin (Jammer 1989, p.246-247).
6.2 De Broglie’s Idea of Matter-Waves
Consider a particle of rest-mass m with an intrinsic periodic motion. It has a
frequency ν0 = mc2/h at rest. Relative to an observer, for which the particle
moves with the velocity v = βc, the frequency is
ν = mc2
h
p
1 − β2
= ν0p
1 − β2
. (87)
according to its energy content. But one also expects the frequency of the
internal phenomenon to change according to time dilation as
ν1 = ν0
p
1 − β2, (88)
so, there should be a relation such that
ν1 = ν(1 − β2). (89)
The apparent discrepancy is lifted when one considers the following: Let there
be a wave with frequency ν, which spreads with the velocity c/β = c2/v, and
a particle with the intrinsic periodic phenomena coincided at t = 0, to which
23

we just ascribed the frequency ν1.16 The wave is described by the equation
sin 2πνx(1/v − β/c) after a time t, and the internal motion changes with
respect to the equation sin 2πν1x/v. Therefore,
νx(1/v − β/c)
!
= ν1x/v ⇒ ν1 = ν(1 − β2), (90)
as excepted. Therefore, ”any moving body may be accompanied by a wave
and that it is impossible to disjoin motion of body and propagation of wave”
(de Broglie, 1924, p.450). The velocity c/β is the phase velocity of the wave.
The phase velocity and group velocity are related by
1/vg = d(ν/v)/dν = 1/βc) = 1/v, (91)
so vg = v, that is, the group velocity of the wave is the velocity of the particle.
Therefore, de Broglie suggested that the wave phenomena is present when
the means of measurement is on the scale λ of the matter waves, whereas
otherwise the structure of the wave goes undisturbed and what we measure is
related to corpuscular phenomena. He also suggested that the probability of
absorption or scattering of light quanta is related to the phase wave vectors
crossing upon the atom.
One of the results that de Broglie proposed was that the Sommerfeld quantum
condition
H
pdq = nh, along with λ = h/p is equivalent to
I
λ−1dq = n, (92)
which states that the (monochromatic) wavelength of the electron in an
orbit is quantised as 2 πr/n, resembling the solution of a boundary value
problem, attracted the interest of Schr¨ odinger deeply. That was also the
wave-mechanical explanation of Bohr’s quantum condition of discrete angu-
lar momentum of the electron in the orbits.
16The reason why frequencies are ascribed such that can be seen by the fact that the
first one satisfies the Doppler effect.
24

6.3 The Wave Equation
Thinking that if there are waves, there should also be a wave equation,
Schr¨ odinger began his study on de Broglie’s matter waves for bound particles.
He thought that for resolutions much higher than the associated wavelength
λ = h/p, just as in geometrical optics, the wavelike phenomena were not
possible to observe, whereas, in the high resolutions, i.e. where the inter-
action distances d between the particles were d ≈ λ, the wavelike nature of
the matter was significant to the behaviour of the system, just as in undula-
tory optics. So, just as de Broglie thought, he showed that there was more
to the resemblance between the analogy with geometrical-undulatory optics
and that of the particle-wave nature of the matter [33].
One of the works that impressed Schr¨ odinger the most was the papers of
Einstein on the ideal gas, where he used Bose’s counting procedure [34],
which renders the particles indistinguishable and thus arranges them in the
possible energy states according to the Ehrenfest and Krammling’s combi-
natoric expression, to arrive at Planck’s formula without the use of classical
electrodynamics, contrary to the way Planck derived it [13, 14]. Schr¨ odinger
saw that the wave concept presented a natural way to account for the phe-
nomenon [31].
Schr¨ odinger published four papers (and a paper to summarise the results)
where he studied the form of the wave equation and applied it successfully
to the problems of quantum mechanics [33, 35–38]. 17 He started his first
communication [35] by proposing that in the time-independent Hamilton
equation (since he was dealing with stationary states in the Hydrogen atom),
H(q, ∂W
∂q ) = E. (93)
Hamilton’s characteristic function W is completely separable for orthogonal
coordinates and quadratic (in the generalised momenta) Hamiltonians with
17His works assumes some knowledge on Hamilton-Jacobi formulation of classical me-
chanics, a summary of which can be found in the second appendix.
25

no time dependence if the potential energy is additively separable in each
coordinate.18 Therefore, he assumed
W =
X
i
Wi(qi; ∂q1 W, . . . , ∂qnW) ≡ K ln
 Y
j
ψ(qj)
!
= K ln ψ, (94)
=⇒ H

q, K
ψ
∂ψ
∂q

= E. (95)
where K is a constant, and ψ are single-valued functions of only one of the co-
ordinates qj, which are real (this condition is lifted in the subsequent papers).
In simple cases, this equation can be written in quadratic form equated to
zero. In this case, ψ also has to be twice continuously differentiable, for which
the first derivative is equal to zero for the equation to be quadratic, which
extremizes the corresponding integral equation. 19 Therefore, he effectively
changed the quantum conditions with the conditions on ψ.20
In cartesian coordinates, where e, mare the electron’s mass and charge, ac-
cording to our considerations in the second appendix, the Hamilton-Jacobi
18See the second appendix, section B.1.
19The last condition is rather arbitrary, as Schr¨ odinger will also give in in his second
communication, but surprisingly leads to the correct answer, the reason of which will be
given in the subsequent pages. The motivation behind this rather ad hoc principle was
argued to be related to optical-mechanical analogy (Joas, Lehner, 2007, p.13):
After several unsuccessful attempts at guessing the variational principle,
there appears in the notebook a program that contains as its second item
”the old Hamiltonian analogy between optics and mechanics”. In the text
corresponding to this item, Schrodinger starts from the Hamiltonian par-
tial differential equation and reinterprets it as a variational principle which
indeed leads him to the (nonrelativistic) wave equation.
20From [35], p.1: ”Wir suchen nun nicht eine L¨ osung der Gleichung (95), sondern wir
stellen folgende Forderung. Gleichung (95) l¨ asst sich bei Vernachl¨ assigung der Massen-
ver¨ anderlichkeit stets, bei Ber¨ ucksichtigung derselben wenigstens dann, wenn es sich um
das Einelektronenproblem handelt, auf die Gestalt bringen: quadratische Form von ψ und
seinen ersten Ableitungen = 0. Wir suchen solche reelle, im ganzen Konfigurationsraum
eindeutige, endliche und zweimal stetig differenzierbare Funktionenψ, welche das ¨ uber den
ganzen Konfigurationsraum erstreckte Integral der eben genannten quadratischen Form zu
einem Extremum machen. Durch dieses Variationsproblem ersetzen wir die Quantenbe-
dingungen.”
26

equation takes the form
3X
i=1
p2
i
2m + V (x, y, z) = K2
2m
3X
i=1
1
ψ
∂ψ
∂qi
2
− e2
r = E (96)
=⇒
3X
i=1
∂ψ
∂qi
2
− 2m
K2

E + e2
r

ψ2 = 0, (97)
where r =
p
x2 + y2 + z2, and K
ψ
∂ψ
∂qi
= pi by (159). Therefore, our variation
problem becomes
δJ = δ
Z +∞
−∞
d3q
3X
i=1
∂ψ
∂qi
2
− 2m
K2

E + e2
r

ψ2 = 0, (98)
from which we get the following equations,
∆ψ + 2m
K2

E + e2
r

ψ = 0,
Z
d fδψ∂ψ
∂n = 0,
(99)
of which the first is the Schr¨ odinger equation for an electron in the hydrogen
atom, and the second, where d fis the surface element of a surface of infinite
extent, is the condition that the wavefunction must go to zero at infinity. 21
21In reference [39], there is an account which explains how this variational principle
works by means of statistical considerations. The number of states in an imaginary en-
semble in the configuration space, which is encoded by the ”field” W, is
N =
Z
ρ(qi, )dq1 . . . dqn, (100)
for n degrees of freedom, and ρ(qi, t) is the density of states in the ensemble. Now, if we
apply the normalisation condition, N = 1, then we have a probability distribution, and
we can define the probability of finding the system at the state qi as
P(qi, t) = ρ(qi, t)R
ρ(qi, )dq1 . . . dqn
= ρ(qi, t). (101)
The evolution of the probability distribution is given by the continuity equation,
∂ρ
∂t + ∇ ·

ρ∇W
m

= 0. (102)
Later in the paper, they state that the statistical Hamilton-Jacoby theory, as they call it,
27

Therefore, Schr¨ odinger reduced to problem of finding the energy levels of the
electron in the hydrogen atom to a boundary value problem for negative E,
i.e., bound states. For positive E, which classically corresponds to hyperbolic
solutions of the Kepler problem, there are no bound states as the electron is
not bounded by the potential. For bound states, he showed that quantisation
naturally occurred whenever
n = me2
K
√
−2mE (105)
is a real positive integer, to give energy eigenvalues of
E = − me4
2K2n2 , (106)
which provides the Bohr energy levels for K = h/2π.
At the beginning of the second communication [36], Schr¨ odinger gives another
means of derivation for the wave equation, as the ansatz (94) and the vari-
ational principle he postulated were ”unintelligible” (unverst¨ andlich). This
time, he explicitly uses the optical-mechanical analogy:
Maybe our classical mechanics is the full analogue of geometri-
cal optics, and, as such, wrong, not in agreement with reality.
It fails as soon as the radii of curvature and the dimensions of
the trajectory are not large anymore compared to a certain wave-
length, to which one can attribute a certain reality in q-space. In
that case, one has to search for an ”undulatory mechanics”—and
can be summarised by the following variational principle,
δ
Z
dq1 . . . dqn ρ
∂W
∂t + H

qi, ∂W
∂qi

= 0, (103)
by treating ρ and W as conjugate variables. The Hamilton-Jacobi equation and the
continuity equation are then derived from this variational principle. It can be seen, upon
comparison, that this variational principle is in the same form as Schr¨ odinger’s variational
principle, for ρ = |ψ|2. By the ansatz W = K ln ψ, we have
ψ = √ρeW/K , (104)
where K has to be an imaginary number to satisfy ρ = |ψ|2.
28

the obvious way to this end is the wave theoretical extension of
Hamilton’s picture. (Schrodinger, [36], pp. 25) 22
For a conservative system, the action is
S =
Z
T − Udt, (107)
and we have the equation
∂S
∂t + 1
2m|∇S|2 + U = 0. (108)
Substituting the usual ansatz
S(qi, t) = −Et + W(qi), (109)
in the equation (108), and by using the fact that |∇S| = |⃗P| = P, we get
|∇S| =
p
2m(E − U), ∂tS = −E, (110)
from which follows, for constant action,
dS =|∇S|ds + ∂tSdt = (V |∇S| −E)dt = 0
=⇒ V = E
|∇S| = Ep
2m(E − U)
, (111)
where V is the phase velocity of the waves. On the other hand, the velocity
of the particle is
|∇S|/m = P/m = v =
p
2(E − U)/m. (112)
Therefore, he showed the equivalence of Fermat’s and Maupertuis’ principle:
δ
Z
ds/V = δ
Z
ds
p
2m(E − U)/E = δ
Z
vdt
p
2m(E − U)/E
= δ
Z
2(E − U)/Edt = 0 =⇒ δ
Z
2T dt= 0.
(113)
Afterwards, he introduced the waves
ψ = A(x, y, z) sin(W/K), (114)
22Translation is from [31], p.15.
29

where K is a constant with the units of action. In this case, the frequency is
ν = E
2πK , (115)
which yields the relation of Einstein for K = h/2π. The associated wave-
length is given as
λ = v/ν = h/
p
2m(E − U) = h/p. (116)
(Note that the equality of particle velocity and the group velocity of the wave
does also hold, as we have seen in de Broglie’s papers.) Next, he introduced
the ordinary wave equation
∆Ψ −
¨Ψ
V 2 = 0, (117)
with the condition that
Ψ(q, t) = ψ(q)e2πiEt/h, (118)
he got the wave equation23:
∆ψ + 8π2m
h2 (E − U)ψ = 0. (124)
23In Atombau und Spektrallinien, [40], Sommerfeld used the optical-mechanical analogy
to derive Schr¨ odinger’s equation as follows. Starting with the equation
1
2m(p2
x + p2
y + p2
z) = E − V = |∇S|2
2m , (119)
where S is Hamilton’s principle function, and compared it with the wave equation
∆u = 1
v2
∂2u
∂t2 . (120)
Next, we use the ansatz u = ψeiωt, where ω = k/v, and k = nk0, where k0 is the
wavelength in the vacuum and n = c/v is the refractive index. Therefore we get
∆ψ + n2k2
0ψ = 0. (121)
Next, he shows the approximate relation between this equation and the Eikonal equation,
as it is done in preceding pages (instead of W, he uses S). Therefore, by the relations
|∆S|2 = 2m(E − V ), |∆S|2 = n2, (122)
we get
∆ψ + 2m(E − V )k2
0ψ = 0. (123)
But in the first equation, S is dimensionless, whereas in the second one, it has dimensions
of energy and mass. The equality of dimensions is retrieved once we state k0 = (2π/h)2.
30

This derivation of the wave equation is what he also preferred in [33].
In the third communication [37], of which we will not delve into the details,
he developed the time-independent perturbation theory and applied it to
calculate the Stark effect of the hydrogen atom.
In the last paper of the series [38], the fourth communication, he developed
the time-dependent perturbation theory for non-conservative systems. Of
course, to do that, he needed the time-dependent wave equation, as the wave
equation derived and used until now was for conservative systems, especially
for the case of the stationary states of the electron in the hydrogen atom.
For time-dependent potentials, the theory had to be extended. To do that,
Schr¨ odinger observed that
− ih
2π∂tΨ = EΨ, (125)
and postulated that the equation
− h2
8π2m∇2Ψ + UΨ = −ih
2π
∂Ψ
∂t . (126)
For that matter, he also lifted the reality condition on ψ.24
Although Schr¨ odinger believed in the literal existence of matter waves, the
wave function that he got was not suitable for such tangible existence, for it
was not defined in 3-dimensions. For a system of N particles, it is defined
on the 3N-dimensional configuration space.
Schr¨ odinger’s idea of the primacy of waves over particles did not become
a consensus. In 1926, just after Schr¨ odinger published his papers on wave
24As expected, it is possible to derive Hamilton-Jacobi equation as a classical approx-
imation of this equation, by letting ψ = √ρ exp iS(x, t)/ℏ, where ℏ = h/2π, substituting
that into the Schr¨ odinger equation, and then taking the limitℏ → 0, which gives
1
2m
∂S
∂x
2
+ V (x) + ∂S
∂t = 0, (127)
in one dimension.
31

mechanics, Born suggested his statistical interpretation of the wave function
in his studies on the scattering theory [41, 42]. Schr¨ odinger strongly re-
sisted Born’s interpretation, believing that wave mechanics should describe
real physical waves rather than probabilities. However, the success of the
probabilistic interpretation in scattering experiments ultimately led to its
acceptance and continued to defend his position throughout his life.
7 Uncertainty Principle, Indistinguishability,
and Complementarity
Although the formal language of quantum theory was slowly gaining ground,
the philosophical implications were still hot topics of discussion. Heisenberg,
Born and others besides these were favouring the particle view over the wave
concept, accepting the quantum jumps as they are, whereas Schr¨ odinger,
Einstein and other physicists were repulsed by these ideas. Observing that
the problem lies in transforming classical concepts like position and velocity
into the language of quantum physics, in a paper in 1927, Heisenberg set
out to find a way to describe these concepts operationally, as Einstein did to
space and time [43].
For Heisenberg, for an observable to have a meaningful description, the mea-
surement process and result have to be defined clearly. For instance, the
concepts of space and time according to Newton do not have a clear means
of measurement, whereas Einstein’s are defined directly on measurements.
For that matter, he considered an experiment with γ-rays to determine the
position of an electron. The velocity of the electron will change according to
the wavelength of the light, which in turn affects the accuracy of the mea-
surement. The photon’s wavelength will change according to the Compton
effect as
∆λ = h
mec(1 − cos θ). (128)
However, since the scattering angle is not known with certainty, we cannot
know the wavelength shift and, therefore, the momentum of the scattered
32

photon. After these considerations, he derived the result:
∆p∆q ≳ h, 25 (129)
This thought experiment seems to be valid for classical particles, too. How-
ever, in classical picture, the particles have exact positions and momenta
before measurement, whereas in quantum theory, they do not.26 So, it is not
a particularly good example of explaining the inherent uncertainty in nature.
Generalisations of the principle for any two conjugate variables followed by
others.27
A consequence related to that, although came before this derivation, is the
concept of indistinguishability of identical particles in quantum mechanics.
The concept of identical particles is not unique to quantum mechanics. For
instance, John Dalton already assumed that the particles comprising the el-
ements were identical [45]. But the concept of indistinguishability was some-
thing new. In classical physics, even if the particles are identical, they have
distinct trajectories defined by their position and momentum. Yet in quan-
tum physics, this cannot be the case, as it is seen by the uncertainty relation.
However, the uncertainty relation was not the only means to see this fact, as
Dirac had already published a paper on the now so-called Fermi-Dirac distri-
25He derived the exact expression
∆p∆q ≥ ℏ/2, (130)
for only Gaussian states. The formula is later shown to hold in general by Kennard [44].
26In wave picture, this principle arises from the inverse behaviour of spreading of wave
functions related to conjugate variables.
27A counter-argument came from Condon, [7], p. 353 - 354, in the meantime. The
basic idea can be outlined as follows: Consider the angular momentum of the electron
in the hydrogen atom, Lz = mℏ, which entails ∆ Lz = 0, and therefore ∆ Lz∆Lx = 0,
although [Lz, Lx] ̸= 0. The solution to the apparent contradiction lies in the fact that the
generalised version of the uncertainty principle reads
∆A∆B ≥ 1
2| ⟨D⟩ |, (131)
where
(∆A)2 =
Z
ψ∗(A − ⟨A⟩)2ψ dt. (132)
Since the equation is valid for ⟨Ly⟩ = 0, there is no contradiction.
33

bution of identical fermions in 1926 (about the same time but independently
from Fermi). The idea that led Dirac to the indistinguishability is as follows
(Dirac, 1926, p.667; [46] in references):
Consider now a system that contains two or more similar parti-
cles, say, for definiteness, an atom with two electrons. Denote by
(mn) that state of the atom in which one electron is in an orbit
labelled m, and the other in the orbit n. The question arises
whether the two states ( mn) and ( nm), which are physically in-
distinguishable as they differ only by the interchange of the two
electrons, are to be counted as two different states or as only one
state, i.e., do they give rise to two rows and columns in the ma-
trices or to only one? If the first alternative is right, then the
theory would enable one to calculate the intensities due to the
two transitions ( mn) → (m′n′) and ( mn) → (n′m′) separately,
as the amplitude corresponding to either would be given by a
definite element in the matrix representing the total polarisation.
The two transitions are, however, physically indistinguishable,
and only the sum of the intensities for the two together could be
determined experimentally. Hence, in order to keep the essential
characteristic of the theory that it shall enable one to calculate
only observable quantities, one must adopt the second alternative
that (mn) and (nm) count as only one state.
It is not necessary to point out that these ideas led to philosophical discus-
sions. There was a big controversy between these seemingly contradictory
concepts in terms of attaining them to reality at the time (and probably to
a greater extent still). The discussion revolved around two keypoints, which
may be called the singularities of the philosophical discussions since they
were the centers of attractions of conceptual discussions and the origin of the
problems themselves. These ”singularities” may be summarised more or less
as follows:
34

1. The whatness of measurement: What really is measurement in quan-
tum mechanical terms? Is there a point of seperation after which we
make a clear distinction between the quantum system and the mea-
surement apparatus?28
2. The questions on the ontological status of things: Is quantum theory
an epistomological theory, that is, a theory which describes nature up
to our capabilities of perception as Heisenberg argued [48]; or does it
really describe things as it is, and that is how nature really works in
the most fundamental level?
A comprehensive discussions on these matters are clearly out of the scope of
this text. However, a term related to these questions and highly relevant to
the development of quantum mechanics must be mentioned here: Comple-
mentarity. In essence, the idea, which is primarily attributed to Bohr [49],
states that the nature in its most fundamental level acts in phenomenologi-
cally mutually exclusive concepts, such as waves and particles, measurement
apparati and systems, or causality and definability of a state (since the act
of observation, which is a must that comes before definition, destroys the
causal evolution of the system ). More precisely, in Bohr’s words (Bohr,
1928, p.580):
On one hand, the definition of the state of a. physical system,
as ordinarily understood, claims the elimination of all external
disturbances. But in that case, according to the quantum pos-
tulate, any observation will be impossible, and, above all, the
concepts of space and time lose their immediate sense. On the
other hand, if in order to make observation possible we permit
certain interactions with suitable agencies of measurement, not
belonging to the system, an unambiguous definition of the state
of the system is naturally no longer possible, and there can be
28It is interesting to see that these questions are peculiarly similar to subject-object
problems in philosophy [47]. See also [7], ch. 7.2.
35

no question of causality in the ordinary sense of the word. The
very nature of the quantum theory thus forces us to regard the
spacetime co-ordination and the claim of causality, the union of
which characterises the classical theories, as complementary but
exclusive features of the description, symbolising the idealisation
of observation and definition, respectively.
The duels of Einstein and Bohr on these topics were especially illuminating,
although generally to Bohr’s advantage. One of these discussions led to the
EPR paradox [50], Bell inequalities [51], and finally, by the observation of
the violation of inequalities [52], to the existence of non-local phenomena in
nature (to the advantage of Bohr again).
One of these mental duels is especially interesting, for Bohr’s use of general
relativity to rule out Einstein’s argument [53]. The argument was as follows:
Consider a box filled with radiation. This box has a shutter that operates
on clockwork, to open and close for an arbitrarily short time to let a photon
escape through the hole. Now, if we measure the mass of the box before and
after the event, we can measure the energy of the photon by
E = mc2, (133)
and thus violate the energy-time uncertainty relation,
∆E∆t ≳ h. (134)
Bohr’s response was on the following lines: The measurement of the mass
difference can be made by balancing the box with a spring and a pointer with
an index to read the mass. After the shutter is closed again, an additional
weight m can be added to the box to measure the mass difference due to the
escaped photon to an accuracy ∆ m, which is connected to the accuracy of
the position measurement ∆ q of the pointer on the index. Since adding the
additional mass will impart an impulse p to the box (and the pointer), which
is subjected to the error ∆ p given by
∆p∆q ≳ h. (135)
36

The error of the momentum measurement is also bounded by the error of the
impulse given by the gravitation as
∆p ≈ h
∆q ≤ T g∆m, (136)
where T is the duration of the balancing procedure, and g is the gravitational
constant. But the ticks of the clocks will change throughout the process
according to the gravitational redshift formula by
∆T
T = g
c2 ∆q, (137)
for a displacement ∆q in the direction of the gravitational field. Substituting
for T in the first equation, we get
∆T c2∆m = ∆T∆E ≳ h. (138)
8 Conclusion
That brings us to the end of our account of the early development of the
quantum theory. When we look back, we realise that all the ideas discussed
here are actually just derivatives of the concept of ”quantum”. Planck in-
troduced the concept as a mathematical convenience (which was proven to
be a necessity by Poincar´ e about a decade later). Especially through the
discussions and applications of the theory of statistical mechanics (to the
calculations of which the concept of quanta brought great convenience as
well as new possibilities of thinking, as it did for Planck), the concept had
made its place in the minds of the physicist of the time in two decades. The
main tools used for calculation were the correspondence principle, in any
form, and the quantum of action principle, both of which had a significant
place in the fundamentals of matrix mechanics. The correspondence princi-
ple is basically a statement which demands you to replace continuity with
discreteness, somewhere and somehow. On the other hand, the quantum of
action principle directly dictates a quantisation principle. In wave picture,
these principles are replaced with boundary conditions on the wave function.
37

That seems too good to be true, and it actually is due to the ontologically
suspicious status of the wave function. Most of the time, it cannot be de-
scribed in our 3-dimensional space, and it also collapses, which is equally
indescribable as the other principles. Therefore, collapse is the place where
the concept of ”quantisation” comes into play, in the sense that we have to
empirically assign rules, as it is done in the particle picture, or suppose other
things to get rid of it, such as infinite parallel universes [54] or pilot waves
[55, 56], which are at best indirectly observable. All in all, maybe the prop-
erty of ”discreteness” (or put in another word, ”separability”) is somehow
equivalent to these seemingly derivative concepts.
Without a doubt, in a work, one of the main aims of which is to provide a
better grasp on the fundamental ideas of the quantum theory, not mention-
ing Pauli’s work on spin [57], which is a new degree of freedom unique to
the quantum realm; Dirac equation [58], which includes the spin degree of
freedom as a result of the reconciliation of special theory of relativity and
quantum theory; the works of von Neumann with the goal of placing the
quantum theory on a mathematically firm ground and understanding the
collapse [59]; (although mentioned) Bell inequalities [51], the observed viola-
tion of which led us to the fact that quantum theory is, in fact, non-local, and
thus closed the way to the local hidden variable theories; can be considered
a defect. Presumably, for further reading on the topics, the references of the
paper, and especially the work of Jammer [7], is a good starting point.
A Einstein’s First Paper on Brownian Mo-
tion
Although not directly related to the quantum theory, since the paper on
Brownian motion has historical significance concerning the discrete nature of
matter, it seemed relevant to discuss it here [60].
In the first two sections of the paper, Einstein assumes a solvent of volume
V and a solute which are separated by a partition V ∗ impermeable to the
38

solute. Then there will be an osmotic pressure P V∗ = zRT for z gram-
molecules on the partition. Now if you assume there are also n suspended
particles in the volume, (back then) classical thermodynamics predicts no
pressure by these particles on the partition. But Einstein suggests that such
particles are differentiated from the solute by only their dimensions and there
is no apparent reason for them not to apply pressure on the partition by the
thermokinetic movements. Then he proceeds to show mathematically that
the molecular-kinetic theory does predict such a pressure of the solute as
P V∗ = (n/NA)RT .
In section three, Einstein derives the diffusion predicted by the classical the-
ory, and in section four, he proceeds to show that molecular theory also
predicts that. At the start of the section, he makes two assumptions
1. The motions of the particles are independent of one another.
2. The subsequent motion of individual particles occurring in
a time τ is independent of one another. 29
Now, suppose there is an even function ϕ(∆) representing the probability
of a change in the position of the particle from x to x + ∆ (for simplicity,
it is studied in 1-dimension denoted x).30 Let η(x, t) represent the number
density of the particles per unit volume. By definition, we have
η(x, t+ τ) =
Z ∆=+∞
∆=−∞
η(x − ∆, t)ϕ(∆)d∆ (139)
29This is considered a weak point in Einstein’s argument since the subsequent motions
might really well be dependent by the causal relation of initial and final states of movement.
A derivation without this presupposition is carried out later, and the formula reached at
the end was the same as Einstein’s in sufficiently large time intervals:
x2 = 2D(t − mB − e−t/mB) − →2Dt
where m indicates the mass of the particle and B mobility.
30The function is even since there is no reason for the probability of a change of −∆
and +∆ to have different values.
39

and since τ is very small compared to observable time,
η(x, t+ τ) ≈ η(x, t) + τ ∂η
∂t . (140)
Since ∆ is a small displacement compared to the dimension of the volume
that contains the particles, we can expand the function in the integral around
∆ and omit the powers after the third term, and combine the expansions to
obtain
η(x,t + τ) ≈ η(x, t) + τ ∂η
∂t
=
Z +∞
−∞
η(x − ∆, t)ϕ(∆)d∆ ≈
Z +∞
−∞
η(x, t) − ∆∂η
∂x + ∆2
2
∂2η
∂x2 ϕ(∆)d∆
= η(x, t)
Z +∞
−∞
ϕ(∆)d∆ − ∂η
∂x
Z +∞
−∞
∆ϕ(∆)d∆
+ ∂2η
∂x2
Z +∞
−∞
∆2
2 ϕ(∆)d∆.
(141)
Since ϕ and ∆ are even functions, the corresponding integral vanishes, while
for
R+∞
−∞ ϕ(∆)d∆ = 1, η(x, t) terms also vanish:
τ ∂η
∂t = ∂2η
∂x2
Z +∞
−∞
∆2
2 ϕ(∆)d∆. (142)
The integral
R+∞
−∞
∆2
2τ ϕ(∆)d∆ = D is the diffusivity and
∂η
∂t = D ∂2η
∂x2 (143)
is the equation of diffusion. Assuming that n particles started from the centre
at t = 0, we have the solution
η(x, t) = n√
4πDt
e
−x2
4Dt , (144)
which is that of a normal distribution. The mean displacement (or the stan-
dard deviation) of the particles is thus
p
x2 =
√
2Dt. (145)
40

Now, using that D = RT
NA
1
6πκR , where κ is a coefficient of viscosity (dynamic
viscosity) and R is the radius of the particles, 31 and then equating it with
the result we derived, we get a relation that depends on T, κand R, whereby
acquire a way to determine NA, κ or R by measuring the corresponding
quantities:
x2
2t = RT
NA
1
6πκR . (146)
B Hamilton-Jacobi Formulation of Classical
Mechanics†
Finding the equations of motion is easiest when the coordinates are cyclic.
Yet the cyclicity of the coordinates depends not only on the system but also
on the chosen coordinate representation of the degrees of freedom. There-
fore, a procedure to transform a set of variables between different coordinate
systems proves useful.
Let a system be described by the coordinate set {qi, pi}, which obeys Hamil-
ton’s equations of motion. After a transformation, the new coordinates may
be written as
Qi = Qi(q, p, t), Pi = Pi(q, p, t). (147)
Since we expect the transformed coordinates to also obey the equations of
motions, for transformed Hamiltonian K = K(Q, P, t), we should have
˙Qi = ∂K
∂Pi
,
˙Pi = − ∂K
∂Qi
.
(148)
Now, since
δ
Z t2
t1
Ldt = δ
Z t2
t1
pi ˙qi − H(q, p, t)dt = 0
=⇒ δ
Z t2
t1
Pi ˙Qi − K(Q, P, t)dt = 0.
(149)
31This expression is derived in the paper but not included here.
† For more information on these topics, see [29] and [61].
41

where L is the Lagrangian of the system, Therefore,
λ[pi ˙qi − H(q, p, t)] = Pi ˙Qi − K(q, p, t) + dF
dt , (150)
where λ is independent of q, p, t, and F is any function of the phase space
coordinates with continuous second derivatives. 32 The transformations for
which λ = 1 are called canonical transformations. The last term of the
transformed Lagrangian can be written as a function of transformed or un-
transformed coordinates, or as a combination of both. They are especially
useful when represented as a combination of old and new coordinates, for
then they can act as a bridge between the set of coordinates. These types of
functions F are called generating functions of the transformation.
Take, for example, the generating function F1 = F1(q, Q, t). We have the
Lagrangian in terms of the transformed coordinates as
L = pi ˙qi −H = Pi ˙Qi −K + dF1
dt = Pi ˙Qi −K + ∂F1
∂t + ∂F1
∂qi
˙qi + ∂Fi
∂Qi
˙Qi. (152)
Therefore,
pi = ∂F1
∂qi
,
Pi = −∂F1
∂Qi
,
K = H + ∂F1
∂t .
(153)
Other kinds of generating functions are
F = F2(q, P, t) − QiPi,
F = F3(p, Q, t) + qipi,
F = F4(p, P, t) + qipi − QiPi.
(154)
32Notice that
δ
Z t2
t1
dF
dt dt = δ(F2 − F1) = 0, (151)
where Fi are evaluated at the endpoints for any combination of the coordinates{Q, P, q, p},
along with t, they contain.
42

These are the Legendre transformations of F1. Note that a suitable gener-
ating function does not have to be in the form of the four we listed. In all
cases, though, the Hamiltonian is in the form
K = H + ∂F
∂t . (155)
If the Hamiltonian is conserved, then there is a coordinate frame for which
every coordinate is cyclic. 33 Therefore, we can choose a coordinate system
where K = 0, for then the transformed coordinates satisfy
∂K
∂Pi
= ˙Qi = 0,
− ∂K
∂Qi
= ˙Pi = 0.
(157)
By (155), then,
H(q, p, t) + ∂F
∂t = 0. (158)
It is convenient to express F in qi, Pi, that is, as F2 = F2(qi, Pi, t), for which
we have
pi = ∂F2
∂qi
, (159)
so that we have
H(qi, ∂F2
∂qi
, t) + ∂F2
∂t = 0, (160)
which is known as the Hamilton-Jacobi equation. The generating function
F2 is denoted as S and called Hamilton’s principle function. The total time
derivative of it reads
dS
dt = ∂S
∂qi
˙qi + ∂S
∂Pi
˙Pi + ∂S
∂t = pi ˙qi − H = L, (161)
33Observe
dH
dt = ∂H
∂t + ∂H
∂q ˙q + ∂H
∂p ˙p
= ∂H
∂t + ∂H
∂q
∂H
∂p − ∂H
∂p
∂H
∂q
= ∂H
∂t ,
(156)
which is equal to zero if the Hamiltonian has no explicit time dependence.
43

by equations (157), (159), and (160). Therefore,
S =
Z
Ldt + const. (162)
Yet, since the coordinates are not known as functions of time before solving
the problem, we cannot just integrate L and find S. When the Hamiltonian
does not have an explicit time dependence, S can be written as
S(q, P, t) = W(q, P) − Et, (163)
where W is called Hamilton’s characteristic function. In this case, Hamilton-
Jacobi equation takes the special form,
H

q1, .., qn; ∂W
∂q1
, . . . ,∂W
∂qn

= E. (164)
It is interesting to see that, since
dW
dt = ∂W
∂qi
˙qi = pi ˙qi, (165)
we have
W =
Z
pi ˙qidt =
Z
pidqi, (166)
which is the action.
B.1 Separable Systems
It is customary to express the constant momenta Pi as αi. A coordinate qj
is said to be separable if the principle function can be set in the form
S(q1, ..,qk, . . . , qn; α1, .., αn; t)
= Sk(qk; α1, . . . , αn; t) + S′(q1, .., qk−1, qk+1, . . . , qn; α1, .., αn; t).
(167)
Hamilton’s principal function S is said to be completely separable if it can
be cast into the form,
S(q1, . . . , qn; α1, . . . , αn; t) =
nX
i=1
Wi(qi; α1, .., αn) − Et. (168)
44

If we also have a Hamiltonian, such as
H =
nX
i=1
Hi

qi, ∂Wi
∂qi

, (169)
then the Hamilton-Jacobi equation can be separated into n equations as
H

qi; ∂Wi
∂qi

= Ei. (170)
For instance, consider a system with a Hamiltonian which is time-independent
and quadratic in momenta, with the potential energy defined byV = V (q1, . . . , qn),
as
H =
nX
i=1
1
2mi
p2
i + V (q1, q2, . . . , qn). (171)
Substituting pi = ∂S/∂qi into the HJE, we get
nX
i=1
1
2mi
∂S
∂qi
2
+ V (q1, q2, . . . , qn) = E. (172)
Assuming that the potential energy is additively separable as
V (q1, q2, . . . , qn) = V1(q1) + V2(q2) + · ··+ Vn(qn), (173)
we can assume a completely separable solution for S in the form (168). Sub-
stituting this into the HJE gives
nX
i=1
1
2mi
dSi
dqi
2
+ Vi(qi) = E. (174)
Since each term depends only on a single coordinate qi, the equation com-
pletely separates into individual equations,
1
2mi
dSi
dqi
2
+ Vi(qi) = Ei, (175)
where the total energy is a sum of individual contributions,
E =
X
i
Ei. (176)
45

B.2 Action-Angle Variables
For systems in periodic motion, sometimes the frequency is more relevant to
know than the whole solution in terms of the coordinates. In this case, the
action-angle variables prove useful, which is the topic of this subsection.
For a system in periodic motion, for which the energy is conserved and the
characteristic function is separable, such that
H

q1, . . . , qn , ∂W
∂q1
, . . . ,∂W
∂qn

= α1, W =
X
i
Wi(qi, αi). (177)
The action variables are defined as
J =
I
pidqi =
I ∂Wi
∂qi
dqi. (178)
Since the qi dependence is integrated away, Ji are functions of only the
constants αi as Ji = Ji(α1, . . . , αn). Assuming that the transformation
(α1, . . . , αn) 7→ (J1, . . . , Jn) is invertible,34 we can write αi = αi(J1, . . . , Jn).
Therefore, the characteristic function and the Hamiltonian can be cast into
the form
K = K(J) = α1(J1, . . . , Jn), W =
X
i
Wi(qi, Ji). (179)
The angle variable is defined, as usual, by
θi = ∂W
∂Ji
. (180)
Thus, we have two kinds of canonical variables, θ and J, such that the
transformed Hamiltonian depends only on one, as K = K(J), so θ is cyclic.
Since K is a constant of motion (by assumption) and depends only on J, J
must also be a constant of motion since
dK
dt =
X
i
∂K
∂Ji
dJi
dt = 0 =⇒ dJi
dt = 0. (181)
34For most integrable systems, we can presume that there are coordinate frames that
satisfy the global invertibility conditions. For the conditions and the proof, see [62] and
[63].
46

Therefore, the Hamilton’s equation for that system should be in the form
˙Ji = −∂K
∂θi
= 0, ˙θi = ∂K
∂Ji
= ωi = const., (182)
where the reason for the second equality is that since K = K(J), and that
J is a constant of motion, then ˙θ can either be zero or another arbitrary
constant.
Now, consider a change in θ in a complete cycle as
∆θi =
I ∂θi
∂qi
dqi =
I ∂2W
∂qi∂Ji
dqi = d
dJi
I ∂Wi
∂qi
dqi = dJi
dJi
= 1, (183)
that is, over a period, the angle variable changes by a unit. Then, since we
have
˙θi = ωi =⇒ θi = ωt + ci, (184)
where ωi and ci are constants, we should also have
∆θi = ωiτi = 1 =⇒ ωi = 1/τi, (185)
where τi is the period, and ωi = ∂JiK is the frequency associated with the
motion in qi.
Statements and Declarations
Competing Interests The author declares that there are no financial or non-financial
competing interests related to this work.
Funding No funding was received for conducting this study.
Data AvailabilityNo datasets were generated or analyzed during the current study.
47

References
1. Kirchhoff, G. ¨Uber das Verh¨ altnis zwischen dem Emissionsverm¨ ogen
und dem Absorptionsverm¨ ogen der K¨ orper f¨ ur W¨ arme und Licht.An-
nalen der Physik 185, 275–301. doi:10.1002/andp.18601850205 (1860).
2. Wien, W. ¨Uber die Energieverteilung im Emissionsspectrum eines schwarzen
K¨ orpers.Annalen der Physik 294, 662–669. doi:10.1002/andp.18962
940803 (1896).
3. Rayleigh, L. Remarks upon the law of complete radiation. Philosophical
Magazine 49, 539–540. doi:10.1080/14786440009463878 (1900).
4. Ehrenfest, P. Welche Z¨ uge der Lichtquantenhypothese spielen in der
Theorie der W¨ armestrahlung eine wesentliche Rolle?Annalen der Physik
341, 91–118. doi:10.1002/andp.19113411106 (1911).
5. Lenard, P. ¨Uber die lichtelektrische Wirkung. Annalen der Physik 313,
149–198. doi:10.1002/andp.19023130510 (1902).
6. Rutherford, E. The Scattering of α and β Particles by Matter and the
Structure of the Atom. Philosophical Magazine 21, 669–688. doi:10.10
80/14786440508637080 (1911).
7. Jammer, M. The Conceptual Development of Quantum Mechanics 2nd
ed., repr. (Tomash Publishers and American Institute of Physics, 1989).
8. Planck, M. Ueber das Gesetz der Energieverteilung im Normalspectrum.
Annalen der Physik 309, 553–563. doi: 10.1002/andp.19013090310
(1901).
9. Planck, M. in Von Kirchhoff bis Planck (ed Sch¨ opf, H.-G.) Reprint of
the original 1900 article inVerhandlungen der Deutschen Physikalischen
Gesellschaft, 175–178 (Vieweg+Teubner Verlag, Wiesbaden, 1900).
10. Jeans, J. H. On the Laws of Radiation. Philosophical Transactions of the
Royal Society of London. Series A, Containing Papers of a Mathemat-
ical or Physical Character 76, 545–552. doi:10.1098/rspa.1905.0060
(1905).
11. Einstein, A. ¨Uber einen die Erzeugung und Verwandlung des Lichtes be-
treffenden heuristischen Gesichtspunkt. Annalen der Physik 322, 132–
148. doi:10.1002/andp.19053220607 (1905).
12. Bomark, N.-E. & Renstrøm, R. The Ultraviolet Myth in Proceedings
of the European Physical Society Conference on High Energy Physics
(EPS-HEP 2023) (2023). https://pos.sissa.it/449/660/.
13. Einstein, A. Quantentheorie des einatomigen idealen Gases. Sitzungs-
berichte der Preußischen Akademie der Wissenschaften, Physikalisch-
mathematische Klasse, 261–267. doi:10.1002/3527608958.ch27 (1924).
48

14. Einstein, A. in Albert Einstein: Akademie-Vortr¨ age245–257 (John Wi-
ley and Sons, Ltd, 1925). doi: https://doi.org/10.1002/3527608958
.ch28.
15. Ehrenfest, P. & Onnes, H. K. XXXIII. Simplified deduction of the for-
mula from the theory of combinations which Planck uses as the basis of
his radiation theory. The London, Edinburgh, and Dublin Philosophical
Magazine and Journal of Science 29, 297–301. doi:10.1080/14786440
208635308. https://doi.org/10.1080/14786440208635308 (1915).
16. Planck, M. La Loi du Rayonnement Noir et l’Hypoth` ese des Quantit´ es
´El´ ementaires d’Actionin La th´ eorie du rayonnement et les quanta: rap-
ports et discussions de la r´ eunion tenue ` a Bruxelles du 30 octobre au 3
novembre 1911 (Gauthier-Villars, Paris, 1912), 93–114. http://www.s
olvayinstitutes.be/pdf/Proceedings_Physics/1911.pdf.
17. Poincar´ e, H. Sur la th´ eorie des quanta.Journal de Physique Th´ eorique
et Appliqu´ ee2, 5–34. doi:10.1051/jphystap:0191200200500 (1912).
18. Bohr, N. On the Constitution of Atoms and Molecules. Philosophical
Magazine 26, 1–25. doi:10.1080/14786441308634955 (1913).
19. Bohr, N. On the Quantum Theory of Line-Spectra https://www.gute
nberg.org/ebooks/47167 (Project Gutenberg, 2014).
20. Born, M. ¨Uber Quantenmechanik. Zeitschrift f¨ ur Physik26, 379–395.
doi:10.1007/BF01327341 (1924).
21. Sommerfeld, A. Zur Theorie der Balmerschen Serie. Sitzungsberichte der
Bayerischen Akademie der Wissenschaften, Mathematisch-Physikalische
Klasse, 425–458. https://d-nb.info/1345425740/34 (1915).
22. Sommerfeld, A. Zur Quantentheorie der Spektrallinien. Annalen der
Physik 356, 1–94. doi:https://doi.org/10.1002/andp.19163561702
(1916).
23. Heisenberg, W. ¨Uber quantentheoretische Umdeutung kinematischer
und mechanischer Beziehungen. Zeitschrift f¨ ur Physik 33, 879–893.
doi:10.1007/BF01328377 (1925).
24. Aitchison, I. J. R., MacManus, D. A. & Snyder, T. M. Understanding
Heisenberg’s ’magical’ paper of July 1925: a new look at the calcula-
tional details. American Journal of Physics 72, 1370–1379. doi:10.111
9/1.1775243 (2004).
25. Born, M., Heisenberg, W. & Jordan, P. Zur Quantenmechanik II. Zeitschrift
f¨ ur Physik35, 557–615. doi:10.1007/BF01379806 (1926).
26. Born, M. & Jordan, P. Zur Quantenmechanik. Zeitschrift f¨ ur Physik
34, 858–888. doi:10.1007/BF01328531 (1925).
27. Born, M. & Wiener, N. Eine neue Formulierung der Quantengesetze f¨ ur
periodische und nicht periodische Vorg¨ ange.Zeitschrift f¨ ur Physik36,
174–187. doi:10.1007/BF01382261 (1926).
49

28. Dirac, P. A. M. The Fundamental Equations of Quantum Mechanics.
Proceedings of the Royal Society of London. Series A, Containing Pa-
pers of a Mathematical and Physical Character 109, 642–653. doi:10.1
098/rspa.1925.0150 (1925).
29. Goldstein, H., Poole, C. & Safko, J. Classical Mechanics 3rd (Addison-
Wesley, 2002).
30. Hamilton, W. R. On a General Method of Expressing the Paths of Light,
and of the Planets, by the Coefficients of a Characteristic Function.
Dublin University Review and Quarterly Magazine 1, 795–826. https:
//www.maths.tcd.ie/pub/HistMath/People/Hamilton/LightPlane
ts/LightPlanets.html (1833).
31. Joas, C. & Lehner, C. The classical roots of wave mechanics: Schr¨ odinger’s
transformation of the optical-mechanical analogy. Studies in History
and Philosophy of Science Part B: Studies in History and Philosophy
of Modern Physics 40, 338–351. doi:10.1016/j.shpsb.2009.06.007
(2009).
32. De Broglie, L. A Tentative Theory of Light Quanta. Philosophical Mag-
azine 47, 446–458. doi:10.1080/14786442408634378 (1924).
33. Schr¨ odinger, E. An Undulatory Theory of the Mechanics of Atoms and
Molecules. Physical Review 28, 1049–1070. doi:10.1103/PhysRev.28
.1049 (1926).
34. Bose, S. N. Planck’s Gesetz und Lichtquantenhypothese. Zeitschrift f¨ ur
Physik 26, 178–181. doi:10.1007/BF01327326 (1924).
35. Schr¨ odinger, E. Quantisierung als Eigenwertproblem. Erste Mitteilung.
Annalen der Physik 384, 361–376. doi: 10.1002/andp.19263840404
(1926).
36. Schr¨ odinger, E. Quantisierung als Eigenwertproblem. Zweite Mitteilung.
Annalen der Physik 384, 489–527. doi: 10.1002/andp.19263840602
(1926).
37. Schr¨ odinger, E. Quantisierung als Eigenwertproblem. Dritte Mitteilung.
Annalen der Physik 385, 437–490. doi: 10.1002/andp.19263851302
(1926).
38. Schr¨ odinger, E. Quantisierung als Eigenwertproblem. Vierte Mitteilung.
Annalen der Physik 386, 109–139. doi: 10.1002/andp.19263861802
(1926).
39. Ip, P. H. The Mystery Behind Schr¨ odinger’s First Communication: A
Non-Historical Study on the Variational Approach and Its Implications.
PhilSci Archive. https://philsci-archive.pitt.edu/9839/ (2013).
40. Sommerfeld, A. Atombau und Spektrallinien 1st. https://archive.o
rg/details/atombauundspektr00somm (Friedrich Vieweg und Sohn,
Braunschweig, 1929).
50

41. Born, M. Quantenmechanik der Stoßvorg¨ ange. Zeitschrift f¨ ur Physik
38, 803–827. doi:10.1007/BF01397184 (1926).
42. Born, M. Zur Quantenmechanik der Stoßvorg¨ ange.Zeitschrift f¨ ur Physik
37, 863–867. doi:10.1007/BF01397477 (1926).
43. Heisenberg, W. The Actual Content of Quantum Theoretical Kinemat-
ics and Mechanics tech. rep. NASA-TM-77379 (NASA Technical Mem-
orandum, 1983). https://ntrs.nasa.gov/citations/19840008978.
44. Kennard, E. H. Zur Quantenmechanik einfacher Bewegungstypen. Zeitschrift
f¨ ur Physik44, 326–352. doi:10.1007/BF01391200 (1927).
45. Dalton, J. A New System of Chemical Philosophy 141–145. https :
//archive.org/details/newsystemofchemi01daltuoft (Cambridge
University Press, 1808).
46. Dirac, P. A. M. On the Theory of Quantum Mechanics. Proceedings of
the Royal Society of London. Series A, Containing Papers of a Mathe-
matical and Physical Character 112, 661–677. doi:10.1098/rspa.192
6.0133 (1926).
47. Bell, J. S. in The physicist’s conception of nature (ed Mehra, J.) 687–
690 (Reidel, 1973).
48. Heisenberg, W. Das Naturbild der heutigen Physik (Rowohlt, Hamburg,
1955).
49. Bohr, N. The Quantum Postulate and the Recent Development of Atomic
Theory. Nature 121, 580–590. doi:10.1038/121580a0 (1928).
50. Einstein, A., Podolsky, B. & Rosen, N. Can Quantum-Mechanical De-
scription of Physical Reality Be Considered Complete? Physical Review
47, 777–780. doi:10.1103/PhysRev.47.777 (1935).
51. Bell, J. S. On the Einstein Podolsky Rosen paradox. Physics Physique
Fizika 1, 195–200. doi:10.1103/PhysicsPhysiqueFizika.1.195 . htt
ps://link.aps.org/doi/10.1103/PhysicsPhysiqueFizika.1.195
(Nov. 1964).
52. Aspect, A., Grangier, P. & Roger, G. Experimental Realization of Einstein-
Podolsky-Rosen-Bohm Gedankenexperiment: A New Violation of Bell’s
Inequalities. Phys. Rev. Lett. 49, 91–94. doi:10.1103/PhysRevLett.49
.91 (July 1982).
53. Bohr, N. in Albert Einstein: Philosopher-Scientist (ed Schilpp, P. A.)
201–241 (Library of Living Philosophers, 1949).
54. Everett, H. The Many-Worlds Interpretation of Quantum Mechanics
PhD Thesis (Princeton University, 1957).
55. Bohm, D. A Suggested Interpretation of the Quantum Theory in Terms
of ”Hidden” Variables. I. Physical Review 85, 166–179. doi:10.1103/Ph
ysRev.85.166 (1952).
51

56. Bohm, D. A Suggested Interpretation of the Quantum Theory in Terms
of ”Hidden” Variables. II. Physical Review 85, 180–193. doi:10.1103
/PhysRev.85.180 (1952).
57. Pauli, W. ¨Uber den Einfluß der Geschwindigkeitsabh¨ angigkeit der Elek-
tronenmasse auf den Zeemaneffekt. Zeitschrift f¨ ur Physik31, 373–385.
doi:10.1007/BF02980592. https://link.springer.com/article/10
.1007/BF02980592 (1925).
58. Dirac, P. A. M. The Quantum Theory of the Electron. Proceedings of
the Royal Society of London. Series A, Containing Papers of a Mathe-
matical and Physical Character 117, 610–624. doi:10.1098/rspa.192
8.0023 (1928).
59. Von Neumann, J. Mathematische Grundlagen der Quantenmechanik
(Springer, 1932).
60. Einstein, A. in Investigations on the Theory of the Brownian Movement
(ed F¨ urth, R.) trans. by Cowper, A. D., 1–18 (Dover Publications, New
York, 1956).
61. Hand, L. N. & Finch, J. D. Analytical Mechanics (Cambridge University
Press, Cambridge, UK, 1998).
62. Gordon, W. B. On the Diffeomorphisms of Euclidean Space. The Amer-
ican Mathematical Monthly 79, 755–759. doi:10.2307/2316266 (1972).
63. Ohkita, S. & Tsukamoto, M. Simple proof of the global inverse func-
tion theorem via the Hopf–Rinow theorem. Proceedings of the Japan
Academy, Series A, Mathematical Sciences 100, 17–19. doi:10.3792/p
jaa.100.004. https://arxiv.org/pdf/2306.17410 (2024).
52