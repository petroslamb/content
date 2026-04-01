Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35078

Roadmap on digital holography [Invited]

AND MASAHIRO

PIETRO FERRARO,7

ENRIQUE TAJAHUERCE,23

BAHRAM JAVIDI,1,* ARTUR CARNICER,2 ARUN ANAND,3
GEORGE BARBASTATHIS,4,5 WEN CHEN,6
J. W. GOODMAN,8 RYOICHI HORISAKI,9 KEDAR KHARE,10
MALGORZATA KUJAWINSKA,11 RAINER A. LEITGEB,12 PIERRE
MARQUET,13 TAKANORI NOMURA,14 AYDOGAN OZCAN,15
YONGKEUN PARK,16,17 GIANCARLO PEDRINI,18 PASCAL
PICART,19 JOSEPH ROSEN,20 GENARO SAAVEDRA,21 NATAN T.
SHAKED,22 ADRIAN STERN,20
LEI
TIAN,24 GORDON WETZSTEIN,8
YAMAGUCHI25
1Electrical and Computer Engineering Department, University of Connecticut, Storrs, CT 06269, USA
2Departament de Física Aplicada, Universitat de Barcelona, Barcelona, Spain
3Optics Laboratory, Applied Physics Department, Faculty of Technology and Engineering, The Maharaja
Sayajirao University of Baroda, Vadodara, India
4Department of Mechanical Engineering, Massachusetts Institute of Technology, Cambridge, MA 02139,
USA
5Singapore-MIT Alliance for Research and Technology (SMART) Centre, Singapore
6Department of Electronic and Information Engineering, The Hong Kong Polytechnic University, Hong
Kong, China
7CNR - Institute of Applied Sciences & Intelligent Systems, Pozzuoli (Napoli), Italy
8Electrical Engineering Department, Stanford University, Stanford, CA 94305, USA
9Department of Information Physics and Computing, Graduate School of Information Science and
Technology, The University of Tokyo, Tokyo, Japan
10Department of Physics, Indian Institute of Technology Delhi, New Delhi, India
11Institute of Micromechanics and Photonics, Warsaw University of Technology, Warsaw, Poland
12Center for Medical Physics and Biomedical Engineering & Christian Doppler Laboratory OPTRAMED,
Medical University of Vienna, Vienna, Austria
13CERVO Brain Research Center, CIUSSS de la Capitale-Nationale & Department of Psychiatry and
Neuroscience, Université Laval, Québec City, Québec, Canada
14Faculty of Systems Engineering, Wakayama University, Wakayama, Japan
15Electrical & Computer Engineering, University of California, Los Angeles, CA 90095, USA
16Department of Physics & KAIST Institute for Health Science and Technology, Korea Advanced Institute
of Science and Technology (KAIST), Daejeon, Republic of Korea
17Tomocube Inc., Daejeon, Republic of Korea
18Institute of Applied Optics ITO, University of Stuttgart, Stuttgart, Germany
19Laboratoire d’Acoustique de l’Université du Mans, CNRS 6613, Institut d’Acoustique-Graduate School
(IA-GS), Le Mans Université, Le Mans, France
20School of Electrical and Computer Engineering, Ben-Gurion University of the Negev, Beer-Sheva, Israel
213D Imaging & Display Laboratory, Universitat de Valéncia, Burjassot, Spain
22Department of Biomedical Engineering, Faculty of Engineering, Tel Aviv University, Tel Aviv, Israel
23GROC·UJI, Institut of New Imaging Technologies (INIT), Universitat Jaume I, Castelló, Spain
24Department of Electrical and Computer Engineering & Department of Biomedical Engineering, Boston
University, Boston, MA 02215, USA
25Tokyo Institute of Technology, School of Engineering, Kanagawa, Japan
*bahram.javidi@uconn.edu

Abstract: This Roadmap article on digital holography provides an overview of a vast array of
research activities in the field of digital holography. The paper consists of a series of 25 sections
from the prominent experts in digital holography presenting various aspects of the field on

#435915
Journal © 2021

https://doi.org/10.1364/OE.435915
Received 6 Jul 2021; revised 3 Sep 2021; accepted 4 Sep 2021; published 12 Oct 2021

© 2021 Optica Publishing Group under the terms of the Open Access Publishing Agreement. Users may use, reuse, and build upon the article, or use the article for text or data mining, so long as such uses are for non-commercial purposes and appropriate attribution is maintained. All other rights are reserved.Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35079

sensing, 3D imaging and displays, virtual and augmented reality, microscopy, cell identification,
tomography, label-free live cell imaging, and other applications. Each section represents the
vision of its author to describe the significant progress, potential impact, important developments,
and challenging issues in the field of digital holography.

© 2021 Optical Society of America under the terms of the OSA Open Access Publishing Agreement

1.

Introduction

Digital holography is a very broad field with numerous applications in bio-medicine, microscopy,
commercial electronics, entertainment, manufacturing, augmented and virtual reality, cyber
physical security, security and defense, etc. [1–210.] This Roadmap article provides an overview
of a vast array of research activities in the field of digital holography by 25 prominent researchers
in the field, including 210 references covering various aspects of this field.

After the publication of holography by D. Gabor in 1948 which lead to receiving a Nobel Prize
in 1971, a number of important holography related inventions occurred in the 1960s. E. Leith
work on off axis holography [2,3] had a substantial impact in making holography a much more
practical and popular discipline. The invention of laser made holography even more practical.
A. Lohmann’s introduction of computer generated holograms used computers to numerically
generate holograms to be printed and photographed for optical reconstruction [41,42]. In late
1960s, there was the invention of digital holography by J. W. Goodman who proposed using
electronic recording of holograms followed by numerical processing to reconstruct the object
digitally (see Section 2 on The Origins of Digital Holography) [4]. In the humble opinion of the
first author of this Roadmap article (B. Javidi), these later inventions on holography by Leith,
Lohmann, and Goodman were equally deserving of the Nobel Prize as they had profound impacts
on making holography what it is today, that is a popular technology with broad and significant
applications in many areas.

This Roadmap article discusses various aspects of the digital holography including the origins of
digital holography, self-referencing digital holographic microscopy, information security, lab-on-
chip holographic tomography, tomographic microscopy with randomly structured illumination,
automated disease identification by digital holography, label-free live cell imaging, digital
holography with machine learning, disordered optics for digital holographic imaging, SLM-based
incoherent digital holography, phase-distortion compensation in digital holography, off-axis
holographic spatial multiplexing, compressive sensing for digital holography, single-pixel digital
holography, holographic 3D reconstruction with multiple scattering models, machine-learning-
enabled holographic near-eye displays for virtual and augmented reality, integration of light-field
imaging and digital holography, and digital holography for macro industrial applications and
inspection.

The paper consists of a series of 25 sections from the prominent experts in digital holography
presenting various aspects of the field including sensing, processing, displays, augmented reality,
microscopy, and other applications. Each section represents the vision of its author to describe the
significant progress, potential impact, important developments, and challenging issues in the field
of digital holography. The sections are presented in alphabetical order. Table 1 presents the title
of each section and its corresponding author. The broad scope of digital holography is reflected in
the large number of publications, conferences, and scholarly, and industrial activities in the field
conducted across the globe in many international organizations in optics, engineering, medicine,
defense, and manufacturing. There are a substantial number of research and development groups
which are active in digital holography. Thus, as in any overview paper on a broad field such as
digital holography, it is not possible to include all active research groups, describe, and represent
all the possible applications, approaches, and activities in the field of digital holography. We
apologize in advance if we have neglected any relevant work, and left out any research groups or

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35080

publications. We hope that the large number of references cited in this article can be helpful in
covering many important aspects of this field.

Table 1.

Abstract and Conclusion

Introduction

The origins of digital holography

Bahram Javidi and Artur Carnicer

Bahram Javidi

Joseph Goodman

Self-referencing digital holographic microscopy

Arun Anand

What do we really “see” in a digital hologram?

George Barbastathis

Production of cylindrical vector beams by means of

Artur Carnicer

holographic techniques

Digital holography for optical security

Wen Chen

Lab-on-chip holographic tomography for flowing cells

Pietro Ferraro

Computational holographic imaging with randomness

Ryoichi Horisaki

and its applications

Digital holography for cell classification and automated

Bahram Javidi

disease identification

Need for standardization of phase estimation

algorithms in digital holographic microscopy

Kedar Khare

Holographic tomography in biomedical applications

Malgorzata Kujawinska

Digital Holography meets optical coherence

Rainer A Leitgeb

tomography

Label-free live cell imaging with digital holography:
towards phenotypic screening and personalized
medicine Approaches

Pierre Marquet

Single-shot digital holography with random phase

Takanori Nomura

modulation to reduce twin-image problem

Digital Holography in the age of machine learning

Aydogan Ozcan

Disordered optics for holographic display and imaging

YongKeun Park

Digital holography for metrology and industrial

Giancarlo Pedrini

inspection

Macro applications of digital holography for industrial

Pascal Picart

applications

SLM-based incoherent digital holography

Joseph Rosen

Phase-distortion compensation/removal in digital

Genaro Saavedra

holographic microscopy

Off-axis holographic spatial multiplexing

Compressive sensing for digital holography

Single-pixel digital holography

Natan T Shaked

Adrian Stern

Enrique Tajahuerce

Holographic 3D reconstruction with multiple scattering

Lei Tian

models

Machine-learning-enabled holographic near-eye

Gordon Wetzstein

displays for virtual and augmented reality

Integration of light-field imaging and digital

Masahiro Yamaguchi

holography

This section was prepared by Bahram Javidi.

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35081

2. Origins of digital holography

Before 1966, the field of digital holography did not exist. Starting in 1966, there was considerable
research by Lohmann [42] and his colleagues on computer-generated holograms, for which the
hologram was computed digitally and the image was obtained optically. Also in 1966, as the first
case of electronic detection of holograms, Enloe et al. [54] detected a hologram on a vidicon,
photographed the hologram from a CRT display, and reconstructed the image optically. An
additional relevant development, preceding those cited above by one year, was the publication by
Cooley and Tukey in 1965 [55] of the method now known as the fast Fourier transform.

In 1967, it occurred to me that, with suitable restrictions on the bandwidth of a hologram,
it should be possible not only to detect a hologram electronically but also to compute the
image digitally using the fast Fourier transform. The detector of choice in those days was the
ubiquitous vidicon widely used in TV. The computer available to us at the time was a DEC PDP-6
minicomputer. My colleague, R. W. Lawrence, programmed the FFT on the PDP-6. The results
were published in 1967 [4].

The vidicon had limited resolution, and therefore we decided on sampling the output in a
256 by 256 array, each sample having 8 gray levels. The recording geometry was the so-called
“lensless Fourier transform” geometry for which the reference wave originates as a point source
that is coplanar with the object. Such a geometry minimizes the resolution requirements for the
detector and allows the image intensity to be calculated by a simple Fourier transform, followed
by computing the squared magnitude of the result. The object was a transparent letter “P” on
an opaque background, illuminated through a diffuser to minimize the dynamic range in the
hologram. Computation of the image required 5 minutes on the PDP-6. While this computation
time actually compared favorably with the time required to develop, fix and dry such a hologram
recorded on film, it was too long for digital reconstruction to be widely used, and the resolution
of the vidicon was too limited to record more complex holograms.

Figure 1 (from Ref. [4]) shows (a) the electronically detected hologram, (b) the digitally
reconstructed image, and (c) an image of the same object obtained from a hologram recorded on
film and reconstructed optically. The coarse fringes in the hologram are due to second reflections
from a glass plate that covered the photosensitive portion of the vidicon. Both the digitally
reconstructed image and the optically reconstructed image contain speckle, a consequence of the
diffuser through which the object was illuminated.

Fig. 1. (a) Detected hologram, (b) Computed image, (c) Optically obtained image. Repro-
duced from J. W. Goodman and R. Lawrence, “Digital image formation from electronically
detected holograms,” Appl. Phys. Lett. 11, 77–79 (1967), with the permission of AIP
Publishing.

What were the developments that led to digital holography becoming the detection and
reconstruction method of choice today? Two technology developments were equally important.
The first is detector technology, for which CCD and CMOS detectors became dominant, primarily
due to the transition of photography from film to electronic-detectors. 100+ megapixel cameras
are readily available today, and their sensors can be used for holography. Such detectors are

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35082

capable of recording hologram samples in more than a 10,000 by 10,000 array, an amazing
improvement over the 256 by 256 vidicon-generated array.

Secondly, Moore’s law has improved the speed of computers by an incredible factor in the
nearly 55 years that have elapsed. What took 5 minutes on a minicomputer that cost $20,000 in
1966 now takes on the order of 10 msec or less on a home computer that costs a factor of 10 less
than the minicomputer.

While some display applications of holography are most effective when the hologram is
recorded on photographic plates or photopolymers, the two developments described above have
led to the almost complete replacement of film by electronic detectors when holography is
used in microscopy or other applications in which the hologram can be recorded in a small but
high-resolution format. Once the hologram exists in electronic form, it is natural to reconstruct
images digitally.

This section was prepared by Joseph Goodman.

3. Self-referencing digital holographic microscopy

Off-axis single-shot digital holographic microscopes (DHM) for cell imaging in transmission
mode generally employ Mach-Zehnder interferometer geometry [18]. It provides high-quality
quantitative phase images, which leads to the computation of optical thickness profiles of the
sample under investigation, resulting in the extraction of cell parameters used to identify them
[39,40]. However, the two-beam configuration used in Mach-Zehnder geometry requires optical
elements for beam splitting, steering, and combination, resulting in bulky devices and reduced
temporal stability [56]. Robust, compact, and low-cost digital holographic microscopes which
are immune to mechanical noise have the potential to act as point-of-care instruments for disease
diagnosis [57]. For sparse object distribution like thin blood smears, the part of the probe beam
not passing through cells can act as the reference (Fig. 2(a)), leading to off-axis self-referencing
digital holographic microscope configuration [39,40,56–58]. This yields compact instruments
with high temporal stability employing only a few optical elements. One of the easiest ways
to implement a self-referencing digital holographic microscope is to use a glass plate to create
two versions of the probe wavefront [39,40,56–59]. The reflected beam from the front or back
surface, not carrying object information, acts as the reference. This setup requires only a
glass plate and a magnifying lens to generate holograms. Another simple way to implement
a compact digital holographic microscope is by using a mirror to fold a portion of the object
wavefront back onto itself (Llyod’s mirror configuration), leading to off-axis geometry [58,59].
Lloyd’s mirror configuration allows adjustment of fringe density, depending upon the investigated
sample. Figure 2(b) shows the quantitative phase image of human erythrocytes imaged using
Lloyd’s mirror configuration [59], the quality of which is comparable to those obtained with
Mach-Zehnder configuration.

Self-referencing digital holographic microscopes yield many biophysical and bio-mechanical
cell parameters, which can train machine learning algorithms, and the trained model can diagnose
diseases with high accuracy [5]. Devices based on self-referencing geometry have the potential
for label-free cell classification and disease identification. Self-referencing configuration also
has the advantage of automatic path length matching, making them suitable for implementation
along with low temporally coherent sources like LEDs, opening up avenues for quantitative
phase imaging with exotic wavelengths. These microscopes can be constructed with off-the-shelf
optical and imaging components, leading to low-cost, hand-held, field-deployable devices. Such
devices will be suitable for point-of-care cell characterization and identification applications in
remote areas with limited healthcare facilities. The road ahead for this class of devices lies in
conducting field trials, generating more effective machine learning models, and extending their
application potential to other types of cells and tissues.

This section was prepared by Arun Anand.

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35083

Fig. 2. (a) Concept of Self-referencing Digital Holographic Microscope [6]. (b) Quantitative
phase images of human erythrocytes obtained using Lloyd’s mirror (wavefront division)
self-referencing Digital Holographic Microscope [7].

4. What do we really “see” in a digital hologram

It is often said that digital holography is a method to reconstruct the “complex amplitude” or “the
amplitude and phase” of the optical field. This is of course interesting in its own right, but we
often forget that the field itself seldom is what a practical user—say, a biologist—is looking for.
The goal of most practical imaging systems is to recover the geometry of objects that the light
has interacted with, including the objects’ three-dimensional shape and material composition:
for example, the shape of a biological cell, where the nucleus is located, etc.

The distinction between reconstructed wavefront and reconstructed object actually places
digital holography in sharp contrast with optical (or display) holography. In the latter, the
purpose is to create an illusion of three-dimensional appearance to a human viewer from the field
emanating from the planar hologram. Therefore, limiting design to capturing and recreating
optical fields is quite appropriate. In the former, digital case, however, we can and should be far
more ambitious.

Once we readjust our goal as reconstructing the object rather than the field, the immediately
next task becomes to assign the appropriate scattering model, or forward model. This maps a
3D refractive index distribution n(x, y, z) in object space to the scattered field ψ(x′, y′; x, y, z) and
from that to the interference pattern

I(x′, y′) = |ψref(x′, y′) + ψ(x′, y′; x, y, z)|2

(1)

