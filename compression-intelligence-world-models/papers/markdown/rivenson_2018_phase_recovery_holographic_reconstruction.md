OPEN

ARTICLE

Light: Science & Applications (2018) 7, 17141; doi:10.1038/lsa.2017.141
Ofﬁcial journal of the CIOMP 2047-7538/18
www.nature.com/lsa

Phase recovery and holographic image reconstruction
using deep learning in neural networks

Yair Rivenson1,2,3,*, Yibo Zhang1,2,3,*, Harun Günaydın1, Da Teng1,4 and Aydogan Ozcan1,2,3,5

Phase recovery from intensity-only measurements forms the heart of coherent imaging techniques and holography. In this study,
we demonstrate that a neural network can learn to perform phase recovery and holographic image reconstruction after appro-
priate training. This deep learning-based approach provides an entirely new framework to conduct holographic imaging by rapidly
eliminating twin-image and self-interference-related spatial artifacts. This neural network-based method is fast to compute and
reconstructs phase and amplitude images of the objects using only one hologram, requiring fewer measurements in addition to
being computationally faster. We validated this method by reconstructing the phase and amplitude images of various samples,
including blood and Pap smears and tissue sections. These results highlight that challenging problems in imaging science can
be overcome through machine learning, providing new avenues to design powerful computational imaging systems.
Light: Science & Applications (2018) 7, 17141; doi:10.1038/lsa.2017.141; published online 23 February 2018

Keywords: deep learning; holography; machine learning; neural networks; phase recovery

INTRODUCTION
Optoelectronic sensor arrays, such as charge-coupled devices (CCDs) or
complementary metal-oxide-semiconductor (CMOS)-based imagers,
are only sensitive to the intensity of light; therefore, phase information
of the objects or the diffracted light waves cannot be directly recorded
using such imagers. Phase recovery from intensity-only measurements
has emerged as an important ﬁeld to recover this lost phase information
in the detection process, enabling the reconstruction of the phase and
amplitude images of specimen using various approaches1–13. In fact,
Gabor’s original in-line holography system14, where the diffracted light
from the object interferes with the background light that is directly
transmitted, is an important example where phase recovery is required
to separate the twin-image and self-interference-related spatial artifacts
from the real image of the sample. In various implementations, to
improve the performance of the phase recovery and image reconstruc-
tion processes, additional intensity information is recorded, for example,
by scanning the illumination source aperture15–18, sample-to-sensor
distance19–23 (in some cases referred to as out-of-focus imaging24),
illumination25,26, or phase front of
the reference
wavelength of
beam27–30, among other methods31–36. All
these methods utilize
additional physical constraints and intensity measurements to robustly
retrieve the missing phase information based on an analytical and/or
iterative solution that satisﬁes the wave equation. Some of these phase
retrieval techniques have enabled discoveries in different ﬁelds37–40.

trained through deep learning41,42,

In this paper, we report a convolutional neural network-based
method,
that can perform
phase recovery and holographic image reconstruction using a single
hologram intensity. Deep learning is a machine learning technique
a multi-layered artiﬁcial neural network for data
that uses
modeling, analysis and decision making and has shown considerable
success in areas where large amounts of data are available. Deep
learning has recently been applied to solving inverse problems in
imaging science such as in super-resolution43,44, acceleration of the
image acquisition speed of computed tomography (CT)45, magnetic
(MRI)46, photoacoustic
and
resonance
holography48,49.

tomography47

imaging

In this work, we used deep learning to rapidly perform phase
recovery and reconstruct complex-valued images of specimen using a
single intensity-only hologram. This process is very fast, requiring
approximately 3.11 s on a graphics processing unit (GPU)-based laptop
computer to recover the phase and amplitude images of a specimen
over a ﬁeld of view of 1 mm2 with ~ 7.3 megapixels in each image
channel (amplitude and phase). We validated this approach by
reconstructing the complex-valued images of various samples, such as
blood and Papanicolaou (Pap) smears as well as thin sections of human
tissue samples, all of which demonstrated successful elimination of the
twin-image and self-interference-related spatial artifacts that arise due to
lost phase information during the hologram detection process. In other
words, the convolutional neural network, after its training, learned to

1Electrical and Computer Engineering Department, University of California, Los Angeles, CA 90095, USA; 2Bioengineering Department, University of California, Los Angeles, CA
90095, USA; 3California NanoSystems Institute (CNSI), University of California, Los Angeles, CA 90095, USA; 4Computer Science Department, University of California, Los
Angeles, CA 90095, USA and 5Department of Surgery, David Geffen School of Medicine, University of California, Los Angeles, CA 90095, USA
*These authors contributed equally to this work
Correspondence: A Ozcan, Email: ozcan@ucla.edu
Received 21 June 2017; revised 5 October 2017; accepted 11 October 2017; accepted article preview online 13 October 2017
The accepted article preview was available with the details: Light: Science & Applications (2018) 7, e17141; doi: 10.1038/lsa.2017.141

Holographic reconstruction and phase recovery using neural networks
Y Rivenson et al

2