on the digital camera coordinates (x′, y′). Here, ψref(x′, y′) is the reference wave. The choice of
forward model is consequential. To avoid excessive computation, we should choose a model
as simple as the object’s expected scattering strength permits, but no simpler. Possible choices
include scattering series [60] and the beam propagation method [61]. In a sense, we have just
reinterpreted the inverse problem associated with digital holography to

I(x′, y′) → n(x, y, z)

(2)

instead of the more customary I(x′, y′) → ψ(x′, y′) (see Fig. 3). The implications for regularizing
the inverse problem are substantial. For example, in many cases databases of valid or acceptable
objects are available. Finely tailored regularizing priors can then be learned, enabling the
I(x′, y′) → n(x′, y′) inversion in highly ill-conditioned situations, e.g. if n(x, y, z) consists of
high-contrast transitions or contains large gradients [62]; whereas comparable learning priors for
scattered fields, i.e. for the I(x′, y′) → ψ(x′, y′) problem, are generally more difficult to express.

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35084

Fig. 3. Scattering geometry for interpreting a digital hologram as a spatial modulation of
the index of refraction

It is an open research question whether it is better to solve the I(x′, y′) → ψ(x′, y′) problem
first, followed by ψ(x′, y′) → n(x, y, z) , as was done in [61] and requires formation of the
interference pattern; or to solve the I(x′, y′) → n(x, y, z) problem directly, as was done in [62]
from a slightly defocused version of the propagated intensity without use of a reference wave.
One benefit of the second approach is that it is straightforward to extend to partially coherent
fields (which is practical in the x-ray regime.) Lastly, similar arguments apply for augmenting the
object description with spectral and/or optical anisotropy descriptors, assuming the experimental
apparatus is designed to provide the relevant information.
This section was prepared by George Barbastathis.

5. Production of cylindrical vector beams by means of holographic techniques

The design and production of highly focused cylindrical vector beams has become a very active
research area. Nowadays, multiple research groups are developing theoretical frameworks and
practical applications in this field, producing a large amount of literature [63]. As a matter
Note that upon recombination, the polarization of the beam at each point of the wavefront is
determined by means of the modulus of the amplitudes and the phase difference. In this step no
interference is recorded. of fact, highly focused fields can be found in a variety of applications
such as optical trapping, laser machining, data storage and optical security just to cite a few [64]
Generally speaking, optical systems able to produce beams with arbitrary complex amplitude,
polarization and angular momentum share similar working principles: the beam is split in two
components with orthogonal polarization [65]. Each component is independently manipulated
and modulated using computer generated holograms displayed on spatial light modulators (SLM).
Then, the beam is recombined and subsequently focused using a high numerical aperture (NA)
objective lens. Note that upon recombination, the polarization of the beam at each point of the
wavefront is determined by means of the modulus of the amplitudes and the phase difference. In
this step, no interference is recorded.

The complex information to be displayed on the SLMs has to be previously calculated and
encoded. Depending on the modulation capabilities of the displays, the codification procedure
might differ. For instance, to encode complex values using a couple of phase-only modulators
might be straightforward. However, special computer-generated holograms (CGH) techniques
must be used when the optical setup implements cheaper phase-mostly transmissive displays [66].
The use of CGHs introduces several practical drawbacks: on the one hand, the transmittance T of

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35085

the display is relatively low (T ≤ 0.4) and on the other, the encoding procedure requires a certain
number of pixels to encode a single complex value. Figure 4 shows several examples of paraxial
beams (before focalization) with arbitrary irrad and ization generated with the setup described in
[67–69].

Fig. 4. Beams with arbitrary irradiance and polarization [66]: radially polarized and
star-like polarized Gaussian beams, azimuthally and radially polarized Laguerre-Gauss 01
beam and doughnut-like beam (adapted from [67]).

The four cases considered correspond to a radially polarized Gaussian beam (first column) a
star-like polarized Gaussian beam (second column); column three displays a Laguerre-Gauss
01 beam with radial polarization in the inner disc and azimuthal polarization in the external
ring. Finally, column four shows a doughnut-like beam with an intricate phase delay between
components. To demonstrate the behavior of the polarization, the beams have been recorded after
a linear polarizer set at 0◦, 45◦, 90◦ and 135◦. The last row (in gray level) represent the calculated
beams. The experimental images were recorded with an 8-bit CCD and displayed using the hot
color map. Once the paraxial beam has been prepared, it can be imaged on the entrance pupil of
a high NA objective lens. Nevertheless, recording such beams in full is not possible because of
the impossibility of capturing the longitudinal component using conventional cameras [68,69].

This section was prepared by Artur Carnicer.

6. Digital holography for optical security

Digital holography is able to record the whole field information of an object, and numerical
reconstruction can be implemented. Digital holography has been applied in many areas, e.g.,
optical security [70]. Digital holography-based optical security has been found to be a promising
approach for securing information, e.g., based on double random phase encoding [70]. Digital
holography-based optical security has an inherent nature of parallel processing, and possesses
multi-parameter and multi-dimensional capabilities. Many optical parameters can be generated
as security keys [70–72], and security and variety of digital holography-based optical encoding
have been continuously enhanced. Although attack algorithms [73] were developed to analyze
the vulnerability of digital holography-based optical security systems, there are always potential
strategies to withstand the attacks, e.g., real-time key updating.

Among the digital holography-based optical security technologies, computer-generated holo-
gram [70–72] has been developed as one of the most promising and effective approaches for
securing information, as schematically illustrated in Fig. 5. In the computer-generated hologram
based optical security, many iterative and non-iterative algorithms, e.g., Gerchberg-Saxton
algorithms, have been studied over the past decades to encode the data into amplitude-only or
phase-only computer-generated holograms which are used as ciphertext. A number of parameters

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35086

in optical setups, e.g., random phase-only patterns, can be flexibly employed as security keys.
An optical setup can be further designed and applied for real-time data display, when correct
security keys are used in the optical setup during the decoding.

Fig. 5. A flow chart for digital holography based optical security.

Although computer-generated hologram based optical security has a high potential to be widely
used in real applications and much progress has also been made, there are still many challenges
to be overcome.

Data encoding: Hologram generation speed, data encoding capacity and key space are always
challenging. Artificial intelligence, e.g., deep learning [74], can be investigated to pre-train the
data in order to rapidly generate the patterns (e.g., computer-generated hologram) as ciphertext.
Optical parameters, e.g., orbital angular momentum [75], can be manipulated to realize high-
capacity and high-security data encoding. Data encoding approaches can also be developed
to combine with metasurface technology rather than just by using spatial light modulators and
digital micromirror devices in order to explore the wider practical applications.

Data storage or transmission: In digital holography-based optical security, more studies can be
conducted to design an integrated system including data storage and transmission, e.g., intelligent
distributions of security keys and ciphertext [72,74]. The state-of-the-art 5G technology can also
be integrated for the transmission. More studies are also suggested to use digital holography
(e.g., computer-generated hologram) in the physical links or optical setups in a direct mode to
realize secure transmission, and high-speed generation of random numbers can also be studied
by using digital holography in the physical links or optical setups.

Data decoding and display: High-speed data decoding using an optical way is challenging.
The existing devices, e.g., spatial light modulators, have a relatively slow refresh rate [71,72].
Micro-electromechanical systems and phased array photonic integrated circuits can be studied and
designed to overcome the potential challenges. When metasurface is integrated, nanomaterials
and fabrication technology need to be studied for digital holography-based optical security.

This section was prepared by Wen Chen.

7. Lab-on-chip holographic tomography for flowing cells

Tomography is a significant tool capable to furnish a whole three-dimensional (3D) visualization
of an object, with its external and inner structures One of the next challenges in biomedicine is
to achieve personalized diagnosis at single cell level [76]. The perspective to analyze a great
number of cells would require high-throughput approaches at the aim to get meaningful statistics
and/or for searching rare cells in body fluids. In fact, in liquid biopsy it is necessary to detect
very few cells in body fluids (blood and urine) for detecting circulating tumor cells (CTCs).
Recently, the powerfulness of the digital holography (DH) has opened the route to such real-world
possibility. In fact, the intrinsic feature of DH to be a 3D imaging tool offers the very formidable
chance to accomplish such difficult task at lab-on-chip scale. From one side, DH has indeed the
ability to detect and track particles in a 3D volume with enough accuracy [77]. At the same
time, the know-how in using DH as interference microscope to visualize and present accurate
quantitative phase-contrast maps of single cells has been very well assessed in last ten years [78].
Furthermore, the last achievements in getting quite easily the full-tomograms in phase-contrast
modality for various types of cells while they are flowing along a microfluidic channel can allow

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35087

the envisaging that a holographic lab-on-chip technology can become a real clinic instrument in
the next future. The flow-cytometric set-up is schematically depicted in Fig. 6(a), in which cells
flow and rotate along a microfluidic channel while their “holographic fingerprint” is captured by
a DH off-axis system. In fact, cells are continuously probed by an object beam while them pass
through the field of view, thus multiple holograms at different viewing angles can be recorded
for each cell. By processing the recorded holograms, the time-lapse quantitative phase maps
(QPMs) can be obtained for each orientation of the cell [79], which in turn must be estimated
since the cell viewing/rolling angles are not a priori known [80]. Therefore, by combining all the
QPMs from all the directions and their estimated illumination angles, the 3D tomograms can be
retrieved [79]. A typical phase-contrast tomogram of an MCF7 cancer cell is shown in Fig. 6(b).

Fig. 6. Opto-fluidic holographic set-up (please note that the reference beam is not shown
for sake of simplicity) (a) and central slice of the 3D tomogram of an MCF-7 cell (b).

The results reported here are to date the only example of a way to get tomograms from flowing
cells in a microfluidic platform. The main advantage of the DH imaging tool is its label-free
property that, in addition to the 2D and 3D feature extraction, make it a very promising technology
for the cell discrimination based on truthful quantitative parameters. After 50 years from the
Gabor’s Nobel prize, holography seems to have a primary role in the future of biomedical
applications by making possible holographic flow-cytometry for single cell analysis. Of course,
next steps have to be pursued by using more strategies based on the use of artificial intelligence
[76,81] or even by exploring other sensing options like for example polarization as further
measurement probe [82].

This section was prepared by Pietro Ferraro.

8. Computational holographic imaging with randomness and its applications

Digital holography (DH) is a quantitative phase imaging technique for computationally recovering
complex amplitude information of specimens [4]. Most biomedical cells are transparent, and it is
difficult to observe them by conventional imaging based on light absorption. DH is promising
for imaging such biomedical targets without any staining because DH can detect not only the
amplitude but also the phase of optical fields. This is important in various biomedical fields,
such as regenerative medicine. One drawback of DH is the need to introduce reference light for
interferometric measurement of phase information. This makes the DH optical setup complicated
and limits the spatial or temporal bandwidth.

Another established quantitative phase imaging technique is coherent diffraction imaging
(CDI), where a complex-amplitude object is computationally recovered from a diffracted intensity
pattern. In CDI, reference light is not necessary, and therefore, the hardware setup is much simpler
than that of DH. This is important for imaging in non-visible regions, such as X-rays, where the

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35088

coherence lengths of light sources are short, making it difficult to implement an interferometric
setup. One issue with CDI is the limited field-of-view, which is called the support and is required
for the phase retrieval process. The support constraint can be alleviated by adopting a multi-shot
CDI modality with scanning of the support, a technique that is called ptychography. One issue
with ptychography, however, is the slow imaging speed.

To solve these issues in DH and CDI, we proposed and demonstrated a single-shot quantitative
phase imaging method by combining DH and CDI with a randomly coded aperture or randomly
structured illumination based on compressive sensing, as shown in Fig. 7 [83,84]. Our method
does not require interferometric measurement nor does it involve the support constraint. As a
result, our method realized single-shot quantitative phase imaging with a large field-of-view and
high spatial and temporal bandwidths with simple and compact optical hardware. Based on this
concept, we achieved single-shot diffraction tomographic microscopy with randomly structured
illumination generated by a diffuser inserted into the optical path in a conventional microscopy
system [85]. We have also extended this concept to single-pixel quantitative phase imaging [86].

Fig. 7. Computational holographic imaging with random modulation.

Randomness in computational imaging is important not only for quantitative phase imaging as
mentioned above but also imaging through scattering media. Speckle-correlation imaging is a
non-invasive method for imaging through scattering media. The shift-invariance of the point
spread functions of the scattering process, which is called the memory effect, is employed in
speckle-correlation imaging. We extended speckle-correlation imaging to depth imaging and
spectral imaging by using the axial and the spectral memory effects, respectively [87,88]. In
general, the calibration cost is an issue in conventional multidimensional imaging. Therefore,
our methods are important not only for non-invasive imaging through scattering media but also
for calibration-free multidimensional imaging with simple and low-cost optical hardware.

Computer-generated holography (CGH) is an optical control technique in which an interref-
erence pattern for reproducing an arbitrary optical field is calculated. CGH is promising for
three-dimensional displays, laser processing, and optical tweezers. The calculated holograms are
implemented with spatial light modulators (SLMs) for dynamical applications. CGH basically
requires iterative processes because SLMs cannot control the amplitude and phase simultaneously.
Therefore, achieving high-quality image reproduction with CHG requires a high computational
cost. We proposed a non-iterative CGH called deeply generated holography (DGH), which
employs a deep neural network for calculating holograms without iteration [89]. We demon-
strated more than 100-times faster hologram synthesis by three-dimensional DGH compared
with conventional CGH.

In summary, we presented recent advancements of computational imaging related to holography.
Information science has grown rapidly and has had an impact on various fields, including optics
and photonics. Technologies in information science, such as compressive sensing and deep
learning, have become important tools in computational imaging and have realized innovative
imaging methods for reducing the costs of hardware, software, calibration, etc., as mentioned
here. These imaging methods will contribute to a wide range of applications, such as life science,
security, and astronomy.

This section was prepared by Ryoichi Horisaki.

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35089

9. Digital holography for cell classification and automated disease identifica-

tion

This section describes an overview of digital holography for automated cell inspection and cell clas-
sification which may be used for automated disease identification [22,26,31,39,40,52,57,90–97].
This approach has been used for automated analysis and identification of malaria infected red
blood cells [39,40], sickle cell disease [57], cancer [96–98], bacteria [44,45,47,99,100], Stem
Cells [91], sperm cells [101], Rapid COVID-19 testing [93], etc. In my opinion, coupled with
advances in image sensors, numerical techniques, classification algorithms such as deep learning,
and 3D printing, this technique has great potential to inspect and classify micro-objects, cells
such as blood cells for automated disease identification. A brief history of the evolution of this
approach is provided in this section.

Following the invention of off axis holography [2,3], free space optical systems were extensively
studied for optical pattern recognition applied to mainly recognition of man-made objects in
scenes [41,43]. There was considerable global activity in optical pattern recognition R&D. Thus,
applying optical pattern recognition concepts to medical applications by treating biological cells
as objects to be recognized and inspected by optical systems was a promising approach [22].
However, cells are mainly transparent and the information of cell parameters is contained in
the spatial phase, index of refraction, and motility of the cells. Thus, conventional systems
as used in classical optical pattern recognition could not provide the precise measurement
of micro-organisms such as optical path length of cells or spatial phase to be used for cell
identification. The solution was to use digital holography or some form of optical sensing of
cells to capture the complex magnitude image of interaction of light with cells which we referred
to as opto-biological signature of the cells [22,52,90,91]. Digital holography provides a large
array of cell parameters such as cell morphology, complex magnitude of modulation of light by
cells, and the cell temporal dynamics or time variation. Starting in 2000, a series of papers were
published that proposed digital holography for 3D object recognition [11,12,16]. Then starting
in 2005, a series of papers were published that proposed digital holography for recognition of
biological cells and microorganisms [22,26,31,90,91] Since then, a variety of innovative optical
implementations, algorithms, and approaches on this subject have been reported by different
groups [39,44–50]. Notable in these activities are the contributions of A. Ozcan at UCLA by
introducing compact lensless digital holography for cell analysis [44,47], Y. Park at KAIST (S.
Korea) on working with quantitative phase imaging and algorithms for cell classification [45,46],
A. Anand at MS University of Baroda (India) by applying self-referencing holographic systems
to malaria identification and other conditions [39,40,50], I. K. Moon of DGIST (S. Korea) by
developing statistical algorithms for segmentation and identification in holographic systems for
cell analysis [39,49,52], and P. Marquet of Univ. Laval (Canada) for hematological and medical
applications of this approach [49]. There are reported applications on detection and classification
of various micro-objects, including micro plastic beads [94,102,103] that are not discussed due
to space limitation.

In cell classification based on digital holography, the opto-biological signature signal due to
the interaction of probe light and cells including cell motility is recorded by an image sensor
connected to digital hardware for numerical processing and pattern classification. A variety
of optical sensing arrangements and pattern recognition algorithms may be used such as deep
learning convolutional neural networks, statistical algorithms, and even correlation [57,90–95].
Figure 8 is an illustration of a cell identification system using a 3D printed compact field portable
self-referencing shearing holography [93,103].

Recently, a lensless cell identification system was proposed using pseudo random encoding of
the optical beam that propagates through the cells [see Fig. 8 (b)]. This approach can increase
the spatial resolution by removing the lens, and reduce size and cost of the sensor [94,95].

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35090