extract and separate the spatial features of the real image from the
features of the twin-image and other undesired interference terms for
both the phase and amplitude channels of the object. Remarkably, this
deep learning-based phase recovery and holographic image reconstruc-
tion approach has been achieved without any modeling of light–matter
interaction or wave interference. However, this does not imply that the
presented approach entirely ignores the physics of light–matter inter-
action and holographic imaging, which is in fact statistically inferred
through deep learning in the convolutional neural network by using a
large number of microscopic images as the gold standard in the training
phase. This training and statistical optimization of the neural network is
performed once and can be considered as part of a blind reconstruction
framework that performs phase recovery and holographic image
reconstruction using a single input such as an intensity-only hologram
of the object. This framework introduces a myriad of opportunities to
design fundamentally new coherent imaging systems and can be broadly
applicable to any phase recovery problem, spanning different parts of
the electromagnetic spectrum, including visible wavelengths as well as
X-rays28,30,50,51.

RESULTS AND DISCUSSION
Our deep neural network approach for phase retrieval and holographic
image reconstruction is schematically described in Figure 1 (see also
Supplementary Figs. S1–S4). In this work, we chose to demonstrate
the proposed framework using lens-free digital in-line holography of
transmissive samples, including human tissue sections and blood and
Pap smears (see Matrials and Methods). Due to the dense and
connected nature of these samples that we imaged, their holographic
in-line imaging requires the acquisition of multiple holograms for
accurate and artifact-free object recovery52. A schematic of our
experimental setup is shown in Supplementary Fig. S5, where the
sample is positioned very close to a CMOS sensor chip with a o1 mm
sample-to-sensor distance, which provides an important advantage in
terms of the sample ﬁeld of view that can be imaged. However, due to
this relatively short sample-to-sensor distance, the twin-image artifact
of
the lost phase
information, is strong and severely obstructs the spatial features of
the sample in both the amplitude and phase channels, as illustrated in
Figures 1 and 2.

the in-line holography, which is a result of

Amplitude

Phase

l

s
e
x
p
M

i

Hologram
intensity

50 μm

N pixels

Input

50 μm

Free space
back-
propagation

v
n
o
C

r
e
y
a

l

v
n
o
C

r
e
y
a

l

v
n
o
C

r
e
y
a

l

v
n
o
C

r
e
y
a

l

2

4

8

l

i

a
u
d
s
e
R

k
c
o
b

l

l

i

a
u
d
s
e
R

k
c
o
b

l

l

i

a
u
d
s
e
R

k
c
o
b

l

l

i

a
u
d
s
e
R

k
c
o
b

l

M

N

16

2
/
M

N/2

16

4
/
M

N/4

16

8
/
M

N/8

16

Network output
(phase recovered)

Amplitude

Phase

Convolutional
neural
network

Network input
(with twin image)

50 μm

M

N

16

M

N

16

M

N

16

M

N

16

/

S
U

k
c
o
b

l

/

S
U

k
c
o
b

l

/

S
U

k
c
o
b

l

Output

v
n
o
C

r
e
y
a

l

M

N

64

Figure 1 Following its training phase, the deep neural network blindly outputs artifact-free phase and amplitude images of the object using only one
hologram intensity. This deep neural network is composed of convolutional layers, residual blocks and upsampling blocks (see Supplementary Information for
additional details) and rapidly processes a complex-valued input image in a parallel, multi-scale manner.

Light: Science & Applications

doi:10.1038/lsa.2017.141

Holographic reconstruction and phase recovery using neural networks
Y Rivenson et al

3

Hologram

1

a

Hologram

i

1

0

50 μm

Amplitude

50 μm

0

Phase

(cid:2)/3

Amplitude

Phase

(cid:2)/3

t
u
p
n

i

k
r
o
w
t
e
N

t
u
p
t
u
o
k
r
o
w
t
e
N

l

i

e
g
n
s
a
m
o
r
f

i

t
h
g
e
h
-
i
t
l
u
M

n
o
i
t
c
u
r
t
s
n
o
c
e
r

50 μm

c

e

g

–(cid:2)/3

j

l

n

50 μm

k

m

o

–(cid:2)/3

b

d

f

m
a
r
g
o
o
h

l

l

s
m
a
r
g
o
o
h
8
m
o
r
f

h

p

50 μm

20× 0.5NA
Microscope image

50 μm

20× 0.5NA
Microscope image

Figure 2 Comparison of the holographic reconstruction results for different types of samples: (a-h) Pap smear, (i-p) breast tissue section. (a, i) Zoomed-in
regions of interest from the acquired holograms. (b, c, j, k) Amplitude and phase images resulting from free-space back-propagation of a single hologram
intensity, shown in a and i, respectively. These images are contaminated with twin-image and self-interference-related spatial artifacts due to the missing
phase information in the hologram detection process. (d, e, l, m) Corresponding amplitude and phase images of the same samples obtained by the deep
neural network, demonstrating the blind recovery of the complex object image without twin-image and self-interference artifacts using a single hologram. (f,
g, n, o) amplitude and phase images of the same samples reconstructed using multi-height phase retrieval with 8 holograms acquired at different sample-to-
sensor distances. (h, p) corresponding bright-ﬁeld microscopy images of the same samples, shown for comparison. The yellow arrows point to artifacts in f, g,
n, o (due to out-of-focus dust particles or other unwanted objects) that are signiﬁcantly suppressed by the network reconstruction, as shown in d, e, l, m.