Fig. 8. (a) Optical configuration and (b) 3D-printed experimental system with dimensions
94 mm x 107 mm x 190.5 mm used for COVID19 testing [93]]. (c) A single random phase
encoding (SRPE) cell identification system. (d) 3D printed field portable compact system
for SRPE cell identification [94,95]. with dimensions of 50 mm x 125 mm x 160 mm.

The success of this approach should be further investigated by more extensive collaboration
between healthcare researchers and optical scientists and engineers. Large trials are needed to
have more reliable success rates. The instrument can be further optimized for consistent and
enhanced performance.

This section was prepared by Bahram Javidi.

10. Need for standardization of phase estimation algorithms in digital holo-

graphic microscopy

Digital holographic microscopy (DHM) is by now a mature technology [104,105]. Thousands of
research articles have been written on DHM system design, phase reconstruction algorithms and
potential applications of this modality to life sciences. Quantitative phase imaging is known to
be more sensitive compared to any amplitude (or intensity) based imaging in detecting small
changes in cell morphology. The ability of DHMs to image unstained cells using the natural
refractive-index contrast is unique as well. System cost is also not a roadblock anymore as
several low-cost DHM designs have been proposed by now. DHM community however needs to
ask why is it that typical researchers in life sciences are still not fully aware of the potential of

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35091

quantitative phase imaging and have not accepted it as a modality in its own right. While there
are a number of reasons for insufficient adaptation of this technology, going forward it will be
very important to make concerted efforts for standardization of DHM systems and reconstruction
methodologies. Quantitative phase estimation is inherently computational in nature and as a result
unless the algorithms are not benchmarked with common datasets, there is a high likelihood that
different system and algorithmic combinations may lead to different numerical phase estimates
for the same sample. This situation is highly undesirable in the current era when data driven
methodologies are being applied increasingly to applications like diagnostics.

From a practical standpoint of deploying a DHM in environments like clinics, single-shot
phase imaging systems have distinct advantage over those that use multi-step phase shifting
methodology. Traditionally, single-shot off-axis digital holograms are processed using the Fourier
filtering approach. This methodology inherently performs below the detector array capability due
to its low-pass filtering nature. However, a newer set of optimization methodologies [106,107]
can overcome this limitation and can provide full-diffraction-limited resolution performance
from single-shot image plane holograms. Figures 9(a)-(d) show a cropped bright-field image of
a cervical cell, its image plane hologram, the low resolution phase recovery using the Fourier
transform method (computed using the full hologram frame) and the superior higher resolution
region-of-interest phase reconstructions obtained via a sparse optimization approach from the
same hologram data. The optimization approach has also been shown to have noise advantage
[108].

Fig. 9. (a) Bright-field image of a cervical cell, (b) its cropped image plane hologram,
(c), (d) phase maps (unwrapped) recovered using Fourier filtering and sparse optimization
methods.

In addition to the basic phase reconstruction, a DHM system needs algorithms for fractional
fringe removal [109], phase unwrapping [110], and focusing of unstained samples. A user needs
to have clarity about what imaging performance to expect when employing a particular set of
algorithms and have a seamless experience like that with other common microscopy modalities.
Finally an important point that needs attention is that the life sciences researchers are currently
not in a position to interpret quantitative phase images. Correcting this situation needs larger
scale collective efforts that must go beyond publication of research articles. At present, individual
DHM research groups have their local collaborators in life sciences, but a DHM users’ consortium
needs to be formed which can take up standardization issues, so that, communication with life
sciences community as a whole becomes more effective. Overall the powerful quantitative phase
imaging technology must be made accessible to a large number researchers in life sciences to
enable exciting new science and applications in future.

This section was prepared by Kedar Khare.

11. Holographic tomography in biomedical applications

Holographic tomography (HT) is an advanced quantitative 3D phase imaging method which
enables non-invasive and high resolution examination of biological samples based on their
refractive index (RI) 3D distribution. HT can be achieved by different approaches such as sample

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35092

rotation (SR), illumination beam rotation (BR) and integrated, dual mode tomography (IDMT)
[111]. Although IDMT provides the best object spatial frequency coverage resulting in the high
and isotropic accuracy of the reconstructed 3D RI [111], BR is considered as the best candidate
for biomedical applications. BR approach has been implemented in numerous research and
commercial limited angle holographic tomography systems (LAHT) based on Mach-Zehnder
interferometer configuration. In LAHT the specimen is stationary, while holographic projections
are acquired for different object illumination directions This makes it a perfect tool for measuring
single biological cells, cell cultures and tissues directly at Petri dishes or microscopic slides.
After all data is captured, specialized tomographic reconstruction algorithms are employed to
retrieve 3D refractive index (RI) distribution. Because RI values depend on the number of
intracellular biomolecules, LAHT allows label-free quantitative 3D morphological mapping
of biological specimens. The main drawbacks of LAHT are so called missing-cone artifacts
(MCA) that are present due to limited angular coverage of acquired projections. These artifacts
include: underestimated RI values, distorted 3D geometry and highly anisotropic resolution
of the calculated results [111,112]. Also, several technical issues, such as a small holographic
field-of-view (FoV) and image degradation due to multiple light scattering, have hindered 3D
RI-based applications such as histopathological analyses of tissues [113]. Therefore current
research development of LAHT methods is mainly focused on two aspects: better correction of
missing-cone artifacts leading to increase of measurement accuracy in full volume and broadening
of LAHT applicability to cover numerous biomedical needs [112].

From the hardware point of view LAHT systems will utilize solutions that allow to understand
the living world in its complexity taking into account multi-spatial-temporal scales [113]. The
measurements of large FoV, either by using low magnification objectives with support of
numerical processing to increase the resolution or by incorporating motorized stages supported by
3D stitching methods will be further enhanced. LAHT setups are more and more incorporating
fluorescence and polarization modes which allow to draw new conclusions from obtained
results by correlating 3D reconstructions acquired with different modalities [111,114]. Also by
combining LAHT imaging with full-field optical coherence tomography, an increased spatial
frequency coverage and/or in-vivo imaging can be potentially obtained [115].

The main challenge in 3D RI reconstruction process is development of algorithms that are
more effective in minimization of missing-cone artifacts and at the same time are fast enough
to allow quasi-real-time data processing. Here, the solutions based on artificial intelligence
(AI) play the key role [46]. However, the results from existing AI algorithms suggest that the
ultimate solution for reduction of MCA will combine deep-learning and traditional reconstruction
methods. AI can also be used for effective data processing including 3D image segmentation and
digital staining based on 3D RI distribution (including birefringence). This will allow to generate,
rapidly and label-free, a molecular image of a biological sample. Also AI based solutions will
bring us closer to overcome the multiple scattering limitation and open LAHT to volumetric
analysis of organoids and thick tissue slices enabling 3D digital phase histopathology [46].

The biggest challenge for commercialization of LAHT in the coming years is strengthening of
its position as the method that allows fast and truly quantitative analysis of 3D samples [116]. This
can be obtained through standardization of metrological validation process of different LAHT
systems including widespread utilization of metrologically tested and standardized 3D-printed
phase microphantoms [112,116] (Fig. 10). This would also support cross-referencing of the
results between laboratories and their reliable usage for diagnostics, pharma and other biomedical
applications.

This section was prepared by Malgorzata Kujawinska.

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35093

Fig. 10. Metrological validation of tomographic reconstruction algorithms and systems:
a) the cell-like phantom (adapted from [116]) and b) crossections of its refractive index
distribution reconstructed by direct inversion (DI) method and Gerchberg-Papoulis algorithm
with the finite object support constrain (MASK) [112].

12. Digital Holography meets optical coherence tomography

Optical Coherence Tomography (OCT) exploits the short temporal coherence of broad bandwidth
light for axial signal gating. It has become a gold standard in ophthalmology for non-invasive and
contact free probing of retinal fine structure in depth, and finds increasing interest also in other
medical areas. Both, holography and OCT are interferometric techniques, being different in that
holography relies on the spatial coherence of light rather than the short temporal coherence used
in OCT. This theoretical distinction however starts to blur when OCT is performed in parallel.
OCT can be distinguished into time domain (TD) and Fourier domain (FD) OCT. In TD OCT, a
reference arm is scanned probing different sample depths within the axial coherence gate. In a
full field (FF) OCT configuration each pixel of a 2D sensor records the local interference pattern.
In order to distinguish the interferometric signal part, that encodes the sample structure, from
the depth independent backscattered intensity, two strategies are followed. They are similar
to in-line versus off-axis digital holography. For the in-line configuration, the reference arm
mirror is mounted on a phase stepping device such as a piezo actuator, and several images are
recorded for each reference arm delay (or sample depth), with defined phase step [118]. The
off-axis configuration on the other hand allows for single image recording and subsequent spatial
frequency filtering of the depth gated OCT signal. In off-axis line field (LF) TD OCT a line is
scanned across the sample and the interference signal is recorded in parallel by pixels of a line
sensor (Fig. 11). Such configuration has been chosen for high speed optical elastography of the
human cornea recording mechanical surface oscillations with a bandwidth up to 100kHz [119].
Another paper demonstrated high resolution retinal imaging as well as blood flow imaging in
retinal capillaries [117]. The challenge of TD OCT is to keep track of the axial position of the
coherence gate in axially moving samples such as the human eye in-vivo. Retrospective axial
correction has been applied for a highly compact system that is commercialized for home care
use [120]. FD OCT on the other hand records the interferometric signal as a function of optical
frequency. LF and FF FD OCT have been realized in off-axis configuration for high resolution
human retinal imaging [121,122]. The line field variant has the advantage over full field OCT of
exhibiting in addition to the coherence gate a half confocal gate. The missing confocal gate in FF
OCT results in loss of contrast due to scattering cross talk in opaque media. By breaking the
spatial coherence of the illumination light it is possible to reduce the scattering cross talk even for
FF OCT systems [123]. Parallel OCT systems are particularly interesting because they share with
holography an intrinsic excellent phase stability in the enface plane. Photoreceptor responses to
optical stimulation in the living retina have been assessed, by sensing nanometer changes in living
cells exploiting the phase of the recorded interferometric signal [122]. Novel dynamic contrast
schemes based on smallest signal changes between successive recordings allow to differentiate
tissue or cells based on their metabolic activity [118]. The available sample phase has equally

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35094

been exploited for extracting wavefront errors from recorded OCT images, and for correcting
those aberrations by phase conjugation in the pupil or Fourier plane, all done in postprocessing.
With digital aberration correction, high resolution cellular retinal details could be revealed by
OCT in vivo, otherwise only visible with expensive adaptive optics equipment [124] (Fig. 11). It
is expected that holographic techniques will in the near future find their way into commercial
OCT devices, enhancing their diagnostic capabilities in both resolution and contrast.

Fig. 11. In-vivo holographic LF OCT of human retina with off-axis reference arm and digital
aberration correction: (a) original recorded en-face image with fringe data; (b) 2D Fourier
transform of (a) showing shifted cross-correlation terms; (c) Spatially filtered axially gated
OCT reconstruction of photoreceptor layer; (d) 2D Fourier transform of (c); (e) Digitally
aberration corrected image by phase conjugating the extracted wavefront error shown in (g)
in the Fourier or pupil plane; (f) 2D Fourier transform of (e) exhibits a Yellot’s ring (arrow)
due to the recovered cone photoreceptor pattern; Zoom in’s (I) and (II) demonstrate the
contrast and resolution gain after digital correction; scale bars are 200µm adapted from [117]

This section was prepared by Rainer A. Leitgeb.

13. Label-free live cell imaging with digital holography:
screening and personalized medicine approaches

towards phenotypic