The ﬁrst step in our deep learning-based phase retrieval and
holographic image reconstruction framework consists of ‘training’
the neural network. This training involves learning the statistical
transformation between a complex-valued image that results from the
back-propagation of a single intensity-only hologram of the object and
the same object’s image that is reconstructed using a multi-height
phase retrieval algorithm (treated as the gold standard for the training
phase). This algorithm uses 8 hologram intensities acquired at
different sample-to-sensor distances (see Materials and Methods as
well as Supplementary Information). As illustrated in Figures 1,2,3, a
simple back-propagation of the object’s hologram, without phase
retrieval, contains severe twin-image and self-interference-related
artifacts, hiding the phase and amplitude information of the object.

This training/learning process (which is performed only once) results
in a ﬁxed deep neural network that is used to blindly reconstruct the
phase and amplitude images of any object, free from twin-image and
other undesired interference-related artifacts, using a single hologram
intensity.

In our holographic imaging experiments, we used three different
types of samples: blood smears, Pap smears and breast tissue sections,
and separately trained three convolutional neural networks for each
sample type, although the network architecture was identical in each
case, as shown in Figure 1. To avoid over-ﬁtting the neural network,
we stopped the training when the deep neural network performance
on the validation image set (which is different from the training image
set and the blind testing image set) began to decline. We also

doi:10.1038/lsa.2017.141

Light: Science & Applications

Holographic reconstruction and phase recovery using neural networks
Y Rivenson et al

4

a

)

2

m
μ
.
d
a
r
(

l

a
r
g
e
t
n

i

e
s
a
h
p

l
l

e
c
d
o
o
b
d
e
r

l

t
u
p
t
u
o
/
t
u
p
n

i

k
r
o
w
t
e
N

0

30

25

20

15

10

5

0

0

Multi-height phase recovery red blood cell effective refractive volume V . Δn (fL)

0.5

1

1.5

2

Network output

Network input

y = x

5

15
Multi-height phase recovery red blood cell phase integral (rad(cid:129)μm2)

25

20

10

2.5

2.5

2

1.5

1

0.5

0

30

Network input

Network output

Multi-height
phase recovery

e

f

g

h

Hologram intensity
b

c

d

e
d
u
t
i
l

p
m
A

e
s
a
h
P

e
m
u
o
v

l

e
v
i
t
c
a
r
f
e
r
e
v
i
t
c
e
f
f
e

l
l

e
c

l

d
o
o
b
d
e
r

t
u
p
t
u
o
/
t
u
p
n

i

k
r
o
w
e
N

t

)
L
f
(

n
Δ

.

V

1

0
(cid:2)/4

Figure 3 Red blood cell volume estimation using our deep neural network-based phase retrieval. The deep neural network output (e, f), given the input (c, d)
obtained from a single hologram intensity (b), shows a good match with the multi-height phase recovery-based cell volume estimation results (a), calculated
using Nholo = 8 (g, h). Similar to the yellow arrows shown in Figure 2f, 2g, 2n and 2o, the multi-height phase recovery results exhibit an out-of-focus fringe
artifact at the center of the ﬁeld-of-view in (g, h). Refer to Supplementary Information for the calculation of the effective refractive volume of cells.

20 μm

–(cid:2)/4

accordingly made
the network compact and applied pooling
approaches53. Following this training process, each deep neural
network was blindly tested with different objects that were not used
in the training or validation image sets. Figures 1,2 and 3 show the
neural network-based blind reconstruction results for the Pap smears,
breast tissue sections and blood smears. These reconstructed phase
and amplitude images clearly demonstrate the success of our deep
neural network-based holographic image reconstruction approach to
blindly infer artifact-free phase and amplitude images of the objects,
matching the performance of the multi-height phase recovery. Table 1
further compares the structural similarity54 (SSIM) of our neural
network output
is,
Nholo = 1) against the results obtained with a traditional multi-height
phase retrieval algorithm using multiple holograms (that is, Nholo = 2,
3,…,8) acquired at different sample-to-sensor distances. A comparison

images (using a single input hologram,

that

of the SSIM index values reported in Table 1 suggests that the imaging
performance of the deep neural network using a single hologram is
comparable to that of multi-height phase retrieval, closely matching
the SSIM performance of Nholo = 2 for both Pap smear and breast
tissue samples and the SSIM performance of Nholo = 3 for blood smear
samples. The deep neural network-based reconstruction approach
reduces the number of holograms required by 2-3 times. In addition
to this reduction in the number of holograms, the computation time
for holographic reconstruction using a neural network is also
improved by more than three- and four-fold compared with those
of the multi-height phase retrieval using Nholo = 2 and Nholo = 3,
respectively (see Table 2).

The phase retrieval performance of our neural network is further
demonstrated by imaging red blood cells (RBCs) in a whole blood
smear. Using the reconstructed phase images of RBCs, the relative

Light: Science & Applications

doi:10.1038/lsa.2017.141

Holographic reconstruction and phase recovery using neural networks
Y Rivenson et al

5

Table 1 Comparison of the SSIM index values between the deep neural network output images obtained with a single hologram intensity (for both the
sample-type-speciﬁc (STS) and universal networks) and the multi-height phase retrieval results for different numbers of input holograms (Nholo)
corresponding to Pap smear samples, breast tissue histopathology slides and blood smear samples

Deep network

Deep network

Deep network

Multi-height

Multi-height

Multi-height

Multi-height

Multi-height

Multi-height

Multi-height

Reconstruction

method

input
(Nholo = 1)

output (STS)
(Nholo = 1)

output (Univer-
sal) (Nholo = 1)

phase-recovery
(Nholo = 2)

phase-recovery
(Nholo = 3)

phase-recovery
(Nholo = 4)

phase-recovery
(Nholo = 5)

phase-recovery
(Nholo = 6)

phase-recovery
(Nholo = 7)

phase-recovery
(Nholo = 8)

Sample type
Pap smear

real part

Pap smear
imaginary part
Blood smear

real part

Blood smear
imaginary part
Breast tissue

real part

Breast tissue
imaginary part

0.726

0.431

0.701

0.048

0.826

0.428

0.895

0.870

0.942

0.930

0.916

0.912

0.893

0.870

0.951

0.925

0.921

0.916

0.875

0.840

0.890

0.46

0.931

0.911

0.922

0.900

0.942

0.849

0.955

0.943

0.954

0.948

0.962

0.907

0.975

0.970

0.979

0.979

0.970

0.935

0.981

0.979

0.985

0.986

0.975

0.938

0.983

0.981

0.986

0.987

0.977

0.955

0.984

0.982

1

1

1

1

1

1

In each case, the SSIM index is separately calculated for the real and imaginary parts of the resulting complex-valued image with respect to the multi-height phase recovery result for Nholo = 8, and
thus, by deﬁnition, the last column on the right has an SSIM index of 1. Due to the presence of twin-image and self-interference artifacts, the ﬁrst column formed by the input images has the worst
performance.

Table 2 Comparison of the holographic image reconstruction runtime for a ﬁeld of view of ~ 1 mm2 for different phase recovery approaches

Deep network

Deep network output

Multi-height

Multi-height

Multi-height

Multi-height

Multi-height

Multi-height

Multi-height

output (STS)
(Nholo = 1)

(Universal)
(Nholo = 1)

phase-recovery
(Nholo = 2)

phase-recovery
(Nholo = 3)

phase-recovery
(Nholo = 4)

phase-recovery
(Nholo = 5)

phase-recovery
(Nholo = 6)

phase-recovery
(Nholo = 7)

phase-recovery
(Nholo = 8)

Runtime (s)

6.45

7.85

23.20

28.32

32.11

35.89

38.28

43.13

47.43

All the reconstructions were performed on a laptop using a single GPU (see Supplementary Information for details). Of the 6.45 s and 7.85 s required for image reconstruction from a single
hologram intensity using sample-type-speciﬁc and universal neural networks, respectively, the deep neural network processing time is 3.11 s for the sample-type-speciﬁc network and 4.51 s for the
universal network, while the rest of the time (that is, 3.34 s for the preprocessing stages) is used for other operations such as pixel super-resolution, auto-focusing and free space back-propagation.

phase delay with respect to the background (where no cells are
present) is calculated to reveal the phase integral per RBC (given in
units of rad·μm2—see Supplementary Information for details), which
is directly proportional to the volume of each cell, V. In Figure 3a, we
compare the phase integral values of 127 RBCs in a given region of
interest, which were calculated using the phase images of the network
input, the network output, and the multi-height phase recovery image
obtained with Nholo = 8. Due to the twin-image and other self-
interference-related spatial artifacts, the effective cell volume and the
phase integral values calculated using the network input
image
demonstrated a highly random behavior. This behavior is shown as
the scattered blue dots in Figure 3a and is signiﬁcantly improved by
the network output, shown as the red dots in the same ﬁgure.

that

Next, to evaluate the tolerance of the deep neural network and its
holographic reconstruction framework to axial defocusing, we digitally
back-propagated the hologram intensity of a breast tissue section to
different depths,
is, defocusing distances within a range of
z = [ − 20 μm, +20 μm] with Δz = 1 μm increments. After this defo-
cusing, we then fed each resulting complex-valued image as input into
the same ﬁxed neural network, which was trained by using in-focus
images at z = 0 μm. The amplitude SSIM index of each network output
was evaluated with respect to the multi-height phase recovery image
with Nholo = 8 used as the reference (Figure 4). Although the deep
neural network was trained with in-focus images, Figure 4 demon-
strates the ability of the network to blindly reconstruct defocused
holographic images with a negligible drop in image quality across the
imaging system’s depth of ﬁeld, which is ~ 4 μm.

In a digital in-line hologram, the intensity of the light incident on

the sensor array can be written as

ð
I x; y

Þ ¼ A þ a x; y

ð

j

Þ

j2

¼ Aj

j2 þ a x; y
j

ð

j2 þ A
Þ

(cid:2)

ð
a x; y

Þ þ Aa

(cid:2)

ð

x; y

Þ

ð1Þ

Þ

where A is the uniform reference wave that is directly transmitted and
a(x,y) is the complex-valued light wave that is scattered by the sample.
Under plane wave illumination, we can assume that A has zero phase
at the detection plane, without loss of generality, that is, A = |A|. For a
weakly scattering object, the self-interference term |a(x,y)|2 can be
ignored compared with the other terms in Equation (1) because
a x; y
jooA. As detailed in our Supplementary Information, none
ð
j
of the samples that we imaged in this work satisﬁes this weakly
scattering assumption. More speciﬁcally,
the root-mean-squared
(RMS) modulus of the scattered wave was measured to be approxi-
mately 28%, 34% and 37% of the reference wave RMS modulus for
breast tissue, Pap smear and blood smear samples, respectively. This is
why, for in-line holographic imaging of such strongly scattering and
structurally dense samples, self-interference-related terms, in addition
to twin-image terms, form strong image artifacts in both the phase
and amplitude channels of the sample, making it difﬁcult to apply
object support-based constraints for phase retrieval. This necessitates
additional holographic measurements for traditional phase recovery
and holographic image reconstruction methods such as the multi-
height phase recovery approach that we used for comparison in this
work. Without increasing the number of holographic measurements,
our deep neural network-based phase retrieval technique can learn to

doi:10.1038/lsa.2017.141

Light: Science & Applications

Holographic reconstruction and phase recovery using neural networks
Y Rivenson et al

6

a

)
.
u
.
a
(

x
e
d
n

i

y
t
i
r
a

l
i

m
s

i

l

a
r
u
t
c
u
r
t
s
e
d
u
t
i
l

p
m
A

In focus

+4 μm
defocus

+10 μm
defocus

0.85

0.8

0.75

0.7

0.65

0.6

0.55

0.5

0.45

–25

–20

–15

–10

–5

5
0
Defocus distance (μm)

10

15

20

25

In focus

+4 μm defocoused
e

+10 μm defocoused
g

f

h

b

In focus
reconstruction
from 8 heights

20 μm

c

d

t
u
p
n

i

k
r
o
w
t
e
N

t
u
p
t
u
o
k
r
o
w
t
e
N

1

0

Figure 4 Estimation of the depth defocusing tolerance of the deep neural network. (a) SSIM index for the neural network output images when the input
image is defocused (that is, deviates from the optimal focus used in the training of the network). The SSIM index compares the network output images in d,
f and h, with the image obtained by using the multi-height phase recovery algorithm with Nholo = 8, shown in b.

separate/clean the phase and amplitude images of the objects from
twin-image and self-interference-related spatial artifacts, as illustrated
in Figures 1, 2, 3. In principle, one could also use off-axis interferometry55–57
to image strongly scattering samples. However, this would create a
penalty in the resolution or ﬁeld of view of the reconstructed images
due to the reduction in the space-bandwidth product of an off-axis
imaging system.

Another important property of this deep neural network-based
holographic reconstruction framework is that it signiﬁcantly sup-
presses out-of-focus interference artifacts, which frequently appear in
holographic images due to dust particles or other imperfections in
various surfaces or optical components of the imaging setup. These
naturally occurring artifacts are also highlighted in Figure 2f, 2g, 2n, 2o
with yellow arrows and cleaned in the corresponding network output
images of Figure 2d, 2e, 2l, 2m. From the perspective of our trained
neural network, this property to suppress out-of-focus interference
artifacts stems from the fact that these holographic artifacts fall into
the same category as twin-image artifacts due to the spatial defocusing
operation, helping the trained network reject such artifacts in the
reconstruction process. This is especially important
for coherent
imaging systems because various unwanted particles and features
form holographic fringes on the sensor plane and superimpose on the

object’s hologram, degrading the perceived image quality after image
reconstruction.

In this study, we used the same neural network architecture depicted
in Figure 1 and Supplementary Figs. S1–S2 for all object types, and
based on this design, we separately trained the convolutional neural
network for different types of objects (for example, breast tissue vs Pap
smear). The neural network was then ﬁxed after the training process to
blindly reconstruct the phase and amplitude images of any object of the
same type. If a different type of sample (for example, a blood smear
image) was used as an input for a speciﬁc network trained on a different
sample type (for example, Pap smear images), reconstruction artifacts
would appear, as exempliﬁed in Supplementary Fig. S6. However, this
does not pose a limitation because in most imaging experiments, the
type of the sample is known, although its microscopic features are
unknown and must be revealed with a microscope. This is the case for
biomedical imaging and pathology since the samples are prepared (for
example, stained and ﬁxed) with the correct procedures, tailored for the
type of the sample. Therefore, the use of an appropriately trained neural
network for a given type of sample can be considered well aligned with
traditional uses of digital microscopy tools.

We also created and tested a universal neural network that can
reconstruct different types of objects after its training, based on the

Light: Science & Applications

doi:10.1038/lsa.2017.141

Holographic reconstruction and phase recovery using neural networks
Y Rivenson et al

7

Sample-type-specific deep network

Universal deep network

Multi-height reconstruction from 8
holograms

Amplitude

Phase

Amplitude

Phase

Amplitude

Phase

a

g

m

50 μm

b

h

n

c

i

o

50 μm

d

j

p

e

k

q

50 μm

f

l

r

Figure 5 Comparison of the holographic image reconstruction results for the sample-type-speciﬁc and universal deep networks for different types of samples.
The deep neural network used a single hologram intensity as input, whereas Nholo = 8 was used in the column on the right. (a–f) Blood smear. (g–l)
Papanicolaou smear. (m–r) Breast tissue section.

layer

in each convolutional

same architecture used in our earlier networks. To handle different
object types using a single neural network, we increased the number of
feature maps
from 16 to 32
(Supplementary Information), which also increased the complexity
of the network, leading to increased training times. However, the
reconstruction runtime (after the network was ﬁxed) increased
marginally from approximately 6.45 s to 7.85 s for a ﬁeld of view of
1 mm2 (Table 2). Table 1 also compares the SSIM index values
achieved using this universal network, which performed similarly
object-type-speciﬁc
networks. A further
the
to
comparison
reconstructions
image
holographic
achieved by this universal network and the object-type-speciﬁc
networks is also provided in Figure 5, conﬁrming the same conclusion
as in Table 1.

individual

between

the

CONCLUSIONS
In this paper, we demonstrated that a convolutional neural network
can perform phase recovery and holographic image reconstruction
after training. This deep learning-based technique provides a new
framework in holographic image reconstruction by rapidly eliminating
twin-image and self-interference-related artifacts using only one
hologram intensity. Compared to existing holographic phase recovery
approaches, this neural network framework is signiﬁcantly faster to
compute and reconstructs improved phase and amplitude images of
the objects with less number of measurements.

MATERIALS AND METHODS
Multi-height phase recovery
To generate the ground truth amplitude and phase images used to
train the neural network, phase retrieval was achieved by using a
multi-height phase recovery method19,21,22. For this purpose, the
image sensor is shifted in the z direction away from the sample by

~ 15 μm increments 6 times and ~ 90 μm increment once, resulting in
8 different relative z positions of approximately 0, 15, 30, 45, 60, 75, 90
and 180 μm. We refer to these positions as the 1st, 2nd, …, 8th
heights, respectively. The holograms at the 1st, 7th and 8th heights are
used to initially calculate the optical phase at the 7th height, using the
transport of intensity equation (TIE) through an elliptic equation
solver52 implemented in MATLAB (Release R2016b, The MathWorks,
Inc., Natick, MA, USA). Combined with the square root of the
hologram intensity acquired at the 7th height, the resulting complex
ﬁeld is used as an initial guess for the subsequent iterations of the
multi-height phase recovery. This initial guess is digitally refocused to
the 8th height, where the amplitude of the guess is averaged with the
square root of the hologram intensity acquired at the 8th height, and
the phase information is kept unchanged. This updating procedure is
repeated at the 7th, 6th,..., 1st heights, which deﬁnes one iteration of
the algorithm. Usually, 10–20 iterations give satisfactory reconstruc-
tion results. However, to ensure the optimality of the phase retrieval
for the training of the network, the algorithm is iterated 50 times, after
which the complex ﬁeld is back-propagated to the sample plane,
yielding the amplitude and phase or real and imaginary images of the
sample. These resulting complex-valued images are used to train the
network and provide comparison images for the blind testing of the
network output.

Generation of training data
To generate the training data for the deep neural network, each
resulting complex-valued object image from the multi-height phase
recovery algorithm, as well as the corresponding single hologram
back-propagation image (which includes the twin-image and self-
interference-related spatial artifacts), is divided into 5 × 5 sub-tiles with
an overlap of 400 pixels in each dimension. For each sample type, this
results in a dataset of 150 image pairs (that is, complex-valued input

doi:10.1038/lsa.2017.141

Light: Science & Applications

Holographic reconstruction and phase recovery using neural networks
Y Rivenson et al

8

images for the network and the corresponding multi-height recon-
struction images), which are divided into 100 image pairs for training,
25 image pairs for validation, and 25 image pairs for blind testing. The
average computation time for the training of each sample-type-speciﬁc
deep neural network (which is done only once) was ~ 14.5 h, whereas
it increased to approximately 22 h for the universal deep neural
network (refer to Supplementary Information for additional details).
As an example, the progression of the universal network training as a
function of the number of epochs is shown in Supplementary Fig. S4.

Speeding up holographic image reconstruction using GPU
programming
As further detailed in the Supplementary Information, the pixel super-
resolution and multi-height phase retrieval algorithms are implemen-
ted in C/C++ and accelerated using the CUDA Application Program
Interface (API). These algorithms are run on a laptop computer using
a single NVIDIA (Santa Clara, California) GTX 1080 graphics card.
The basic image operations are implemented using customized kernel
functions and are tuned to optimize the GPU memory access based on
the access patterns of individual operations. GPU-accelerated libraries,
such as cuFFT58 and Thrust59, are utilized for development produc-
tivity and optimized performance. The TIE initial guess is generated
using a MATLAB-based implementation, which is interfaced using the
MATLAB C++ engine API, allowing the overall algorithm to be
maintained within a single executable after compilation.

Sample preparation
Breast tissue slide. Formalin-ﬁxed parafﬁn-embedded (FFPE) breast
tissue is sectioned into 2 μm slices and stained using hematoxylin and
eosin (H&E). The de-identiﬁed and existing slides are obtained from
the Translational Pathology Core Laboratory at UCLA.

Pap smear. De-identiﬁed and existing Papanicolaou smear slides
were obtained from the UCLA Department of Pathology.

Blood smear. De-identiﬁed blood smear slides are purchased from
Carolina Biological (Item # 313158).

CONFLICT OF INTEREST
The authors declare no conﬂict of interest.

1 Gerchberg RW, Saxton WO. A practical algorithm for the determination of phase from

image and diffraction plane pictures. Optik 1972; 35: 237.

2 Fienup JR. Reconstruction of an object from the modulus of its Fourier transform. Opt

Lett 1978; 3: 27–29.

3 Zalevsky Z, Mendlovic D, Dorsch RG. Gerchberg–Saxton algorithm applied in the

fractional Fourier or the Fresnel domain. Opt Lett 1996; 21: 842–844.

4 Elser V. Solution of the crystallographic phase problem by iterated projections. Acta

Crystallogr A 2003; 59: 201–209.

12 Rodriguez JA, Xu R, Chen CC, Zou YF, Miao JW. Oversampling smoothness: an effective
algorithm for phase retrieval of noisy diffraction intensities. J Appl Crystallogr 2013; 46:
312–318.

13 Rivenson Y, Aviv (Shalev) M, Weiss A, Panet H, Zalevsky Z. Digital resampling diversity
sparsity constrained-waveﬁeld reconstruction using single-magnitude image. Opt Lett
2015; 40: 1842–1845.

14 Gabor D. A new microscopic principle. Nature 1948; 161: 777–778.
15 Faulkner HML, Rodenburg JM. Movable aperture lensless transmission microscopy: a

novel phase retrieval algorithm. Phys Rev Lett 2004; 93: 023903.

16 Dierolf M, Menzel A, Thibault P, Schneider P, Kewish CM et al. Ptychographic X-ray

computed tomography at the nanoscale. Nature 2010; 467: 436–439.

17 Zheng GA, Horstmeyer R, Yang C. Wide-ﬁeld, high-resolution Fourier ptychographic

microscopy. Nat Photonics 2013; 7: 739–745.

18 Tian L, Waller L. 3D intensity and phase imaging from light ﬁeld measurements in an

LED array microscope. Optica 2015; 2: 104–111.

19 Misell DL. An examination of an iterative method for the solution of the phase problem in
optics and electron optics: I. Test calculations. J Phys D Appl Phys 1973; 6: 2200–2216.
20 Teague MR. Deterministic phase retrieval: a Green’s function solution. J Opt Soc Am

1983; 73: 1434–1441.

21 Paganin D, Barty A, McMahon PJ, Nugent KA. Quantitative phase-amplitude micro-

scopy. III. The effects of noise. J Microsc 2004; 214: 51–61.

22 Greenbaum A, Ozcan A. Maskless imaging of dense samples using pixel super-resolution
based multi-height lensfree on-chip microscopy. Opt Express 2012; 20: 3129–3143.
23 Rivenson Y, Wu Y, Wang H, Zhang Y, Feizi A et al. Sparsity-based multi-height phase

recovery in holographic microscopy. Sci Rep 2016; 6: 37862.

24 Wang H, Göröcs Z, Luo W, Zhang Y, Rivenson Y et al. Computational out-of-focus
imaging increases the space–bandwidth product in lensbased coherent microscopy.
Optica 2016; 3: 1422–1429.

25 Ferraro P, Miccio L, Grilli S, Paturzo M, De Nicola S et al. Quantitative Phase
Microscopy of microstructures with extended measurement range and correction of
chromatic aberrations by multiwavelength digital holography. Opt Express 2007; 15:
14591–14600.

26 Luo W, Zhang YB, Feizi A, Göröcs Z, Ozcan A. Pixel super-resolution using wavelength

scanning. Light Sci Appl 2016; 5: e16060; doi:10.1038/lsa.2016.60.

27 Gonsalves RA. Phase retrieval and diversity in adaptive optics. Opt Eng 1982; 21:

215829.

28 Eisebitt S, Lüning J, Schlotter WF, Lörgen M, Hellwig O et al. Lensless imaging of
magnetic nanostructures by X-ray spectro-holography. Nature 2004; 432: 885–888.
29 Rosen J, Brooker G. Non-scanning motionless ﬂuorescence three-dimensional holo-

graphic microscopy. Nat Photonics 2008; 2: 190–195.

30 Marchesini S, Boutet S, Sakdinawat AE, Bogan MJ, Bajt S et al. Massively parallel X-ray

holography. Nat Photonics 2008; 2: 560–563.

31 Popescu G, Ikeda T, Dasari RR, Feld MS. Diffraction phase microscopy for quantifying

cell structure and dynamics. Opt Lett 2006; 31: 775–777.

32 Coppola G, Di Caprio G, Gioffré M, Puglisi R, Balduzzi D et al. Digital self-referencing
quantitative phase microscopy by wavefront folding in holographic image reconstruc-
tion. Opt Lett 2010; 35: 3390–3392.

33 Wang Z, Millet L, Mir M, Ding HF, Unarunotai S et al. Spatial light interference

microscopy (SLIM). Opt Express 2011; 19: 1016–1026.

34 Rivenson Y, Katz B, Kelner R, Rosen J. Single channel in-line multimodal digital

holography. Opt Lett 2013; 38: 4719–4722.

35 Shechtman Y, Eldar YC, Cohen O, Chapman HN, Miao JW et al. Phase retrieval with
application to optical imaging: a contemporary overview. IEEE Signal Process Mag
2015; 32: 87–109.

36 Kelner R, Rosen J. Methods of single-channel digital holography for three-dimensional

imaging. IEEE Trans Ind Inform 2016; 12: 220–230.

37 Zuo JM, Vartanyants I, Gao M, Zhang R, Nagahara LA. Atomic resolution imaging of a

carbon nanotube from diffraction intensities. Science 2003; 300: 1419–1421.

38 Song CY, Jiang HD, Mancuso A, Amirbekian B, Peng L et al. Quantitative imaging of
single, unstained viruses with coherent X rays. Phys Rev Lett 2008; 101: 158101.
39 Miao JW, Ishikawa T, Shen Q, Earnest T. Extending X-ray crystallography to allow the
imaging of noncrystalline materials, cells, and single protein complexes. Annu Rev Phys
Chem 2008; 59: 387–410.

40 Loh ND, Hampton CY, Martin AV, Starodub D, Sierra RG et al. Fractal morphology,
imaging and mass spectrometry of single aerosol particles in ﬂight. Nature 2012; 486:
513–517.

41 LeCun Y, Bengio Y, Hinton G. Deep learning. Nature 2015; 521: 436–444.
42 Schmidhuber J. Deep learning in neural networks: An overview. Neural Netw 2015; 61:

5 Luke DR. Relaxed averaged alternating reﬂections for diffraction imaging. Inverse Probl

85–117.

2005; 21: 37–50.

43 Dong C, Loy CC, He KM, Tang XO. Image super-resolution using deep convolutional

6 Latychevskaia T, Fink HW. Solution to the twin image problem in holography. Phys Rev

networks. IEEE Trans Pattern Anal Mach Intell 2016; 38: 295–307.

Lett 2007; 98: 233901.

44 Rivenson Y, Gorocs Z, Gunaydin H, Zhang YB, Wang HD et al. Deep learning

7 Marchesini S. Invited Article: a uniﬁed evaluation of iterative projection algorithms for

microscopy. Optica 2017; 4: 1437–1443.

phase retrieval. Rev Sci Instrum 2007; 78: 011301.

8 Quiney HM, Williams GJ, Nugent KA. Non-iterative solution of the phase retrieval
problem using a single diffraction measurement. Opt Express 2008; 16: 6896–6903.
9 Brady DJ, Choi K, Marks DL, Horisaki R, Lim S. Compressive holography. Opt Express

2009; 17: 13040–13049.

10 Szameit A, Shechtman Y, Osherovich E, Bullkich E, Sidorenko P et al. Sparsity-based
single-shot subwavelength coherent diffractive imaging. Nat Mater 2012; 11:
455–459.

45 Jin KH, McCann MT, Froustey E, Unser M. Deep convolutional neural network for
inverse problems in imaging. IEEE Trans Image Process 2017; 26: 4509–4522.
46 Wang SS, Su ZH, Ying L, Peng X, Zhu S et al. Accelerating magnetic resonance imaging
via deep learning. Proceedings of the 13th International Symposium on Biomedical
Imaging (ISBI); 13-16 April 2016; Prague, Czech Republic. IEEE: Prague, Czech
Republic 2016doi:10.1109/ISBI.2016.7493320 .

47 Antholzer S, Haltmeier M, Schwab J. Deep learning for photoacoustic tomography from

sparse data. arXiv:1704.04587, 2017.

11 Candès EJ, Eldar YC, Strohmer T, Voroninski V. Phase retrieval via matrix completion.

48 Jo Y, Park S, Jung J, Yoon J, Joo H et al. Holographic deep learning for rapid optical

SIAM J Imaging Sci 2013; 6: 199–225.

screening of anthrax spores. Sci Adv 2017; 3: e1700606.

Light: Science & Applications

doi:10.1038/lsa.2017.141

Holographic reconstruction and phase recovery using neural networks
Y Rivenson et al

9

49 Sinha A, Lee J, Li S, Barbastathis G. Lensless computational imaging through deep

57 Goodman JW. Introduction to Fourier Optics. 3rd edn. Roberts and Company Publish-

learning. arXiv: 1702.08516, 2017.

ers: Greenwood Village, Colorado. 2005.

50 Bartels M, Krenkel M, Haber J, Wilke RN, Salditt T. X-ray holographic imaging of

hydrated biological cells in solution. Phys Rev Lett 2015; 114: 048103.

51 McNulty I, Kirz J, Jacobsen C, Anderson EH, Howells MR et al. High-resolution imaging

by Fourier transform X-ray holography. Science 1992; 256: 1009–1012.

52 Greenbaum A, Zhang YB, Feizi A, Chung PL, Luo W et al. Wide-ﬁeld computational
imaging of pathology slides using lens-free on-chip microscopy. Sci Transl Med 2014;
6: 267ra175–267ra175.

53 Nowlan SJ, Hinton GE. Simplifying neural networks by soft weight-sharing. Neural

Comput 1992; 4: 473–493.

54 Wang Z, Bovik AC, Sheikh HR, Simoncelli EP. Image quality assessment: from error
visibility to structural similarity. IEEE Trans Image Process 2004; 13: 600–612.
55 Lohmann A. Optische einseitenbandübertragung angewandt auf das Gabor-Mikroskop.

Opt Acta 1956; 3: 97–99.

58 cuFFT. NVIDIA Developer 2012. Available at https://developer.nvidia.com/cufft
(accessed on 9th April 2017) (The content in the link is not NVIDIA Developer).
59 Thrust-Parallel Algorithms Library. Available at https://thrust.github.io/ (accessed and

9th April 2017) (The content in the link is not NVIDIA Developer).

This work is licensed under a Creative Commons Attribution 3.0
Unported License. The images or other third party material in this

article are included in the article’s Creative Commons license, unless indicated otherwise
in the credit line; if the material is not included under the Creative Commons license, users
will need to obtain permission from the license holder to reproduce the material. To view a
copy of this license, visit http://creativecommons.org/licenses/by/3.0/

56 Leith EN, Upatnieks J. Reconstructed wavefronts and communication theory. J Opt Soc

Am 1962; 52: 1123–1130.

r The Author(s) 2018

Supplementary Information for this article can be found on the Light: Science & Applications’ website (http://www.nature.com/lsa).

doi:10.1038/lsa.2017.141

Light: Science & Applications