Digital holography (DH) has developed dramatically over the last 20 years, thanks in particular to
both the availability of inexpensive digital image sensors with a high pixel number of small size
(between ∼ 1µ and ∼ 10µ as well as the increase in computing power allowing to easily process
digital images of several megapixels. Numerical processing of such digital holograms has led to
the amazing possibility to retrieve the whole complex wavefront scattered by a specimen, which
provides unique information on the latter, especially when biological cells are concerned.

Indeed, most of biological cells as transparent specimens differing only slightly from their
surroundings in terms of optical properties (including absorbance, reflectance, etc.). The phase
information, contained in this complex scattered wavefront, represents thus an intrinsic contrast to

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35095

visualize living cells without any staining as stressed by the Phase contrast (PhC) and Normarski’s
differential interference contrast (DIC) microscopy as well as interference microscopy, techniques
developed in the mid-twentieth century. PhC and especially DIC producing very high-quality
and high-resolution images are widely used in biology although they do not provide quantitative
measurements of the phase retardation induced by the specimen on the transmitted light wave.
For its part, interference microscopy provides quantitative phase imaging (QPI) at the cost of
demanding opto-mechanical designs preventing its use on a large scale in biology.

In contrast, DH, thanks to the numerical calculation of the phase information from holograms,
has allowed the development of a large number of QPI approaches from very simple experimental
set-ups. This has led to the development of numerous applications including cell culture
inspection [125], automated cell counting, recognition, classification and analysis for diagnostic
purpose [126] with the use of machine learning approaches [98], or aiming at assessing cellular
responses induced by new drugs particularly in the field of oncology [127]. These various
applications have paved the way to develop very attractive diagnostic approaches at the point of
care knowing that DH makes it possible to consider compact and portable set-ups [99].

On the other hand, the ability of numerical propagation to apply autofocusing and extended
depth of focus has made possible efficient semen analyses, including freely swimming human
sperm cell exploration, which represents appealing developments in the field of fertility medicine
[128].

DH is also a promising technology to achieve label-free high content screening (HCS)
approaches [129]. Indeed, HCS, in combination with stem cell technologies, is widely used today
in particular in the field of drug discovery through the design of phenotypic cellular assays (i.e.
based on automated quantitative analysis of a large number of data characterizing cells changes
within a population) to identify mechanisms, pathways and targets that have therapeutic potential.
All these various promising and exciting applications in the field of cellular imaging are based
on the capacity of DH to provide quantitative phase images, in a simple and robust way. This
aspect of quantitative phase is often put forward to claim the advantage QPI over the more
traditional approaches including PhC and DIC. It is quite true that the quantitative phase signal
(QPS) could provide information about highly relevant cellular parameters including dry mass,
intracellular refractive index and thickness making it possible to measure the absolute cell volume.
However, most of these cellular parameters are entangled with each other in the QPS. On the
other hand, identifying specific cellular phenotypes, that are the expression of many biological
processes and pathways requires to be able to perform a characterization through the analysis of
many different cellular parameters, such as morphometry, volume and its changes, viscoelasticity
and deformability, membrane fluctuation, transmembrane water fluxes, etc. Therefore, exploiting
the great potential offered by these label-free QPI techniques, based on DH or not, in attractive
fields such as diagnostics and personalized medicine or high-content screening for drug discovery,
definitely needs the developments of efficient approaches to extract from QPS a large set of
cellular parameters.

This section was prepared by Pierre Marquet.

14. Single-shot digital holography with random phase modulation to reduce

twin-image problem

In-line digital holography can be realized by a simple configuration and is robust against
disturbance. However, a twin image should be removed to achieve a high-quality image. Here, a
twin-image reduction method using a diffuser for phase-imaging in-line digital holography is
described. The proposed twin-image reduction is categorized into computational optical sensing
and imaging. It is inspired by a double-random phase-encoding optical encryption [9,70]. In
the literature [130], though a coherent light source such as a laser was used, we show that it
is valid for a low-coherent light source such as an LED. The schema of the single-shot digital

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35096

holography with random phase modulation is shown in Fig. 12(top) It is assumed that a specimen
is a weak phase object and its extent is small enough compared with the reference beam. In
this method, an object wave is modulated by a diffuser, and a reference wave is not. A digital
hologram is obtained by interference between modulated object wave and unmodulated reference
wave. Signal processing with the phase modulation obtained in advance enable us to diffuse only
the twin image on a reconstructed plane. Therefore, we can obtain a phase distribution of the
object beam, where the effect of the twin image is reduced.

Fig. 12. Top: Schema of an optical setup for single-shot digital holography with random
phase modulation. Bottom: Experimental results: (a) a phase object as a specimen, (b) a
retrieved phase distribution with a laser, and (c) a retrieved phase distribution with an LED.

In the experiment, two phase-only spatial light modulators were used for the specimen and the
diffuser. The phase specimen is shown in Fig. 12(bottom, a). A green laser with a wavelength
of 532 nm and a green LED with a central wavelength of 523 nm were used for coherent and
low-coherent light sources, respectively. The full-width at the half-maximum of the wavelength
of the LED was 40 nm. The retrieved phase distributions are shown in Fig. 12(bottom, b) and
12(bottom, c )by using a laser and an LED, respectively. You can see phase distribution with less
twin images in both figures. For an LED, owing to the less speckles, the image quality was better
than that of a laser. The use of an LED makes it possible to realize a compact optical system. It
might be portable on site.

This section was prepared by Takanori Nomura.

15. Digital holography in the age of machine learning

Among many areas of science and engineering, modern machine learning methods, in particular
deep learning and neural networks, have also enabled a remarkable transformation in the way
that holograms are digitally processed and reconstructed [133,134]. In addition to their earlier
success in e.g., image classification and segmentation of features etc., deep neural networks and
data-driven training and statistical learning methods have enabled powerful solutions to phase
recovery problems in holography, creating faster and better numerical approaches for holographic
image reconstruction from intensity only-recordings [133]. Using these modern machine learning

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35097

methods, reconstruction of a monochrome hologram with the spatial and spectral contrast of
brightfield imaging (Fig. 13(a)), eliminating various forms of speckle and interference artifacts,
while also providing color information, has become possible [131]. In this case that is highlighted
in Fig. 13(a), a deep neural network was trained using the generative adversarial network (GAN)
framework through a set of 3D registered image pairs, where the inputs were created by the
holograms of samples digitally back-propagated to various depths (without any phase retrieval
step) and the ground truth images of the same samples were acquired by a 3D scanning brightfield
microscope at the exact corresponding depths. After this training phase, which is a one-time effort,
the generator neural network can virtually create the brightfield equivalent image of a sample on
any axial plane by using a single hologram that is back-propagated to the corresponding plane.

Fig. 13. Deep learning-enabled cross-modality image transformations in digital holography.
(a) A trained deep neural network is used to reconstruct holograms with the spatial and color
contrast and axial sectioning capability of a brightfield microscope. BP refers to digital
wave back-propagation. Adapted from Ref. [131]. (b) A trained deep network is used to
virtually/digitally stain a label-free (unstained) human tissue section using a reconstructed
hologram as its input; the output image virtually achieves the same staining color and image
contrast as the actual histochemically stained tissue section. Adapted from Ref. [132].

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35098

Stated differently, only one hologram intensity can be used to virtually generate, through the
trained neural network, a 3D stack of brightfield equivalent images of the sample. This approach
is referred to as “Brightfield Holography” [131] since it combines the single-shot volumetric
imaging capabilities of holography with the speckle- and artifact-free image contrast and axial
sectioning ability of brightfield microscopy. Figure Fig. 13(a) exemplifies the performance of this
deep learning-enabled virtual brightfield holography system for 3D imaging of pollen particles.
This unique capability of cross-modality image transformations enabled by deep neural networks
has opened up various new opportunities and applications in biomedical imaging that were not
possible before, such as the virtual staining of label-free tissue samples using holographic images
(see Fig. 13(b)) [131]. These rapid advances in digital holography, together with the economies
of scale brought by e.g., consumer electronics and digital cameras, especially in mobile phones,
have also enabled a transformation in holographic imaging and sensing instruments, making
them both field-portable and cost-effective, which provide ideal platforms for high-throughput
and sensitive screening of large sample volumes even in resource limited settings [100,135,136].

This section was prepared by Aydogan Ozcan.

16. Disordered optics for holographic display and imaging

Digital holographic display would be an ultimate form of three-dimensional (3D) display because
it controls the amplitude and phase information of light in real-time and can overcome the
vergence–accommodation conflict. However, one of the major technical challenges of the current
digital holographic display is the limited space bandpass range–the product of an imaging size
and a viewing angle range is fixed and determined by the total number of controllable optical
modes (e.g., the pixel number of a spatial light modulator (SLM)).

Several approaches have been proposed to overcome this limited space bandpass range using
spatial or temporal multiplexing, and metamaterials [137] (see Fig. 14). Disordered optics are
exploited to demonstrate the simultaneous increase of both the imaging size and viewing angle
range [138]. The demonstrated holographic display device was composed of a SLM and optical
diffusers placed after the SLM. Once the optical transmission matrix (TM) of the diffusers, which
describes the light transport through an optical system, were measured, the combination of the
SLM and diffusers significantly increased the space bandpass range. However, the method had
limitations: the measurement of the TM should be performed repeatedly for calibration; the
size of the system was bulky. To overcome these limitations, a pinhole array was fabricated and
utilized as an engineered diffusor, which was directly attached to a liquid crystal display unit
for a compact size [139]. The technique also does not require the time-consuming calibration,
because the information about the pinholes was readily known, and thus the TM can be directly
calculated. Furthermore, the approach can be extended to scalable production. Nonetheless, the
limited number of controllable optical modes and coherent speckle noise prevent from generating
image quality compatible to commercial-grade display.

Since displaying and imaging can be understood as time-reversal analogy, the techniques
developed in the holographic display can also be applied to holographic imaging [140]. Once
the TM of a scattering layer was measured, it can be used as an optical lens [141]. Exploiting
the generation of nearfield by multiple light scattering, imaging beyond diffraction limit was
demonstrated [142]. A scattering lens can be used to achieve high-resolution imaging while
maintaining a long working distance. However, the calibration of a diffusor – or the measurement
of the TM of the diffusor – generally requires an interferometric imaging system with systematic
illumination control. Recently, the speckle-correlation scattering matrix (SSM) was developed
[143]. Without using interferometry, light transport through a diffusor is characterized using
simple intensity measurements. The SSM has been exploited for holographic camera and
microscopic imaging and demonstrated potentials for imaging 3D objects with high spatial

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35099

Fig. 14. Illustration of (a) conventional holographic imaging, (b) holographic imaging with
disordered optics, (c) conventional holographic display, and (d) holographic display with
disordered optics

bandwidth ranges. Practical 3D holographic display and camera are yet to come but will be
realized with the advances in photonics and engineered materials.

This section was prepared by YongKeun Park.

17. Digital holography for metrology and industrial Inspection

Digital holography relies on interference and is very sensitive to the environmental conditions
(vibrations, unwanted deformations, and temperature). In order to allow its application in industry
it is necessary to reduce the time of acquisition of the digital holograms. Pulsed lasers were
used for hologram recordings, the short pulse length (few nanoseconds) and the possibility of
recording two or more holograms in a short time (microseconds) allow measurements of vibrations
[144–146] or strong dynamical deformations (e.g. shock caused by impact). Figure 15(a) shows
the result of the measurement of a round plate (diameter 15 cm) vibrating with a frequency of 4800
Hz. The vibration shape (right) is obtained by unwrapping a phase map (left) calculated from the
phase difference of two holograms recorded with a temporal separation of 10 microseconds.

The increasing trends towards miniaturization in many different application fields, from optical
communications to medicine, have produced in the past few years a dramatic progress in the
development of micro-electro-mechanical systems (MEMS) and micro opto-mechanical systems
(MOEMS). Digital holography is well suited for the measurement of MEMS and MOMS, it was
shown [147] that it can be used for characterization of in-plane and out of plane movements
of micro devices with accuracies in the nanometer range. Figure 15(b) shows an out-of-plane
movement measurement of a micro device. By recording holograms sequences during the
movement of the devices, it is possible to retrieve time resolved deformations.

Another application of digital holography is the residual stress analysis in industrial environment.
In Ref. [148], it was shown that the residual stresses inside coated surfaces can be determined.
A notch is drilled by using a pulsed laser and the 3D deformation around it is measured. The
residual stresses are determined from the deformations using FEM calculations. The method
works well even when the surface to be investigated has high temperature. Figure 15(c) shows
two phase-maps obtained from holograms recorded during the deformation of the surfaces at the
temperatures of 24 ◦C and 215 ◦C, respectively.

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35100

Fig. 15. (a) Measurement of a vibrating plate, adapted from Ref. [146]; (b) Out-of-plane
movement measurement of a MEMS, adapted from Ref. [147]; (c) Measurements of coated
samples at room and high temperatures, adapted from Ref. [148]; (d) Shape measurement of
a tungsten sample located at a distance of 23 m, adapted from Ref. [150].

The shape of a sample can be retrieved from holograms recorded at different wavelengths
[149,150]. Figure 15(d) show the measurement of a tungsten sample located at a distance of 23
m from the measuring system. This shows that long distance shape measurements can be carried
out by two wavelengths digital holography. This section was prepared by Giancarlo Pedrini.

18. Macro applications of digital holography for industrial applications

Holography is a very powerful method for metrology, both at the micro and macro scales [151].
Holographic phase imaging measures the optical path length related to the scene/object/structure
of interest and the relevant data is a wrapped modulo 2π phase that can be advantageously used for
several industrial purposes: roughness measurements [152], surface shape profiling [153], surface
deformation [154] or vibration measurements [155]. The method of holographic interferometry
has the advantage of being contact-less, non-intrusive by the use of light illumination but also
provides full-field measurements. With the advent of very high-speed sensors, high temporal
resolution can be obtained [155]. Thus, the approach is adapted to investigate fundamental
properties of transient mechanical waves propagating in complex metamaterials [156]. The recent
advent of long wavelength infrared digital holography allows large deformation measurements,
which are of interest for wide-field investigations [157]. In addition, such advances desensitize
holographic measurement since the wavelength is increased by a factor of almost 20 [154].

For the past 10 years, artificial intelligence (AI) and deep learning based on convolutional neural
network has emerged as very efficient tools in signal and image processing with applications in
speech and language understanding, or image recognition. It has now impacted digital holography
for computer-generated holograms [158] and phase de-noising in holographic interferometry
[159]. Deep learning will probably strongly influence digital holography and its related post
processing approaches in the near future.

Despite significant progress in the understanding and modeling of the image-to-object
relationship in holographic imaging, digital holographic interferometry is limited by the processing
chain and by limited spatial resolution and phase resolution. The use of digital holography in
industrial applications requires the ability to process data very quickly [153]. Whereas classical

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35101

unwrapping and de-noising algorithms [160] are powerful, they are not fast enough for industrial
purposes. One promising possibility includes AI with predictive signal and noise models based
on prior on the underlying phenomena to speed up unwrapping and noise reduction techniques.
The gains in de-noising performance and speed will consequently improve the phase resolution
limits below the nanometer range. New processing schemes will have to be evaluated with
normalization procedures and the constitution of large and evolutionary data bases. Currently,
digital holographic interferometry lacks spatial resolution, especially for high-speed acquisitions
because the number of pixels is reduced to achieve high frame rates. Consequently, holographic
interferometry mixed with super resolution approaches could bridge the gap to improve the
spatial resolution of the processed data. That will also increase the dimensions of the inspected
area. One feature of digital holographic interferometry is to provide huge amount of data. That
means that the rapid exploitation of output data will require the use of techniques of massive data
mining, which are to be developed for digital holography.

Holographic metrology has the potential to challenge many future industrial applications.
As a non-destructive testing method, its performance will be improved by coupling its outputs
with AI and data on defects. The simultaneous acquisition of tridimensional deformation/strain
fields at high frame rates will be of great interest for mechanical engineering. The demands
for environmental noise control, transportation, heat control/recycling, clean electrical energy,
pollution and risks (such as industrial explosions) require real-time characterization and control
of tridimensional complex flows coupled with acoustic phenomena. Potentially, this could also
impact other sectors such as sound zone control and new electric vehicles which demand default
diagnostic that are different than internal combustion engine. In the same way, the full in-situ
control of additive manufacturing processes for better diagnostic fabrication defaults and potential
failures is a great opportunity for holography. For future extraterrestrial missions which will
have increasing importance, considering the huge amount of space debris (∼ 300, 000 with +1
cm diameter), there will be a demand for tracking and elimination of these objects. There is no
doubt that holographic metrology may take a leading role in these challenging issues.

This section was prepared by Pascal Picart.

19. SLM-based incoherent digital holography

When the first SLM-based incoherent digital holography appeared, there were two main methods
of generating digital holograms of an incoherently illuminated scene. The more dominant
technique has been optical scanning holography [161], where the more digital method has been
multiple view projection digital holography [162]. Both techniques are based on different ways
of time-wasting scanning. The first design of Fresnel incoherent correlation holography (FINCH)
was proposed in 2007 [163] to record incoherent digital holograms without scanning. FINCH
is the first SLM-based incoherent digital holography, but its principles of operation have been
implemented by many different configurations with and without SLM. FINCH has also been used
for many applications such as 3D imaging, fluorescence microscopy, super-resolution, image
processing, and imaging with sectioning. The interested reader can find more about FINCH
and its applications and other incoherent digital holography methods in the review article [164].
The advantage of using SLM for digital holography is that almost all operations related to the
hologram generation can be done by the same phase SLM. In self-interference incoherent digital
holography, there is a need to split the light coming from any object point to two beams, to
spatially modulate the two beams differently, and to shift the phase of one beam at least three times
to eliminate the twin image and the bias term [163,164]. In FINCH, all these three operations are
performed by the same SLM. FINCH has played an important role by inspiring other SLM-based
incoherent digital holography systems, such as Fourier incoherent single-channel holography
[165] and Coded aperture correlation holography (COACH) described next.

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35102

COACH [166] was proposed as a generalization of FINCH but was found to have different
features. Instead of the quadratic phase function, a general chaotic phase mask has been displayed
on the SLM. The image reconstruction has been modified to a cross-correlation with a guidestar
response instead of using the Fresnel backpropagation as in FINCH. In comparison to FINCH,
COACH has better axial resolution but worse lateral resolution. However, the most prominent
difference between them is that COACH can do the same holographic 3D imaging without
two-wave interference [164]. Nevertheless, there are still several applications that can only be
performed by a version of the original COACH with the two-wave interference. One of such
applications is a one-channel-at-a-time incoherent synthetic aperture imager (OCTISAI) [167]
which its setup and results are shown in Fig. 16.

Fig. 16. The tabletop experimental setup of OCTISAI with far-field illuminated objects
and components assembled inside the blue rectangle to execute the operation of synthetic
aperture imaging; BS1 and BS2 - beamsplitters; CMOS camera - Complementary metal-
oxide-semiconductor camera; L01, L02, and L1 - refractive lenses; LED1 and LED2 -
identical light-emitting diodes; P1 and P2 - polarizers; SLM - spatial light modulator; and
USAF - United States Air Force resolution target. Reconstructed images after stitching of (b)
8 central horizontal holograms, (c) 8 central vertical holograms, (d) 2x2 central holograms,
(e) 4x4central holograms, (f) 6x6 central holograms and (g) 8x8 central holograms. Adapted
from [167].

This section was prepared by Joseph Rosen.

20. Phase-distortion compensation/removal in digital holographic microscopy

The transfer of the phase and the amplitude structure from the original sample to the hologram is
strongly affected by the use of the imaging system in DHM. Two typical imaging architectures
have been used in microscopy: (a) the finite-conjugate configuration, with a single MO that
conjugates sample and image planes; and, (b) the infinite-conjugate layout, with a MO followed
by a tube lens (TL), that images the front focal plane of the objective onto the back focal plane
of the TL. Even in the absence of aberrations, a spherical-phase distorsion (SPD) appears onto
the image plane in the finite-conjugate architectures [168], preventing an accurate quantitative
phase imaging (QPI) of the sample. A big research effort has been devoted to correct these
distortions by a numerical post-processing [168–170], by estimating the center and the radius
of curvature of the MO-induced phase perturbation from allegedly flat/empty regions in the
sample plane. Those processes require, however, very precise estimations of the parameters of
the SPD, since even a minimal error in these parameters perturbs dramatically the fidelity of the
QPI result [171]. Additionally, the effect of a residual SPD generates an undesirable shift-variant
response, producing an uneven resolution throughout the field of view (FoV) of the microscope

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35103

[171]. On the other hand, the a posteriori compensation of the SPD cannot avoid the loss of
available bandwidth for the sample in the registration process. This effect is due to the spread of
the spectrum of any signal after modulation by a spherical phase factor, and it affects both phase
and amplitude image resolutions.

To overcome the above problems, some physical a priori removal solutions have been pro-posed.
As an example, the replication of the imaging system used in the object arm into the reference
arm of the setup was proposed to introduce the same SPD in the reference wave-front [21]. This
proposal, however, is complex, expensive and very sensitive to small optical misalignments. An
exact removal of the SPD has been proposed by using an infinite-conjugate architecture. The
optimization of the distance between the two elements of the imaging system (MO and TL) is
used in that paper to completely cancel out the SPD onto the image of the sample. This optimal
design corresponds in fact to a telecentric configura-tion of the microscope, in which the back
focal plane of the MO coincides with the front fo-cal plane of the TL [172]. This configuration
has been successfully applied to ac-curate QPI of biological and biomedical samples [173].
As an example of the comparison of the performance of telecentric and nontelecentric DHM
architectures, Fig. 17 shows some results from [171] where a DH microscope in transmission
mode was used to image a transparent disk with a phase jump of 1.87 rad, at two different
locations within the FoV of the microscope.

Fig. 17. Reconstructed phase profiles of a phase disk located at different places of the
FoV in a DH microscope with: (a) nontelecentric configuration; (b) telecentric layout (Ref.
[171])

In the nontelecentric case, the SPD was estimated by means of a regular a posteriori numerical
approach with very small residual errors. Profiles along the center of the disk show that telecentric
DHM is inherently a shift invariant imaging system that preserves the accuracy of the QPI over
the whole FoV, not requiring a posteriori numerical correction of the measured phase.

This section was prepared by Genaro Saavedra.

21. Off-axis holographic spatial multiplexing

Conventional off-axis holography enables the acquisition of the sample complex wavefront in a
single camera shot, by introducing an angle between the sample and reference beams, yielding an
off-axis hologram containing straight interference fringes in a certain orientation. This single-shot
acquisition mode is attractive for acquiring rapid dynamic processes. However, it comes on the
expense of the spatial bandwidth consumption of the camera, since the sample image needs to
be enlarged more in comparison to on-axis holography, to be able to represent also the off-axis
fringe carrier frequency that modulates the sample spatial information. As shown in Fig. 18(a),
in the spatial-frequency domain, the cross-correlation (CC) terms, each of which contains the
complex wavefront of the sample, are shifted from the origin, where the DC terms, containing
the sample and reference beam intensities, are located. Luckily, this representation introduces

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35104

redundancy, which allows compression of more information along the other orientations in
the spatial-frequency domain as well. This can be obtained by spatial multiplexing of several
off-axis interference patterns with different fringe orientations into a single off-axis multiplexed
hologram, allowing the acquisition of several sample wavefronts at once. Each of the multiplexed
wavefronts can contain different information from the imaged sample, meaning that holographic
multiplexing allows acquisition of more information using the same number of camera pixels
typically used for a single off-axis hologram. This approach, referred to as off-axis holographic
multiplexing, is beneficial for acquiring highly dynamic samples as more spatial data can be
recorded at once.

Fig. 18. (a) Conventional off-axis holography. (b) Multiplexing two sample wavefronts.
(c) Six-pack holography: multiplexing six sample wavefronts.

The working principle of off-axis holographic multiplexing is the projection of more than
one pair of sample/reference beams onto the digital camera, so that the camera can acquire a
multiplexed off-axis hologram with different off-axis fringe orientations at once, where each
fringe orientation encodes a different sample wavefront. These orientations are selected so
that the various CC terms do not overlap in the spatial-frequency domain. Then, the multiple
wavefronts encoded can be reconstructed without loss of resolution or field of view. Figure 18(b)
demonstrates the principle of off-axis holographic multiplexing, where two sample beams, S1
and S2, are multiplexed, using a single reference beam R. Since the two CC pairs, CC1 and CC2,
created from S1 and R and S2 and R respectively, are in orthogonal orientations, they can be
fully reconstructed. In general, more than a single reference beam can be used. The diagonal
cross-term pair, CCx, is created by interference between S1 and S2, which is not useful for the
complex wavefront reconstruction. This unwanted term generation can be avoided by using
different illumination sources, or by using a single illumination source with different wavelength
regions, polarization effects, or coherence gating effects.

The idea of multiplexing two wavefront channels can be further extended to up to six wavefront
channels [174] without an overlap in the spatial-frequency domain, as shown in Fig. 18(c),
making the spatial bandwidth consumption in off-axis holography even more efficient than
on-axis holography, while still enabling single-acquisition mode. One can use this approach
to multiplex the complex sample wavefronts of different sample fields of view [175], color
channels [176], angular perspectives (i.e. for optical tomography or out-of-focus light rejection)
[177], temporal events, polarization states, sample axial planes [178], etc. In addition, digital
multiplexing in off-axis holography can be used for speeding up the holographic reconstruction
process [179]. A comprehensive review on many possible implementations and applications of
off-axis holographic multiplexing has been published recently [101].

This section was prepared by Natan T. Shaked.

22. Compressive sensing for digital holography

3D Digital holography (DH) imaging can be viewed as an inherent compressive imaging modality
since it maps the 3D object space onto the 2D recorded hologram. During the last decade,
compressive sensing (CS) techniques [180] have been employed to make this 3D-to-2D mapping
more efficient. CS provides a framework for the reconstruction of an N dimensional signal, f,

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35105

from M dimensional linear projections, g = ϕf, where M ≪ N. In order to make possible the
reconstruction of the signal f from the undersampled g, the sensing matrix ϕ needs to fulfill
specific requirements, and f should be (approximately) sparse or to have a sparse representation
(i.e., f = Ψα where α is sparse). A canonical example in the CS theory is with ϕ = F , where F
the Fourier operator, and with f being sparse in its native domain (i.e., ϕ is the identity operator).
In such a case, only M ∼ S log N ≪ N random Fourier transform samples are required to fully
reconstruct a signal f composed of S sparse components. One can notice that this canonical
example applies to the relation between the object and hologram field in Fresnel holography
realized in the far field regime. This observation initiated numerous CS applications for DH
(see chap. 8 in [180]). In general, CS tools can be used for digital holography for two different
purposes:

(1) CS can be applied to improve the DH acquisition process efficiency in terms of the number
of recorded samples. For example, CS was employed to undersample the hologram
plane in Fresnel holography [33]. It was shown that only M ∼ N2
FS/N · log N random
hologram samples are sufficient to represent the object’s complex field, where N2
denotes
F
the recording device Fresnel number [180]. Reducing the number of hologram samples is
particularly useful for incoherent holography (see also Sec. 19) where the acquisition effort
for each measurement is large. Indeed, CS was applied for MVP (multiple view projection)
and S-SAFE (sparse synthetic aperture with Fresnel elements) incoherent holography
techniques [180], where the acquisition effort was reduced by an order of magnitude.

(2) CS reconstruction algorithms have been employed to better extract the 3D object information
from the recorded hologram [32]. With proper modeling of the sensing matrix, ϕ, such to
account for the relation between the 3D object and the 2D field at the hologram plane, g,
CS algorithms can be used to reconstruct f with enhanced resolution and signal-to-noise
ratio [32]. For example, it can be shown that the axial resolution in DH tomography can be
increased theoretically by 33% and practically up to an order of magnitude [181]. This, of
course, has important implications for applications such as DH microscopy (e.g., [182]).
Another example for the utility of proper modeling of ϕ together with the power of CS
reconstruction algorithms is for imaging objects behind a partially occluding environment.
In [183], the partially occluded object imaging scenario was recast as a CS problem, and
reconstructions from Fresnel DH with more than 60% occlusion of the field-of-view were
demonstrated.

CS reconstruction algorithms can be made even more effective by using data-driven methods.
One such way is to use hologram exemplaries to better specify the object’s representation space
by building a learned dictionary, which replaces the predefined sparsifying transforms Ψ, in the
above-described CS model. The learned dictionary can then be used with any conventional CS
algorithm. In general, CS algorithms using learned dictionary sparsifiers show better performance
than with using predefined sparsifiers [184]. Overcomplete dictionaries have been used for
compressive Fresnel holography in [185] and demonstrated improved 3D reconstruction with
reduced inter-section diffraction noise. Recently, more powerful data-driven methods which
employ deep learning (DL) algorithms (see also Sec. 15) have been introduced for holography
(e.g., [133]). DL algorithms may learn both the (non-linear) representation of the signal together
with the acquisition process and thus generate more precise and faster reconstructions than
conventional iterative algorithms do. We expect that further research efforts on the application of
DL for compressive holography may yield further improvement of the 3D objects reconstruction,
better feature extraction from the holograms for various applications (e.g., microscopy, industrial
inspection, etc.), enhanced phase retrieval, improved cross-generalization, and optimization of
the acquisition process.

This section was prepared by Adrian Stern.

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35106

23. Single-pixel digital holography

Computational imaging techniques based on structured light and single-pixel detection permit
to use light sensors without pixelated structure [186]. The method consists on sampling the
scene sequentially with a set of microstructured light patterns while a simple bucket detector,
for instance a photodiode, records the light intensity transmitted, reflected or diffused by the
object. By using light patterns codifying Hadamard or Fourier components, images are retrieved
by just a simple basis transformation. The technique is well adapted also to apply compressive
sensing (CS), by using different basis of functions, or deep learning. Other sampling strategies or
reconstruction algorithms can be applied. Using random speckle patterns, for example, reveals
the close connection of single-pixel imaging with ghost imaging.

Single-pixel imaging (SPI) techniques have been applied with success to phase and complex
amplitude imaging both with non-interferometric [140,187,188] and with interferometric holo-
graphic setups [189–192]. In holographic setups based on interferometers, usually an arbitrary
plane at the object light beam, which may be also the object plane, is sampled with a spatial light
modulator (SLM). Light diffracted by the object and sampled by the SLM interferes with the
reference beam and is integrated by a simple bucket detector such as a photodiode.

Figure 19(a) shows a Mach-Zehnder configuration for single-pixel holography (SPH) [189]. The
SLM is a digital micromirror device (DMD) which samples a diffraction pattern with Hadamard
masks. The phase shifter at the reference beam allows to apply phase-shifting techniques to
measure the complex index associated to each Hadamard pattern with the photodiode. The
complex amplitude distribution at the DMD plane is then reconstructed by applying SPI algorithms.
Other patterns such as the phase distribution at the object plane can be reconstructed by numerical
propagation, as is shown in the inset in Fig. 19(a).

Fig. 19. Optical configurations based on phase-shifting interferometers for single-pixel
digital holography:
(b) Michelson
architecture with LCD [190].

(a) Mach-Zehnder architecture with DMD [189].

Many other optical configurations can be used for SPH, such as the Michelson interferometer
in Fig. 19(b) [190]. In this case, the SLM used to sample the complex amplitude distribution is a
liquid crystal display (LCD), which is also used to apply phase-shifting techniques. Interestingly,
the LCD can be located at the reference arm of the interferometer to reconstruct diffraction
patterns at the object beam.

SPH methods benefit from the simplicity of the sensing device in contrast with other holographic
techniques. This characteristic should help to develop new holographic systems working efficiently
in conditions where light is scarce. It also should make easier to measure the spatial distribution
of multiple optical properties of the light, allowing to develop new multimode imaging techniques.
Bucket detectors permit to sense a broader spectral range compared to conventional multi-pixel
cameras. Furthermore, single pixel detection is more tolerant to aberrations or scattering produced

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35107

in the optical path near the light sensor. The main challenge in developing new SPH techniques
is the sequential nature of the sampling method. Besides, there is a trade-off between spatial
resolution and frame-rate. Therefore, it is essential to decrease the acquisition time by developing
faster SLMs, more efficient compressive methods, and smart reconstruction algorithms. With
these improvements, single-pixel detection may provide holographic techniques, alone or in
combination with other imaging methods, with remarkable new features for innovative industrial
or biomedical applications.

This section was prepared by Enrique Tajahuerce.

24. Holographic 3D reconstruction with multiple scattering models

In this section, we present an overview of holographic 3D reconstruction with multiple scattering
models. In many applications, it is highly desirable to reconstruct 3D information from a 2D
image. Digital holography (DH) is particularly suited for this application since it can record 3D
information in a single hologram. However, for holographic 3D reconstructions, the problem
is challenging because the multiple scattering effects become significant with the increase of
the thickness of the 3D object and the refractive index contrast, which makes the widely used
single-scattering assumption (i.e., 1st Born or Rytov approximations) based reconstruction
inaccurate.

To overcome the limitation of weak-scattering assumption, multiple-scattering-based models
have recently been developed. For example, the beam propagation model (BPM) [193,194], split-
step non-paraxial (SSNP) method [195], and multi-layer Born model [196] have shown effective
in tomographically reconstructing complex object using multiple holographic measurements.
For single-shot applications, Tahir et al.
[197] propose to reconstruct 3D particle fields
based on the iterative Born series. In [197], it shows that the multiple-scattering model leads
to significant improvement in both the forward holographic modeling and the inverse 3D
localization as compared to traditional methods based on the single-scattering approximation.
However, the proposed method is computational prohibitive especially for large-scale 3D volume
reconstructions, which limit its application in practice.

More recently, single-shot 3D reconstruction based on the BPM has been reported in [198].
This new method utilizes the BPM to account for the multiple scattering, as shown in Fig. 20(a)
and Fig. 20(b). The BPM can then be used to reconstruct 3D particles with state-of-the-art
accuracy, as shown in Fig. 20(c).
In addition, the BPM method significantly reduces the
computational complexity by two orders of magnitude as compared with [197].

Fig. 20. Particle 3D imaging from a single in-line hologram using the BPM [198].
(a) Experimental setup. (b) BPM model involves successive propagation and refraction
operations to compute the scattered field from one object slice to the next. (c) Holographic
particle 3D reconstruction.

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35108

Though incorporating the multiple scattering models into holographic imaging opens up
holographic 3D reconstruction to an entirely new range of samples that are thicker and more
scattering than previous could, there are still some challenges to be solved in the future. One
limitation is the severe missing cone artifact when reconstructing an object from a single hologram
or limited-angle holographic tomography measurements, which elongates the reconstructed
samples and underestimates the values of the refractive index. A promising future direction is to
combine multiple-scattering models and advanced deep-learning priors to further improve the
reconstruction performance [199].

This section was prepared by Lei Tian.

25. Machine-learning-enabled holographic near-eye displays for virtual and aug-

mented reality

Augmented and virtual reality (AR/VR) systems promise unprecedented user experiences, but the
light engines of current AR/VR platforms are limited in their peak brightness, power efficiency,
device form factor, support of perceptually important focus cues, and ability to correct visual
aberrations of the user or optical aberrations of the downstream optics. Holographic near-eye
displays promise solutions for many of these problems. Their unique capability of synthesizing a
3D intensity distribution with a single spatial light modulator (SLM) and coherent illumination,
created by bright and power-efficient lasers, makes these displays ideal for applications in wearable
computing systems.

Although the fundamentals of holography have been developed more than 70 years ago, until
recently, high-quality holograms have only been achieved using optical recording techniques but
not using digital spatial light modulators. The primary challenge for generating high-quality digital
holograms in a computationally efficient manner are the algorithms used for computer-generated
holography (CGH). Traditional CGH algorithms [200] rely on simulated wave propagation
models that do not adequately represent the physical optics aspects of a near-eye display, thus
severely limiting the achievable quality (see Fig. 21). Moreover, iterative CGH methods are slow
and not suitable for the power-constrained settings in which wearable computing systems must
operate. Recently, a class of machine-learning-enabled CGH algorithms has been proposed that
overcome some of these challenges. For example, Peng et al. [201,202] and Chakravarthula et
al. [203] proposed automatic ways to calibrate better wave propagation models using cameras,
thereby significantly improving upon previously reported holographic image quality. Horisaki et
al. [158], Peng et al., Eybposh et al. [201202, 204], and Shi et al. [158] also introduced various
neural network architectures for real-time holographic image synthesis.

Fig. 21. Conventional computer-generated holography algorithms, such as Gerch-
berg–Saxton, suffer from artifacts. Recent advances in machine-learning-enabled holographic
displays, such as camera-in-the-loop (CITL) optimization strategies [201,202] and neural
networks, such as HoloNet [201,202], achieve unprecedented holographic image quality and
real-time framerates. Image adapted from [200].

At the intersection of computational optics and computer graphics, advanced computer-
generated holography algorithms are a key enabling technology for 3D virtual and augmented

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35109

reality applications. First steps to combining classical CGH algorithms and optical systems with
modern machine-learning techniques have been taken to address several long-standing challenges,
such as speed and image quality.

To unlock the full potential of holographic near-eye displays in VR/AR applications, however,
several remaining challenges need to be addressed. Foremost, the size, weight, and power
requirements of the optics and spatial light modulators has to be reduced into wearable form
factors. This includes the development of thin optical combiners, such as geometric light guides
or diffractive waveguide couplers, that utilize the unique capabilities of holographic light engines
in optical see-through augmented reality applications. Moreover, safety concerns about lasers
used in near-eye displays need to be addressed, for example by enabling holographic displays
with partially coherent sources [201]. Machine-learning-enabled holographic displays provide
new opportunities for solving these and other long-standing challenges.

This section was prepared by Gordon Wetzstein.

26.

Integration of light-field imaging and digital holography

The wavefront captured by DH delivers the information on the phase modulation by the object that
represents the thickness and refractive index, and the 3D structure of the object such as scattering
or absorbing materials. DH normally requires a coherent source, and the color or spectral
imaging is not easy. Color or multispectral DH has been reported using multiple laser sources,
but each image is captured by a single wavelength and the absorption in other wavelengths cannot
be observed. In fact, the wavelength dependence of phase does not substantially represent the
characteristics of a material and not much of interest. The wavelength dependence of absorption
is vital information for the analysis of materials and color or spectral imaging to capture it
can more easily be implemented using an incoherent light source with a continuous spectrum.
Another limitation of coherent imaging is the speckle noise and the diffraction pattern in the
out-of-focus objects. In the image reconstructed from DH, the diffraction pattern often hinders
the observation of the target object.

To overcome those limitations of DH, the combination of DH and incoherent imaging has
been studied [131,205–208]. For example, in the microscopic observation of biological samples,
the color added by the staining technique represents the structural and molecular information.
Combining it with the quantitative phase information obtained by DH will contribute to a more
advanced analysis in biomedicine [205,206]. Another way to utilize them is to incorporate the
3D information obtained by DH in the incoherently observed image. Figure 22 shows an example
of combining the incoherent bright-field (BF) image with the 3D structural information obtained
by DH [207]. In this case, a BF image is captured with focusing on a certain object, and a DH is
captured with a single wavelength. The refocusing is possible by DH reconstruction, but the
appearance of defocused images is vastly different from the BF image. Using both the DH and
BF images, the 3D color image is reconstructed, which enables refocusing with natural visual
appearance. That is to say, light-field (LF) imaging can be implemented with the assistance of
DH [131].

LF imaging is employed in image acquisition, computer graphics, and 3D display, which is
based on the “plenoptic” function; a function of spatial coordinates, ray direction, wavelength,
and time. Integral imaging is a typical technique of acquiring LF. A limitation of LF is the lack of
phase information, and it is not suitable for the imaging of phase objects. An obvious extension is
adding phase to LF. If we add the phase term and consider the complex amplitude representation,
it can directly be associated with the wavefront dealt in holography [209]. Another issue in the
LF representation is the sampling of rays. In the ray-tracing of computer graphics, the rays are
always a very narrow. In the physical world, however, if the rays are sampled at a certain plane,
they become broadened due to diffraction. Thus, the ray sampling should be done carefully such

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35110

Fig. 22. Simulation result of BF image refocusing by assistance of DH. (a) Captured image
with focusing on ’3’ and ’C’. (b) DH reconstruction focusing on ’4’ and ’D’. Refocused
results by (c) proposed method and (d) BF image only.

that the image resolution is not degraded. As the ideal location of ray-sampling is the object
surface, the influence can be minimized if it is done near the object [210].

The ray representation is obtained by the angular spectrum of the wavefront, i.e., Fourier
transform. Then the conversion between the wavefront and light-rays can be calculated by
FFT. The ray-tracing can be substituted with the wave propagation if the diffraction effect is
non-negligible. The wave propagation is computed by the convolution. In this way, the integration
of DH and LF can lead to the construction of novel imaging techniques. The integrated DH-LF
will also be significantly advanced by incorporating computational imaging with sophisticated
optimization technology and/or “deep” machine learning.
This section was prepared by Masahiro Yamaguchi.

27. Conclusion

Holography is a very broad discipline. Since its inception in the late 1940s and its evolution
in the 1960s and beyond, it has grown to become a well-researched field with many diverse
applications. While there are many areas of holography, this article has focused on digital
holography. The Roadmap paper is comprised of 25 sections contributed by prominent experts
in the field to provide an overview of various aspects of digital holography. We start the roadmap
article by presenting the origins of holography in Section 2 by J. W. Goodman. Then the
author of each remaining section describes the progress, potential, vision, and challenges in
a particular application of digital holography. A vast array of topics are covered including
self-referencing digital holography, information security, lab-on-chip holography, tomographic
microscopy with randomly structured illumination, automated disease identification by digital
holography, label-free live cell imaging, digital holography with machine learning, disordered
optics for digital holography, SLM-based incoherent digital holography, off-axis holographic
spatial multiplexing, compressive sensing, single-pixel digital holography, holographic 3D
reconstruction with multiple scattering models, machine-learning-enabled holographic near-eye
displays for virtual and augmented reality, integration of light-field imaging and digital holography,
and digital holography macro industrial applications and inspection. Table 1 has a list of all the
sections and their corresponding author.

As in any overview paper of this nature, it is not possible to describe and represent all the
possible applications, approaches, and activities in the broad field of digital holography. We
apologize in advance if we have not included any relevant work in digital holography. Hopefully,
the large number of cited references can aid the reader with those areas not fully discussed in this
Roadmap.

Funding. National Research Foundation Singapore; Intelligence Advanced Research Projects Activity; Institute of
Information & communications Technology Planning & Evaluation (IITP) grant funded by the Korea government
(MSIT) (2021-0-00745); National Research Foundation of Korea (2015R1A3A2066550); Office of Naval Research

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35111

(N000141712405); Army Research Office; National Science Foundation (1839974); Ford Motor Company; Euro-
pean Research Council (ERC StG 678316); National Science Foundation (1846784); National Science Foundation
(1813848); Universitat Jaume I (UJIB2018-68); Generalitat Valenciana (PROMETEO/2020/029); Agencia Estatal de
Investigación (PID2019-110927RB-I00/AEI/10.13039/501100011033); Agencia Estatal de Investigación (PID2019-
104268GB-C22/AEI/10.13039/501100011033); Generalitat Valenciana (PROMETEO/2019/048); Ministerio de Ciencia,
Innovacion y Universidades (RTI2018-099041-B-I00); Israel Science Foundation (1669/16); NSF PATHS-UP; Canada
Excellence Research Chairs, Government of Canada; Canada Foundation for Innovation (342, 36689); Natural Sciences
and Engineering Research Council of Canada (RGPIN-2018-06198); European Commission (H2020-ICT-2016-1 MOON
Grant 732969); Austrian National Science Foundation (FWF grant no. P 29093-N36); Department of Science and
Technology India (IDP/MED/34/2016); Foundation for Polish Science co-financed by the European Union under the
European Regional Development Fund (TEAM TECH/2016-1/4); Horizon 2020 Framework Programme (101016726);
Morphological Biomarkers for early diagnosis in Oncology (MORFEO) (MUR- PRIN 2017 Prot. 2017N7R2CJ); Hong
Kong Polytechnic University (4-ZZLF, 1-W167); Board of Research in Nuclear Sciences (2013/34/11/BRNS/504);
Science and Engineering Research Board (EMR/20l7/002724).

Disclosures. Pierre Marquet declares a potential conflict as co-founder of Lyncée Tec. Rainer A. Leitgeb authors
patents with Carl Zeiss Meditec. The rest of the authors declare no conflicts of interest.

Data availability. Data underlying the results presented in this paper are not publicly available at this time but may
be obtained from the authors upon reasonable request.

References
1. D. Gabor, “A new microscopic principle,” Nature 161(4098), 777–778 (1948).
2.

3.

4.

E. N. Leith and J. Upatnieks, “Reconstructed wavefronts and communication theory,” J. Opt. Soc. Am. 52(10),
1123–1130 (1962).
E. N. Leith, J. Upatnieks, and K. A. Haines, “Microscopy by wavefront reconstruction,” J. Opt. Soc. Am. 55(8),
981–986 (1965).
J. W. Goodman and R. Lawrence, “Digital image formation from electronically detected holograms,” Appl. Phys.
Lett. 11(3), 77–79 (1967).
T. S. Huang, “Digital holography,” Proc. IEEE 59(9), 1335–1346 (1971).

5.
6. U. Schnars and W. Jüptner, “Direct recording of holograms by a ccd target and numerical reconstruction,” Appl.

7.
8.

Opt. 33(2), 179–181 (1994).
I. Yamaguchi and T. Zhang, “Phase-shifting digital holography,” Opt. Lett. 22(16), 1268–1270 (1997).
E. Cuche, F. Bevilacqua, and C. Depeursinge, “Digital holography for quantitative phase-contrast imaging,” Opt.
Lett. 24(5), 291–293 (1999).

9. B. Javidi and T. Nomura, “Securing information by use of digital holography,” Opt. Lett. 25(1), 28–30 (2000).
10. E. Tajahuerce and B. Javidi, “Encrypting three-dimensional information with digital holography,” Appl. Opt. 39(35),

6595–6601 (2000).

11. B. Javidi and E. Tajahuerce, “Three-dimensional object recognition by use of digital holography,” Opt. Lett. 25(9),

610–612 (2000).

12. E. Tajahuerce, O. Matoba, and B. Javidi, “Shift-invariant three-dimensional object recognition by means of digital

holography,” Appl. Opt. 40(23), 3877–3886 (2001).

13. W. Osten, T. Baumbach, and W. Jüptner, “Comparative digital holography,” Opt. Lett. 27(20), 1764–1766 (2002).
14. T. Colomb, P. Dahlgren, D. Beghuin, E. Cuche, P. Marquet, and C. Depeursinge, “Polarization imaging by use of

digital holography,” Appl. Opt. 41(1), 27–37 (2002).

15. P. Ferraro, S. De Nicola, A. Finizio, G. Coppola, S. Grilli, C. Magro, and G. Pierattini, “Compensation of the
inherent wave front curvature in digital holographic coherent microscopy for quantitative phase-contrast imaging,”
Appl. Opt. 42(11), 1938–1946 (2003).

16. D. Kim and B. Javidi, “Distortion-tolerant 3-d object recognition by using single exposure on-axis digital holography,”

Opt. Express 12(22), 5539–5548 (2004).

17. T. Kreis, Handbook of Holographic Interferometry: Optical and Digital Methods (John Wiley & Sons, 2006).
18. P. Marquet, B. Rappaz, P. J. Magistretti, E. Cuche, Y. Emery, T. Colomb, and C. Depeursinge, “Digital holographic
microscopy: a noninvasive contrast imaging technique allowing quantitative visualization of living cells with
subwavelength axial accuracy,” Opt. Lett. 30(5), 468–470 (2005).

19. B. Rappaz, P. Marquet, E. Cuche, Y. Emery, C. Depeursinge, and P. J. Magistretti, “Measurement of the integral
refractive index and dynamic cell morphometry of living cells with digital holographic microscopy,” Opt. Express
13(23), 9361–9373 (2005).

20. P. Ferraro, S. Grilli, D. Alfieri, S. De Nicola, A. Finizio, G. Pierattini, B. Javidi, G. Coppola, and V. Striano,

“Extended focused image in microscopy by digital holography,” Opt. Express 13(18), 6738–6749 (2005).

21. C. J. Mann, L. Yu, C.-M. Lo, and M. K. Kim, “High-resolution quantitative phase-contrast microscopy by digital

holography,” Opt. Express 13(22), 8693–8698 (2005).

22. B. Javidi, I. Moon, S. Yeom, and E. Carapezza, “Three-dimensional imaging and recognition of microorganism

using single-exposure on-line (seol) digital holography,” Opt. Express 13(12), 4492–4506 (2005).

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35112

23. Y. Frauel, T. J. Naughton, O. Matoba, E. Tajahuerce, and B. Javidi, “Three-dimensional imaging and processing

using computational holographic imaging,” Proc. IEEE 94(3), 636–653 (2006).

24. Y. Park, G. Popescu, K. Badizadegan, R. R. Dasari, and M. S. Feld, “Diffraction phase and fluorescence microscopy,”

Opt. Express 14(18), 8263–8268 (2006).

25. C. Kohler, X. Schwab, and W. Osten, “Optimally tuned spatial light modulators for digital holography,” Appl. Opt.

45(5), 960–967 (2006).

26. M. DaneshPanah and B. Javidi, “Tracking biological microorganisms in sequence of 3D holographic microscopy

images,” Opt. Express 15(17), 10761–10766 (2007).

27. T. Nomura and B. Javidi, “Object recognition by use of polarimetric phase-shifting digital holography,” Opt. Lett.

28.

32(15), 2146–2148 (2007).
J. Rosen and G. Brooker, “Non-scanning motionless fluorescence three-dimensional holographic microscopy,” Nat.
Photonics 2(3), 190–195 (2008).

29. B. Kemper and G. VonBally, “Digital holographic microscopy for live cell applications and technical inspection,”

Appl. Opt. 47(4), A52–A61 (2008).

30. P. Langehanenberg, B. Kemper, D. Dirksen, and G. VonBally, “Autofocusing in digital holographic phase contrast

31.

microscopy on pure phase objects for live cell imaging,” Appl. Opt. 47(19), D176–D182 (2008).
I. Moon, M. Daneshpanah, B. Javidi, and A. Stern, “Automated three-dimensional identification and tracking of
micro/nanobiological organisms by computational holographic microscopy,” Proc. IEEE 97(6), 990–1010 (2009).
32. D. J. Brady, K. Choi, D. L. Marks, R. Horisaki, and S. Lim, “Compressive holography,” Opt. Express 17(15),

13040–13049 (2009).

33. Y. Rivenson, A. Stern, and B. Javidi, “Compressive fresnel holography,” J. Disp. Technol. 6(10), 506–509 (2010).
34. V. Micó and J. García, “Common-path phase-shifting lensless holographic microscopy,” Opt. Lett. 35(23), 3919–3921

(2010).

35. M. DaneshPanah, S. Zwick, F. Schaal, M. Warber, B. Javidi, and W. Osten, “3d holographic imaging and trapping

for non-invasive cell identification and tracking,” J. Disp. Technol. 6(10), 490–499 (2010).

36. L. Onural, F. Yaraş, and H. Kang, “Digital holographic three-dimensional video displays,” Proc. IEEE 99(4),

576–589 (2011).

37. W. Osten, A. Faridian, P. Gao, K. Körner, D. Naik, G. Pedrini, A. K. Singh, M. Takeda, and M. Wilke, “Recent

advances in digital holography,” Appl. Opt. 53(27), G44–G63 (2014).

38. A. K. Singh, A. Faridian, P. Gao, G. Pedrini, and W. Osten, “Quantitative phase imaging using a deep uv led source,”

Opt. Lett. 39(12), 3468–3471 (2014).

39. A. Anand, I. Moon, and B. Javidi, “Automated disease identification with 3-d optical imaging: a medical diagnostic

tool,” Proc. IEEE 105(5), 924–946 (2017).

40. A. Anand, V. Chhaniwal, N. Patel, and B. Javidi, “Automatic identification of malaria-infected rbc with digital

holographic microscopy using correlation algorithms,” IEEE Photonics J. 4(5), 1456–1464 (2012).
J. W. Goodman, Introduction to Fourier Optics (Macmillan Education, 2017), 4th ed.

41.
42. B. R. Brown and A. W. Lohmann, “Complex spatial filtering with binary masks,” Appl. Opt. 5(6), 967–969 (1966).
43. B. Javidi and J. L. Horner, Real-time optical information processing (Academic, 1994).
44. S. Seo, T.-W. Su, D. K. Tseng, A. Erlinger, and A. Ozcan, “Lensfree holographic imaging for on-chip cytometry and

diagnostics,” Lab Chip 9(6), 777–787 (2009).

45. Y. Jo, J. Jung, M.-H. Kim, H. Park, S.-J. Kang, and Y. Park, “Label-free identification of individual bacteria using

fourier transform light scattering,” Opt. Express 23(12), 15792–15805 (2015).

46. Y. Jo, H. Cho, S. Y. Lee, G. Choi, G. Kim, H.-S. Min, and Y. Park, “Quantitative phase imaging and artificial

intelligence: a review,” IEEE J. Sel. Top. Quantum Electron. 25(1), 1–14 (2019).

47. H. C. Koydemir, Z. Gorocs, D. Tseng, B. Cortazar, S. Feng, R. Y. L. Chan, J. Burbano, E. McLeod, and A.
Ozcan, “Rapid imaging, detection and quantification of giardia lamblia cysts using mobile-phone based fluorescent
microscopy and machine learning,” Lab Chip 15(5), 1284–1293 (2015).

48. A. El Mallahi, C. Minetti, and F. Dubois, “Automated three-dimensional detection and classification of living
organisms using digital holographic microscopy with partial spatial coherent source: application to the monitoring
of drinking water resources,” Appl. Opt. 52(1), A68–A80 (2013).

49. K. Jaferzadeh, B. Rappaz, F. Kuttler, B. K. Kim, I. Moon, P. Marquet, and G. Turcatti, “Marker-free automatic
quantification of drug-treated cardiomyocytes with digital holographic imaging,” ACS Photonics 7(1), 105–113
(2020).
I. Moon, A. Anand, M. Cruz, and B. Javidi, “Identification of malaria-infected red blood cells via digital shearing
interferometry and statistical inference,” IEEE Photonics J. 5(5), 6900207 (2013).

50.

51. G. Popescu, T. Ikeda, R. R. Dasari, and M. S. Feld, “Diffraction phase microscopy for quantifying cell structure and

52.

dynamics,” Opt. Lett. 31(6), 775–777 (2006).
I. Moon and B. Javidi, “Volumetric three-dimensional recognition of biological microorganisms using multivariate
statistical method and digital holography,” J. Biomed. Opt. 11(6), 064004 (2006).

53. S. Osten and N. Reingand, Optical Imaging and Metrology: Advanced Technologies (Wiley-VCH Verlag GmbH &

Co., 2012).

54. L. Enloe, J. Murphy, and C. Rubinstein, “Bstj briefs hologram transmission via television,” The Bell Syst. Tech. J.

45(2), 335–339 (1966).

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35113

55.

J. W. Cooley and J. W. Tukey, “An algorithm for the machine calculation of complex fourier series,” Math. Comput.
19(90), 297 (1965).

56. A. S. Singh, A. Anand, R. A. Leitgeb, and B. Javidi, “Lateral shearing digital holographic imaging of small

biological specimens,” Opt. Express 20(21), 23617–23622 (2012).

57. T. O’Connor, A. Anand, B. Andemariam, and B. Javidi, “Deep learning-based cell identification and disease
diagnosis using spatio-temporal cellular dynamics in compact digital holographic microscopy,” Biomed. Opt.
Express 11(8), 4491–4508 (2020).

58. A. Anand, V. Chhaniwal, and B. Javidi, “Tutorial: common path self-referencing digital holographic microscopy,”

APL Photonics 3(7), 071101 (2018).

59. V. Chhaniwal, A. S. Singh, R. A. Leitgeb, B. Javidi, and A. Anand, “Quantitative phase-contrast imaging with
compact digital holographic microscope employing lloyd’s mirror,” Opt. Lett. 37(24), 5127–5129 (2012).
60. D. L. Marks, “A family of approximations spanning the born and rytov scattering series,” Opt. Express 14(19),

8837–8848 (2006).

61. U. S. Kamilov, I. N. Papadopoulos, M. H. Shoreh, A. Goy, C. Vonesch, M. Unser, and D. Psaltis, “Optical
tomographic image reconstruction based on beam propagation and sparse regularization,” IEEE Transactions on
Comput. Imaging 2(1), 59–70 (2016).

62. A. Goy, G. Rughoobur, S. Li, K. Arthur, A. I. Akinwande, and G. Barbastathis, “High-resolution limited-angle phase
tomography of dense layered objects using deep neural networks,” Proc. Natl. Acad. Sci. 116(40), 19848–19856
(2019).

63. Q. Zhan, “Cylindrical vector beams: from mathematical concepts to applications,” Adv. Opt. Photonics 1(1), 1–57

(2009).

64. C. Rosales-Guzmán, B. Ndagano, and A. Forbes, “A review of complex vector light fields and their applications,” J.

Opt. 20(12), 123001 (2018).

65. X.-L. Wang, J. Ding, W.-J. Ni, C.-S. Guo, and H.-T. Wang, “Generation of arbitrary vector beams with a spatial

light modulator and a common path interferometric arrangement,” Opt. Lett. 32(24), 3549–3551 (2007).

66. V. Arrizón, “Complex modulation with a twisted-nematic liquid-crystal spatial light modulator: double-pixel

approach,” Opt. Lett. 28(15), 1359–1361 (2003).

67. D. Maluenda, I. Juvells, R. Martínez-Herrero, and A. Carnicer, “Reconfigurable beams with arbitrary polarization

and shape distributions at a given plane,” Opt. Express 21(5), 5432–5439 (2013).

68. D. Maluenda, R. Martínez-Herrero, I. Juvells, and A. Carnicer, “Synthesis of highly focused fields with circular

polarization at any transverse plane,” Opt. Express 22(6), 6859–6867 (2014).

69. R. Martínez-Herrero, D. Maluenda, I. Juvells, and A. Carnicer, “Synthesis of light needles with tunable length and

nearly constant irradiance,” Sci. Rep. 8(1), 2657–2710 (2018).

70. P. Refregier and B. Javidi, “Optical image encryption based on input plane and fourier plane random encoding,”

Opt. Lett. 20(7), 767–769 (1995).

71. O. Matoba, T. Nomura, E. Perez-Cabre, M. S. Millan, and B. Javidi, “Optical techniques for information security,”

Proc. IEEE 97(6), 1128–1148 (2009).

72. W. Chen, B. Javidi, and X. Chen, “Advances in optical security systems,” Adv. Opt. Photonics 6(2), 120–155 (2014).
73. A. Carnicer, M. Montes-Usategui, S. Arcos, and I. Juvells, “Vulnerability to chosen-cyphertext attacks of optical

encryption schemes based on double random phase keys,” Opt. Lett. 30(13), 1644–1646 (2005).

74. L. Zhou, Y. Xiao, and W. Chen, “Learning complex scattering media for optical encryption,” Opt. Lett. 45(18),

5279–5282 (2020).

75. X. Fang, H. Ren, and M. Gu, “Orbital angular momentum holography for high-security encryption,” Nat. Photonics

14(2), 102–108 (2020).

76. L. Miccio, F. Cimmino, I. Kurelac, M. M. Villone, V. Bianco, P. Memmolo, F. Merola, M. Mugnano, M. Capasso,
A. Iolascon, P. L. Maffettone, and P. Ferraro, “Perspectives on liquid biopsy for label-free detection of “circulating
tumor cells” through intelligent lab-on-chips,” View 1(3), 20200034 (2020).

77. P. Memmolo, L. Miccio, M. Paturzo, G. DiCaprio, G. Coppola, P. A. Netti, and P. Ferraro, “Recent advances in

holographic 3D particle tracking,” Adv. Opt. Photonics 7(4), 713–755 (2015).

78. L. Miccio, P. Memmolo, F. Merola, P. Netti, and P. Ferraro, “Red blood cell as an adaptive optofluidic microlens,”

Nat. Commun. 6(1), 6502–6507 (2015).

79. F. Merola, P. Memmolo, L. Miccio, R. Savoia, M. Mugnano, A. Fontana, G. D’ippolito, A. Sardo, A. Iolascon, A.
Gambale, and P. Ferraro, “Tomographic flow cytometry by digital holography,” Light: Sci. Appl. 6(4), e16241
(2017).

80. D. Pirone, P. Memmolo, F. Merola, L. Miccio, M. Mugnano, A. Capozzoli, C. Curcio, A. Liseno, and P. Ferraro,
“Rolling angle recovery of flowing cells in holographic tomography exploiting the phase similarity,” Appl. Opt.
60(4), A277–A284 (2021).

81. A. Saba, J. Lim, A. B. Ayoub, E. E. Antoine, and D. Psaltis, “Polarization-sensitive optical diffraction tomography,”

Optica 8(3), 402–408 (2021).

82. G. Wetzstein, A. Ozcan, S. Gigan, S. Fan, D. Englund, M. Soljačić, C. Denz, D. A. Miller, and D. Psaltis, “Inference

in artificial intelligence with deep optics and photonics,” Nature 588(7836), 39–47 (2020).

83. R. Horisaki, Y. Ogura, M. Aino, and J. Tanida, “Single-shot phase imaging with a coded aperture,” Opt. Lett. 39(22),

6466–6469 (2014).

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35114

84. R. Horisaki, R. Egami, and J. Tanida, “Single-shot phase imaging with randomized light (SPIRaL),” Opt. Express

85. R. Horisaki, K. Fujii, and J. Tanida, “Diffusion-based single-shot diffraction tomography,” Opt. Lett. 44(8),

24(4), 3765–3773 (2016).

1964–1967 (2019).

86. R. Horisaki, H. Matsui, R. Egami, and J. Tanida, “Single-pixel compressive diffractive imaging,” Appl. Opt. 56(5),

1353–1357 (2017).

87. R. Horisaki, Y. Okamoto, and J. Tanida, “Single-shot noninvasive three-dimensional imaging through scattering

media,” Opt. Lett. 44(16), 4032–4035 (2019).

88. K. Ehira, R. Horisaki, Y. Nishizaki, M. Naruse, and J. Tanida, “Spectral speckle-correlation imaging,” Appl. Opt.

60(8), 2388–2392 (2021).

89. R. Horisaki, Y. Nishizaki, K. Kitaguchi, M. Saito, and J. Tanida, “Three-dimensional deeply generated holography,”

90.

91.

Appl. Opt. 60(4), A323–A328 (2021).
I. Moon and B. Javidi, “3-D visualization and identification of biological microorganisms using partially temporal
incoherent light in-line computational holographic imaging,” IEEE Transactions on Medical Imaging 27(12),
1782–1790 (2008).
I. Moon and B. Javidi, “Three-dimensional identification of stem cells by computational holographic imaging,”
Royal Soc. Interface 4(13), 305–313 (2007).

92. B. Javidi, A. Markman, S. Rawat, T. O’Connor, A. Anand, and B. Andemariam, “Sickle cell disease diagnosis
based on spatio-temporal cell dynamics analysis using 3D printed shearing digital holographic microscopy,” Opt.
Express 26(10), 13614–13627 (2018).

93. T. O’Connor, J.-B. Shen, B. T. Liang, and B. Javidi, “Digital holographic deep learning of red blood cells for

field-portable, rapid covid-19 screening,” Opt. Lett. 46(10), 2344–2347 (2021).

94. B. Javidi, S. Rawat, S. Komatsu, and A. Markman, “Cell identification using single beam lensless imaging with

pseudo-random phase encoding,” Opt. Lett. 41(15), 3663–3666 (2016).

95. T. O’Connor, C. Hawxhurst, L. M. Shor, and B. Javidi, “Red blood cell classification in lensless single random

phase encoding using convolutional neural networks,” Opt. Express 28(22), 33504–33515 (2020).

96. E. Watanabe, T. Hoshiba, and B. Javidi, “High-precision microscopic phase imaging without phase unwrapping for

cancer cell identification,” Opt. Lett. 38(8), 1319–1321 (2013).

97. M. Ugele, M. Weniger, M. Stanzel, M. Bassler, S. W. Krause, O. Friedrich, O. Hayden, and L. Richter, “Label-free

high-throughput leukemia detection by holographic microscopy,” Adv. Sci. 5(12), 1800761 (2018).

98. M. Rubin, O. Stein, N. A. Turko, Y. Nygate, D. Roitshtain, L. Karako, I. Barnea, R. Giryes, and N. T. Shaked,
“Top-gan: Stain-free cancer cell classification using deep learning with a small training set,” Med. Image Anal. 57,
176–185 (2019).

99. A. Ozcan and E. McLeod, “Lensless imaging and sensing,” Annu. Rev. Biomed. Eng. 18(1), 77–102 (2016).
100. H. Wang, H. C. Koydemir, Y. Qiu, B. Bai, Y. Zhang, Y. Jin, S. Tok, E. C. Yilmaz, E. Gumustekin, Y. Rivenson, and
A. Ozcan, “Early detection and classification of live bacteria using time-lapse coherent imaging and deep learning,”
Light: Sci. Appl. 9(1), 118–217 (2020).

101. N. T. Shaked, V. Micó, M. Trusiak, A. Kuś, and S. K. Mirsky, “Off-axis digital holographic multiplexing for rapid

wavefront acquisition and processing,” Adv. Opt. Photonics 12(3), 556–611 (2020).

102. B. Javidi, A. Markman, and S. Rawat, “Automatic multicell identification using a compact lensless single and

double random phase encoding system,” Appl. Opt. 57(7), B190–B196 (2018).

103. S. Rawat, S. Komatsu, A. Markman, A. Anand, and B. Javidi, “Compact and field-portable 3D printed shearing

digital holographic microscope for automated cell identification,” Appl. Opt. 56(9), D127–D133 (2017).

104. M. K. Kim, “Principles and techniques of digital holographic microscopy,” J. Photonics Energy 1, 018005 (2010).
105. Y. Park, C. Depeursinge, and G. Popescu, “Quantitative phase imaging in biomedicine,” Nat. Photonics 12(10),

578–589 (2018).

106. K. Khare, P. S. Ali, and J. Joseph, “Single shot high resolution digital holography,” Opt. Express 21(3), 2581–2591

(2013).

107. S. Rajora, M. Butola, and K. Khare, “Mean gradient descent: an optimization approach for single-shot interferogram

analysis,” J. Opt. Soc. Am. A 36(12), D7–D13 (2019).

108. M. Singh, K. Khare, A. K. Jha, S. Prabhakar, and R. Singh, “Accurate multipixel phase measurement with

classical-light interferometry,” Phys. Rev. A 91(2), 021802 (2015).

109. M. Singh and K. Khare, “Accurate efficient carrier estimation for single-shot digital holographic imaging,” Opt.

Lett. 41(21), 4871–4874 (2016).

110. N. Pandey, A. Ghosh, and K. Khare, “Two-dimensional phase unwrapping using the transport of intensity equation,”

Appl. Opt. 55(9), 2418–2425 (2016).

111. V. Balasubramani, A. Kuś, H.-Y. Tu, C.-J. Cheng, M. Baczewska, W. Krauze, and M. Kujawińska, “Holographic

tomography: techniques and biomedical applications,” Appl. Opt. 60(10), B65–B80 (2021).

112. W. Krauze, “Optical diffraction tomography with finite object support for the minimization of missing cone artifacts,”

Biomed. Opt. Express 11(4), 1919–1926 (2020).

113. H. Hugonnet, Y. W. Kim, M. Lee, S. Shin, R. H. Hruban, S.-M. Hong, and Y. Park, “Multiscale label-free volumetric
holographic histopathology of thick-tissue slides with subcellular resolution,” Adv. Photonics 3(02), 026004 (2021).

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35115

114. J. van Rooij and J. Kalkman, “Polarization contrast optical diffraction tomography,” Biomed. Opt. Express 11(4),

2109–2121 (2020).

115. K. C. Zhou, R. Qian, A.-H. Dhalla, S. Farsiu, and J. A. Izatt, “Unified k-space theory of optical coherence

tomography,” arXiv preprint arXiv:2012.04875 (2020).

116. M. Ziemczonok, A. Kuś, P. Wasylczyk, and M. Kujawińska, “3D-printed biological cell phantom for testing 3D

quantitative phase imaging systems,” Sci. Rep. 9(1), 18872–9 (2019).

117. L. Ginner, T. Schmoll, A. Kumar, M. Salas, N. Pricoupenko, L. M. Wurster, and R. A. Leitgeb, “Holographic line
field en-face oct with digital adaptive optics in the retina in vivo,” Biomed. Opt. Express 9(2), 472–485 (2018).
118. O. Thouvenin, K. Grieve, P. Xiao, C. Apelian, and A. C. Boccara, “En face coherence microscopy,” Biomed. Opt.

Express 8(2), 622–639 (2017).

119. C.-H. Liu, A. Schill, R. Raghunathan, C. Wu, M. Singh, Z. Han, A. Nair, and K. V. Larin, “Ultra-fast line-field low
coherence holographic elastography using spatial phase shifting,” Biomed. Opt. Express 8(2), 993–1004 (2017).

120. H. Sudkamp, D. Hillmann, P. Koch, M. Vom Endt, H. Spahr, M. Münst, C. Pfäffle, R. Birngruber, and G. Hüttmann,
“Simple approach for aberration-corrected oct imaging of the human retina,” Opt. Lett. 43(17), 4224–4227 (2018).
121. D. J. Fechtig, T. Schmoll, B. Grajciar, W. Drexler, and R. A. Leitgeb, “Line-field parallel swept source interferometric

imaging at up to 1 mhz,” Opt. Lett. 39(18), 5333–5336 (2014).

122. D. Hillmann, H. Spahr, C. Pfäffle, H. Sudkamp, G. Franke, and G. Hüttmann, “In vivo optical imaging of
physiological responses to photostimulation in human photoreceptors,” Proc. Natl. Acad. Sci. 113(46), 13138–13143
(2016).

123. E. Auksorius, D. Borycki, and M. Wojtkowski, “Crosstalk-free volumetric in vivo imaging of a human retina with
fourier-domain full-field optical coherence tomography,” Biomed. Opt. Express 10(12), 6390–6407 (2019).
124. Y.-Z. Liu, F. A. South, Y. Xu, P. S. Carney, and S. A. Boppart, “Computational optical coherence tomography,”

Biomed. Opt. Express 8(3), 1549–1574 (2017).

125. L. Kastl, M. Isbach, D. Dirksen, J. Schnekenburger, and B. Kemper, “Quantitative phase imaging for cell culture

quality control,” Cytom. Part A 91(5), 470–481 (2017).

126. T. O’Connor, S. Rawat, A. Markman, and B. Javidi, “Automatic cell identification and visualization using digital
holographic microscopy with head mounted augmented reality devices,” Appl. Opt. 57(7), B197–B204 (2018).
127. L. V. Croft, J. A. Mulders, D. J. Richard, and K. O’Byrne, “Digital holographic imaging as a method for quantitative,
live cell imaging of drug response to novel targeted cancer therapies,” in Theranostics, (Springer, 2019), pp.
171–183.

128. G. Di Caprio, M. A. Ferrara, L. Miccio, F. Merola, P. Memmolo, P. Ferraro, and G. Coppola, “Holographic imaging

of unlabelled sperm cells for semen analysis: a review,” J. Biophotonics 8(10), 779–789 (2015).

129. B. Rappaz, P. Jourdain, D. Banfi, F. Kuttler, P. Marquet, and G. Turcatti, “Image-based marker-free screening of
gabaa agonists, antagonists, and modulators,” SLAS DISCOVERY: Adv. Sci. Drug Discov. 25(5), 458–470 (2020).
130. K. Oe and T. Nomura, “Twin-image reduction method using a diffuser for phase imaging in-line digital holography,”

Appl. Opt. 57(20), 5652–5656 (2018).

131. Y. Wu, Y. Luo, G. Chaudhari, Y. Rivenson, A. Calis, K. De Haan, and A. Ozcan, “Bright-field holography:
cross-modality deep learning enables snapshot 3D imaging with bright-field contrast using a single hologram,”
Light: Sci. Appl. 8(1), 25–27 (2019).

132. Y. Rivenson, T. Liu, Z. Wei, Y. Zhang, K. de Haan, and A. Ozcan, “Phasestain: the digital staining of label-free

quantitative phase microscopy images using deep learning,” Light: Sci. Appl. 8(1), 23 (2019).

133. Y. Rivenson, Y. Zhang, H. Günaydın, D. Teng, and A. Ozcan, “Phase recovery and holographic image reconstruction

using deep learning in neural networks,” Light: Sci. Appl. 7(2), 17141 (2018).

134. Y. Rivenson, Y. Wu, and A. Ozcan, “Deep learning in holography and coherent imaging,” Light: Sci. Appl. 8(1),

85–98 (2019).

135. Z. Göröcs, M. Tamamitsu, V. Bianco, P. Wolf, S. Roy, K. Shindo, K. Yanny, Y. Wu, H. C. Koydemir, Y. Rivenson,
and A. Ozcan, “A deep learning-enabled portable imaging flow cytometer for cost-effective, high-throughput, and
label-free analysis of natural water samples,” Light: Sci. Appl. 7, 1–12 (2018).

136. Y.-C. Wu, A. Shiledar, Y.-C. Li, J. Wong, S. Feng, X. Chen, C. Chen, K. Jin, S. Janamian, Z. Yang, Z. S. Ballard, Z.
Göröcs, A. Feizi, and A. Ozcan, “Air quality monitoring using mobile microscopy and machine learning,” Light:
Sci. Appl. 6(9), e17046 (2017).

137. J.-H. Park, J. Park, K. Lee, and Y. Park, “Disordered optics: Exploiting multiple light scattering and wavefront

shaping for nonconventional optical elements,” Adv. Mater. 32(35), 1903457 (2020).

138. H. Yu, K. Lee, J. Park, and Y. Park, “Ultrahigh-definition dynamic 3D holographic display by active control of

volume speckle fields,” Nat. Photonics 11(3), 186–192 (2017).

139. J. Park, K. Lee, and Y. Park, “Ultrathin wide-angle large-area digital 3D holographic display using a non-periodic

photon sieve,” Nat. Commun. 10(1), 1304–1308 (2019).

140. S. Shin, K. Lee, Y. Baek, and Y. Park, “Reference-free single-point holographic imaging and realization of an

optical bidirectional transducer,” Phys. Rev. Appl. 9(4), 044042 (2018).

141. A. P. Mosk, A. Lagendijk, G. Lerosey, and M. Fink, “Controlling waves in space and time for imaging and focusing

in complex media,” Nat. Photonics 6(5), 283–292 (2012).

142. J.-H. Park, C. Park, H. Yu, J. Park, S. Han, J. Shin, S. H. Ko, K. T. Nam, Y.-H. Cho, and Y. Park, “Subwavelength

light focusing using random nanoparticles,” Nat. Photonics 7(6), 454–458 (2013).

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35116

143. K. Lee and Y. Park, “Exploiting the speckle-correlation scattering matrix for a compact reference-free holographic

image sensor,” Nat. Commun. 7(1), 13359–7 (2016).

144. G. Pedrini, Y. Zou, and H. Tiziani, “Digital double-pulsed holographic interferometry for vibration analysis,” J.

Mod. Opt. 42(2), 367–374 (1995).

145. S. Schedin, G. Pedrini, H. J. Tiziani, and F. M. Santoyo, “Simultaneous three-dimensional dynamic deformation

measurements with pulsed digital holography,” Appl. Opt. 38(34), 7056–7062 (1999).
146. T. Yoshizawa, Handbook of Optical Metrology: Principles and Applications (CRC, 2009).
147. G. Pedrini, I. Alekseenko, W. Osten, J. Gaspar, M. E. Schmidt, and O. Paul, “Measurement of nano/micro
out-of-plane and in-plane displacements of micromechanical components by using digital holography and speckle
interferometry,” Opt. Eng. 50(10), 101504 (2011).

148. I. Alekseenko, G. Pedrini, V. Martinez-Garcia, A. Mora, A. Killinger, A. Kozhevnikova, S. Schmauder, R. Gadow,
and W. Osten, “Residual stress evaluation in ceramic coating under industrial conditions by digital holography,”
IEEE Transactions on Ind. Informatics 16(2), 1102–1110 (2019).

149. G. Pedrini, P. Fröning, H. J. Tiziani, and M. E. Gusev, “Pulsed digital holography for high-speed contouring that

uses a two-wavelength method,” Appl. Opt. 38(16), 3460–3467 (1999).

150. G. Pedrini, I. Alekseenko, G. Jagannathan, M. Kempenaars, G. Vayakis, and W. Osten, “Feasibility study of
digital holography for erosion measurements under extreme environmental conditions inside the international
thermonuclear experimental reactor tokamak,” Appl. Opt. 58(5), A147–A155 (2019).

151. P. Picart, New Techniques in Digital Holography (John Wiley & Sons, 2015).
152. T. Biewer, J. Sawyer, C. Smith, and C. Thomas, “Dual laser holography for in situ measurement of plasma facing

component erosion,” Rev. Sci. Instrum. 89(10), 10J123 (2018).

153. M. Fratz, T. Beckmann, J. Anders, A. Bertz, M. Bayer, T. Gießler, C. Nemeth, and D. Carl, “Inline application of

digital holography,” Appl. Opt. 58(34), G120–G126 (2019).

154. M. P. Georges, J.-F. Vandenrijt, C. Thizy, Y. Stockman, P. Queeckers, F. Dubois, and D. Doyle, “Digital holographic
interferometry with CO2 lasers and diffuse illumination applied to large space reflector metrology,” Appl. Opt.
52(1), A102–A116 (2013).

155. E. Meteyer, F. Foucart, M. Secail-Geraud, P. Picart, and C. Pezerat, “Full-field force identification with high-speed

digital holography,” Mech. Syst. Signal Process. 164, 108215 (2022).

156. L. Lagny, M. Secail-Geraud, J. Le Meur, S. Montresor, K. Heggarty, C. Pezerat, and P. Picart, “Visualization of
travelling waves propagating in a plate equipped with 2D ABH using wide-field holographic vibrometry,” J. Sound
Vib. 461, 114925 (2019).

157. L. Valzania, Y. Zhao, L. Rong, D. Wang, M. Georges, E. Hack, and P. Zolliker, “Thz coherent lensless imaging,”

Appl. Opt. 58(34), G256–G275 (2019).

158. R. Horisaki, R. Takagi, and J. Tanida, “Deep-learning-generated holography,” Appl. Opt. 57(14), 3859–3863 (2018).
159. S. Montresor, M. Tahon, A. Laurent, and P. Picart, “Computational de-noising based on deep learning for phase

data in digital holographic interferometry,” APL Photonics 5(3), 030802 (2020).

160. V. Bianco, P. Memmolo, M. Leo, S. Montresor, C. Distante, M. Paturzo, P. Picart, B. Javidi, and P. Ferraro,

“Strategies for reducing speckle noise in digital holography,” Light: Sci. Appl. 7(1), 48 (2018).

161. B. W. Schilling, T.-C. Poon, G. Indebetouw, B. Storrie, K. Shinoda, Y. Suzuki, and M. H. Wu, “Three-dimensional

holographic fluorescence microscopy,” Opt. Lett. 22(19), 1506–1508 (1997).

162. N. T. Shaked, B. Katz, and J. Rosen, “Review of three-dimensional holographic imaging by multiple-viewpoint-

projection based methods,” Appl. Opt. 48(34), H120–H136 (2009).

163. J. Rosen and G. Brooker, “Digital spatially incoherent fresnel holography,” Opt. Lett. 32(8), 912–914 (2007).
164. J. Rosen, A. Vijayakumar, M. Kumar, M. R. Rai, R. Kelner, Y. Kashter, A. Bulbul, and S. Mukherjee, “Recent

advances in self-interference incoherent digital holography,” Adv. Opt. Photonics 11(1), 1–66 (2019).

165. R. Kelner and J. Rosen, “Spatially incoherent single channel digital fourier holography,” Opt. Lett. 37(17), 3723–3725

(2012).

166. A. Vijayakumar, Y. Kashter, R. Kelner, and J. Rosen, “Coded aperture correlation holography–a new type of

incoherent digital holograms,” Opt. Express 24(11), 12430–12441 (2016).

167. A. Bulbul and J. Rosen, “Super-resolution imaging by optical incoherent synthetic aperture with one channel at a

time,” Photonics Res. 9(7), 1172–1181 (2021).

168. E. Cuche, P. Marquet, and C. Depeursinge, “Simultaneous amplitude-contrast and quantitative phase-contrast
microscopy by numerical reconstruction of fresnel off-axis holograms,” Appl. Opt. 38(34), 6994–7001 (1999).
169. K. W. Seo, Y. S. Choi, E. S. Seo, and S. J. Lee, “Aberration compensation for objective phase curvature in phase

holographic microscopy,” Opt. Lett. 37(23), 4976–4978 (2012).

170. T. Colomb, F. Montfort, J. Kühn, N. Aspert, E. Cuche, A. Marian, F. Charrière, S. Bourquin, P. Marquet, and C.
Depeursinge, “Numerical parametric lens for shifting, magnification, and complete aberration compensation in
digital holographic microscopy,” J. Opt. Soc. Am. A 23(12), 3177–3190 (2006).

171. A. Doblas, E. Sánchez-Ortiga, M. Martínez-Corral, G. Saavedra, P. Andrés, and J. Garcia-Sucerquia, “Shift-variant
digital holographic microscopy: inaccuracies in quantitative phase imaging,” Opt. Lett. 38(8), 1352–1354 (2013).
172. E. Sánchez-Ortiga, P. Ferraro, M. Martínez-Corral, G. Saavedra, and A. Doblas, “Digital holographic microscopy

with pure-optical spherical phase compensation,” J. Opt. Soc. Am. A 28(7), 1410–1417 (2011).

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35117

173. A. Doblas, E. Roche, F. J. Ampudia-Blasco, M. Martinez-Corral, G. Saavedra, and J. García-Sucerquia, “Diabetes

screening by telecentric digital holographic microscopy,” J. Microsc. 261(3), 285–290 (2016).

174. S. K. Mirsky and N. T. Shaked, “First experimental realization of six-pack holography and its application to dynamic

synthetic aperture superresolution,” Opt. Express 27(19), 26708–26720 (2019).

175. P. Girshovitz and N. T. Shaked, “Doubling the field of view in off-axis low-coherence interferometric imaging,”

Light: Sci. Appl. 3(3), e151 (2014).

176. N. A. Turko, P. J. Eravuchira, I. Barnea, and N. T. Shaked, “Simultaneous three-wavelength unwrapping using

external digital holographic multiplexing module,” Opt. Lett. 43(9), 1943–1946 (2018).

177. S. K. Mirsky and N. T. Shaked, “Six-pack holographic imaging for dynamic rejection of out-of-focus objects,” Opt.

Express 29(2), 632–646 (2021).

178. L. Wolbromsky, N. A. Turko, and N. T. Shaked, “Single-exposure full-field multi-depth imaging using low-coherence

holographic multiplexing,” Opt. Lett. 43(9), 2046–2049 (2018).

179. G. Dardikman, N. A. Turko, N. Nativ, S. K. Mirsky, and N. T. Shaked, “Optimal spatial bandwidth capacity in
multiplexed off-axis holography for rapid quantitative phase reconstruction and visualization,” Opt. Express 25(26),
33400–33415 (2017).

180. A. Stern, Optical Compressive Imaging (CRC, 2016).
181. Y. Rivenson, A. Stern, and J. Rosen, “Reconstruction guarantees for compressive tomographic holography,” Opt.

Lett. 38(14), 2509–2511 (2013).

182. A. Brodoline, N. Rawat, D. Alexandre, N. Cubedo, and M. Gross, “4D compressive sensing holographic microscopy

imaging of small moving objects,” Opt. Lett. 44(11), 2827–2830 (2019).

183. Y. Rivenson, A. Rot, S. Balber, A. Stern, and J. Rosen, “Imaging through partially occluding media using compressive

sensing,” Opt. Photonics News 23(12), 32 (2012).

184. Y. Oiknine, B. Arad, I. August, O. Ben-Shahar, and A. Stern, “Dictionary based hyperspectral image reconstruction
captured with cs-musi,” in 2018 9th Workshop on Hyperspectral Image and Signal Processing: Evolution in Remote
Sensing (WHISPERS), (IEEE, 2018), pp. 1–5.

185. J. Yim, K. Choi, and S.-W. Min, “Optical sectioning using compressive fresnel holography with dictionary learning,”

Opt. Eng. 57(07), 1 (2018).

186. M. P. Edgar, G. M. Gibson, and M. J. Padgett, “Principles and prospects for single-pixel imaging,” Nat. Photonics

13(1), 13–20 (2019).

187. R. Horisaki, H. Matsui, and J. Tanida, “Single-pixel compressive diffractive imaging with structured illumination,”

188. K. Komuro, Y. Yamazaki, and T. Nomura, “Transport-of-intensity computational ghost imaging,” Appl. Opt. 57(16),

Appl. Opt. 56(14), 4085–4089 (2017).

4451–4456 (2018).

189. P. Clemente, V. Durán, E. Tajahuerce, P. Andrés, V. Climent, and J. Lancis, “Compressive holography with a

single-pixel detector,” Opt. Lett. 38(14), 2524–2527 (2013).

190. L. Martínez-León, P. Clemente, Y. Mori, V. Climent, J. Lancis, and E. Tajahuerce, “Single-pixel digital holography

with phase-encoded illumination,” Opt. Express 25(5), 4975–4984 (2017).

191. H. González, L. Martínez-León, F. Soldevila, M. Araiza-Esquivel, J. Lancis, and E. Tajahuerce, “High sampling
rate single-pixel digital holography system employing a dmd and phase-encoded patterns,” Opt. Express 26(16),
20342–20350 (2018).

192. K. Ota and Y. Hayasaki, “Complex-amplitude single-pixel imaging,” Opt. Lett. 43(15), 3682–3685 (2018).
193. L. Tian and L. Waller, “3D intensity and phase imaging from light field measurements in an led array microscope,”

Optica 2(2), 104–111 (2015).

194. S. Chowdhury, M. Chen, R. Eckert, D. Ren, F. Wu, N. Repina, and L. Waller, “High-resolution 3D refractive index

microscopy of multiple-scattering samples from intensity images,” Optica 6(9), 1211–1219 (2019).

195. J. Lim, A. B. Ayoub, E. E. Antoine, and D. Psaltis, “High-fidelity optical diffraction tomography of multiple

scattering samples,” Light: Sci. Appl. 8(1), 1–12 (2019).

196. M. Chen, D. Ren, H.-Y. Liu, S. Chowdhury, and L. Waller, “Multi-layer born multiple-scattering model for 3D

phase microscopy,” Optica 7(5), 394–403 (2020).

197. W. Tahir, U. S. Kamilov, and L. Tian, “Holographic particle localization under multiple scattering,” Adv. Photonics

1(03), 1 (2019).

198. H. Wang, W. Tahir, J. Zhu, and L. Tian, “Large-scale holographic particle 3D imaging with the beam propagation

model,” Opt. Express 29(11), 17159–17172 (2021).

199. A. Matlock and L. Tian, “Physical model simulator-trained neural network for computational 3D phase imaging of

multiple-scattering samples,” arXiv preprint arXiv:2103.15795 (2021).

200. C. Chang, K. Bang, G. Wetzstein, B. Lee, and L. Gao, “Toward the next-generation vr/ar optics: a review of

holographic near-eye displays from a human-centric perspective,” Optica 7(11), 1563–1578 (2020).

201. Y. Peng, S. Choi, N. Padmanaban, and G. Wetzstein, “Neural holography with camera-in-the-loop training,” ACM

202. Y. Peng, S. Choi, N. Padmanaban, J. Kim, and G. Wetzstein, “Neural holography,” in ACM SIGGRAPH 2020

Transactions on Graph. (TOG) 39(6), 1–14 (2020).

Emerging Technologies, (ACM, 2020), pp. 1–2.

203. P. Chakravarthula, E. Tseng, T. Srivastava, H. Fuchs, and F. Heide, “Learned hardware-in-the-loop phase retrieval

for holographic near-eye displays,” ACM Transactions on Graph. (TOG) 39(6), 1–18 (2020).

Research Article

Vol. 29, No. 22 / 25 Oct 2021 / Optics Express 35118

204. M. H. Eybposh, N. W. Caira, M. Atisa, P. Chakravarthula, and N. C. Pégard, “Deepcgh: 3D computer-generated

holography using deep learning,” Opt. Express 28(18), 26636–26650 (2020).

205. X. Mo, B. Kemper, P. Langehanenberg, A. Vollmer, J. Xie, and G. VonBally, “Application of color digital
holographic microscopy for analysis of stained tissue sections,” in European Conference on Biomedical Optics,
(Optical Society of America, 2009), p. 7367_18.

206. S. H. B. Norazman, T. Nakamura, F. Kimura, and M. Yamaguchi, “Analysis of quantitative phase obtained by digital

holography on H & E-stained pathological samples,” Artif. Life Robotics 24(1), 38–43 (2019).

207. S. H. B. Norazman, T. Nakamura, and M. Yamaguchi, “Digital holography-assisted 3-d bright-field image

reconstruction and refocusing,” Opt. Rev. 27(6), 455–464 (2020).

208. X. Quan, K. Nitta, O. Matoba, P. Xia, and Y. Awatsuji, “Phase and fluorescence imaging by combination of digital

holographic microscopy and fluorescence microscopy,” Opt. Rev. 22(2), 349–353 (2015).

209. M. Yamaguchi, H. Hoshino, T. Honda, and N. Ohyama, “Phase-added stereogram: calculation of hologram using

computer graphics technique,” Proc. SPIE 1914, 25–31 (1993).

210. M. Yamaguchi, “Light-field and holographic three-dimensional displays,” J. Opt. Soc. Am. A 33(12), 2348–2364

(2016).

