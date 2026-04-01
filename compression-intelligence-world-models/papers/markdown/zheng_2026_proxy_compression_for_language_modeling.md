|     |            | Proxy | Compression |     |          | for Language  | Modeling |               |     |     |     |     |
| --- | ---------- | ----- | ----------- | --- | -------- | ------------- | -------- | ------------- | --- | --- | --- | --- |
|     | LinZheng*1 |       | XinyuLi*1   |     | QianLiu2 | XiachongFeng1 |          | LingpengKong1 |     |     |     |     |
Abstract compressioniscomputationallyessential,asitreducesthe
sequencelengthandthusenablesefficienttraining.
Modernlanguagemodelsaretrainedalmostex-
clusivelyontokensequencesproducedbyafixed However,thisdesigncouplestheentiremodelingstackto
tokenizer,anexternallosslesscompressoroften afixedexternalcompressor. Everyinputandoutputmust
6202 beF 4  ]LC.sc[  1v98240.2062:viXra over UTF-8 byte sequences, thereby coupling passthroughit,andatthelevelofrawdata,1 themodelis
the model to that compressor. This work intro- nolongerstrictlyend-to-end,asitlearnsonlytomanipulate
ducesproxycompression,analternativetraining thecompressor’soutputs. Inthecaseofhand-craftedtok-
scheme that preserves the efficiency benefits of enizers,thiscouplingintroduceswell-documentedartifacts
compressedinputswhileprovidinganend-to-end, (Phanetal.,2024), includingpromptboundaryproblems
raw-byteinterfaceatinferencetime. Duringtrain- (Microsoft,2023;Lundberg&Ribeiro,2023;Athiwaratkun
ing, one language model is jointly trained on etal.,2024;Hayaseetal.,2025),retokenizationdrift(Team,
rawbytesequencesandcompressedviewsgen- 2025),under-trainedorglitchtokens(Rumbelow&Watkins,
eratedbyexternalcompressors;throughthepro- 2023; Land & Bartolo, 2024; Wang et al., 2024a; Yang,
cess, the model learns to internally align com- 2024; Yang et al., 2024), data mixture leakage (Hayase
pressed sequences and raw bytes. This align- etal.,2024),biasesagainstlow-resourcelanguages(Petrov
ment enables strong transfer between the two etal.,2023;Ahiaetal.,2023;Limisiewiczetal.,2024),and
formats, even when training predominantly on increasedsensitivitytoadversarialinputs(Sunetal.,2020;
| compressedinputswhicharediscardedatinfer- |             |     |     |               |     | Pagnonietal.,2024). |     |     |     |     |     |     |
| ----------------------------------------- | ----------- | --- | --- | ------------- | --- | ------------------- | --- | --- | --- | --- | --- | --- |
| ence. Extensive                           | experiments |     | on  | code language |     |                     |     |     |     |     |     |     |
Inthiswork,weaskwhetheritispossibletokeeptheef-
| modeling      | demonstrate | that    | proxy           | compression |       |                                                  |           |                   |               |         |      |          |
| ------------- | ----------- | ------- | --------------- | ----------- | ----- | ------------------------------------------------ | --------- | ----------------- | ------------- | ------- | ---- | -------- |
|               |             |         |                 |             |       | ficiency                                         | benefits  | of training       | on compressed |         | data | without  |
| substantially | improves    |         | training        | efficiency  | and   |                                                  |           |                   |               |         |      |          |
|               |             |         |                 |             |       | hard-wiringthecompressorintothemodel’sinterface. |           |                   |               |         |      | We       |
| significantly | outperforms |         | pure byte-level |             | base- |                                                  |           |                   |               |         |      |          |
|               |             |         |                 |             |       | address                                          | this with | proxy compression |               | (Figure | 1):  | treating |
| lines given   | fixed       | compute | budgets.        | As          | model |                                                  |           |                   |               |         |      |          |
externalcompressorsasatraining-timeproxyratherthana
| scale increases, | these             | gains | become | more       | pro- |                             |     |     |                         |     |     |     |
| ---------------- | ----------------- | ----- | ------ | ---------- | ---- | --------------------------- | --- | --- | ----------------------- | --- | --- | --- |
|                  |                   |       |        |            |      | permanentpartofthepipeline. |     |     | Givenatrainingcorpus,we |     |     |     |
| nounced,         | and proxy-trained |       | models | eventually |      |                             |     |     |                         |     |     |     |
applyanexternalcompressortoproducecompressedviews
| match or | rival tokenizer |     | approaches, | all | while |     |     |     |     |     |     |     |
| -------- | --------------- | --- | ----------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
ofeachsequenceandmixthesecompressedsequenceswith
| operating                               | solely on | raw | bytes and | retaining | the |                                     |         |            |             |     |                 |      |
| --------------------------------------- | --------- | --- | --------- | --------- | --- | ----------------------------------- | ------- | ---------- | ----------- | --- | --------------- | ---- |
|                                         |           |     |           |           |     | rawUTF-8counterpartsduringtraining. |         |            |             |     | Asinglelanguage |      |
| inherentrobustnessofbyte-levelmodeling. |           |     |           |           | Our |                                     |         |            |             |     |                 |      |
|                                         |           |     |           |           |     | model is                            | trained | to perform | next-symbol |     | prediction      | over |
https://github.com/
| code is available |     | at  |     |     |     |                      |     |          |     |           |       |        |
| ----------------- | --- | --- | --- | --- | --- | -------------------- | --- | -------- | --- | --------- | ----- | ------ |
|                   |     |     |     |     |     | both representations |     | jointly. | At  | inference | time, | we can |
LZhengisme/proxy-compression.
discardthecompressorentirelyandrunthemodelonraw
|     |     |     |     |     |     | bytes alone;                                      | the | compressor | has | served | only to | provide |
| --- | --- | --- | --- | --- | --- | ------------------------------------------------- | --- | ---------- | --- | ------ | ------- | ------- |
|     |     |     |     |     |     | shorterproxysequencesduringtrainingforefficiency. |     |            |     |        |         | Our     |
1.Introduction
centralfindingenablingproxycompressionisstrongcross-
Modernlanguagemodelsarealmostalwaystrainedoncom- representationtransfer: althoughthemajorityoftraining
|     |     |     |     |     |     | data is specified |     | in compressed | form | for | efficiency | (e.g., |
| --- | --- | --- | --- | --- | --- | ----------------- | --- | ------------- | ---- | --- | ---------- | ------ |
pressedviewsofdataratherthanonitsrawformat(Bengio
etal.,2003). Inpractice,thecompressor,mostcommonlya 90%), the model performs surprisingly well on raw-byte
tokenizer(Sennrichetal.,2016;Kudo&Richardson,2018) inference.Moreover,transferstrengthofproxycompression
|     |     |     |     |     |     | growswithmodelscale: |     | smallmodelsdemonstrateweakor |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------------------- | --- | ---------------------------- | --- | --- | --- | --- |
orarithmeticcodingwithanotherlanguagemodel(Lester
et al., 2024), maps the raw input into a shorter sequence negativetransfer,whilelargermodelswithproxycompres-
sionevenmatchorsurpassordinarylanguagemodelswith
| ofdiscretetokensthatthemodelactuallyprocesses. |     |     |     |     |     | This |     |     |     |     |     |     |
| ---------------------------------------------- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
*Equalcontribution 1UniversityofHongKong2TikTok.Corre- 1WeuserawtorefertotheUTF-8byteencodingoftext,con-
trastingitwithcompressedsequencesoftenderivedfromthatbyte
spondenceto:LinZheng<lzheng2@cs.hku.hk>.
stream,suchastokenizedtext.
Preprint.February5,2026.
1

ProxyCompressionforLanguageModeling
|     | Training Data Preparation |     |     |                             |     |     | Modeling               |     |     |     |     |
| --- | ------------------------- | --- | --- | --------------------------- | --- | --- | ---------------------- | --- | --- | --- | --- |
|     |                           |     |     | Mixed-representation inputs |     |     | Next-symbol prediction |     |     |     |     |
<comp> 733, 8223, 1187, 8338, 7144, …
|     |     |     |     | </comp> | <comp> 733, 1231, 4494, |     |     |     |     |     |     |
| --- | --- | --- | --- | ------- | ----------------------- | --- | --- | --- | --- | --- | --- |
733, 8223, 1187, 8338, 7144, 62780,
|     |     |     |     | 7390, 11507, … </comp> | <raw> 10, |     |     |     |     |     |     |
| --- | --- | --- | --- | ---------------------- | --------- | --- | --- | --- | --- | --- | --- |
7054, 285, 1087, 271, 2436, 1783,
|     |     |     |     | 100, 101, 102, 32, 113, 117, 105, … </raw> |     |     |     | Language Model |     |     |     |
| --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | -------------- | --- | --- | --- |
5072, 285, 1006, 763, 702, …
|     |     |     |     | <comp> 733, … </comp> |     | <comp> |     |     |     |     |     |
| --- | --- | --- | --- | --------------------- | --- | ------ | --- | --- | --- | --- | --- |
Proxy Compressor
|     | (Tokenization / Neural / Gzip) |     |       | 741, 1786, 763, 988, 347, 848, … </comp>    |     |     |                                 |     |     |     |     |
| --- | ------------------------------ | --- | ----- | ------------------------------------------- | --- | --- | ------------------------------- | --- | --- | --- | --- |
|     |                                |     |       | 10, 100, 101, 102, 32, 113, 117, 105, 99,   |     |     | 10, 97, 115, 121, 110, 99, 32,  |     |     |     |     |
|     | Training corpus                |     |       | 107, 115, 111, 114, 116, 40, 97, 114, 114,  |     |     | 100, 101, 102, …                |     |     |     |     |
|     |                                |     | UTF-8 | 58, 32, 108, 105, 115, 116, 91, …           |     |     |                                 |     |     |     |     |
Byte-level Inference
Figure1.Overviewofproxycompressionforlanguagemodeling.Duringtraining,wepreparemixed-representationinputsbycombining
compressedsequenceswithrawUTF-8bytes,whicharepackedtogethertotrainasinglelanguagemodelwithnext-symbolprediction
overbothrepresentations.Differentrepresentationsareassociatedwithspecialsentinels,suchas⟨comp⟩,⟨/comp⟩forcompresseddata
and⟨raw⟩and⟨/raw⟩forrawdata.Atinferencetime,theproxycompressorisdiscardedentirely,andthemodeloperatessolelyonraw
bytes.Bytrainingprimarilyoncompresseddata(e.g.,90%oftrainingdatainthiswork),thisapproachcapturesthetrainingefficiency
benefitsofcompresseddatawithouthard-wiringthecompressorintothemodel’sinterface.
hard-wiredcompressors(Figure2). 8nonethelessoutperformpureraw-bytebaselinesundera
|               |                   |       |     |              | fixed compute | budget, | as  | they can | consume | substantially |     |
| ------------- | ----------------- | ----- | --- | ------------ | ------------- | ------- | --- | -------- | ------- | ------------- | --- |
| Conceptually, | proxy compression | makes | the | learning ob- |               |         |     |          |         |               |     |
morecompresseddatawhilebenefitingfromstrongtrans-
| jectivemoredemandinginausefulway. |     |     | Themodelmust |     |     |     |     |     |     |     |     |
| --------------------------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
fer;atscale,theymatchorsurpassstrongtokenizer-based
| predict in | two different code | spaces | and implicitly | align |            |                                              |     |     |     |     |     |
| ---------- | ------------------ | ------ | -------------- | ----- | ---------- | -------------------------------------------- | --- | --- | --- | --- | --- |
|            |                    |        |                |       | baselines. | In-contexttransferprobes(§3.3)showthatproxy- |     |     |     |     |     |
them, learninganinternalmappingbetweenproxycodes
trainedmodelscannear-perfectlyrecoverrawinputsfrom
| andbytes. | Thisencouragesthemodeltotreatcompressed |     |     |     |     |     |     |     |     |     |     |
| --------- | --------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
theircompressedformsincontext.Wetheninvestigatewhat
sequencesasinformativehintsratherthanacompletesub-
|                             |               |                         |         |            | makes a      | good proxy      | compressor | §3.4,  | where          | gzip | prox-    |
| --------------------------- | ------------- | ----------------------- | ------- | ---------- | ------------ | --------------- | ---------- | ------ | -------------- | ---- | -------- |
| stitutefortherawbytestream. |               | Fromacodingperspective, |         |            |              |                 |            |        |                |      |          |
|                             |               |                         |         |            | ies fail to  | transfer,       | possibly   | due to | their unstable |      | outputs, |
| a language                  | model defines | a compressor            | via its | predictive |              |                 |            |        |                |      |          |
|                             |               |                         |         |            | whereas both | tokenizer-based |            | and    | neural proxies |      | support  |
distribution(Deletangetal.,2024);proxycompressioncan
|     |     |     |     |     | strong transfer. | Robustness |     | evaluations | (§3.5) | show | that |
| --- | --- | --- | --- | --- | ---------------- | ---------- | --- | ----------- | ------ | ---- | ---- |
thusbeviewedaspartiallydelegatingcompressiontoanex-
proxy-trainedmodelsretainmostoftheinherentrobustness
ternalproxywhiletrainingthemodeltoremainaneffective
ofrawbyte-levelmodeling.
| compressoroverrawbytes. |     | Thisnavigatesafundamental |     |     |     |     |     |     |     |     |     |
| ----------------------- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
trade-off: training on purely compressed data is efficient Insummary,thisworkmakesthefollowingcontributions:
butconstrainsthemodeltopatternsthecompressorexposes,
while training with pure raw bytes captures all structure • Weintroduceproxycompression,amixed-representation
trainingschemethatenablesefficienttrainingovercom-
| butathighcomputationalcost. |     | Proxycompressiongains |     |     |     |     |     |     |     |     |     |
| --------------------------- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
presseddatawhilekeepingasimple,raw-byteinference
efficiencyfromcompressedinputswhilestayinggrounded
interface,withoutmodifyingmodelarchitectures.
intheunderlyingbyte-leveldistribution.
• Wedemonstratestrongcross-representationtransferwith
| We instantiate     | proxy compression                 |     | with several | families |                    |     |        |         |               |     |     |
| ------------------ | --------------------------------- | --- | ------------ | -------- | ------------------ | --- | ------ | ------- | ------------- | --- | --- |
|                    |                                   |     |              |          | proxy compression: |     | models | trained | predominantly |     | on  |
| ofcompressors(§2): | tokenizer-basedcompression(§2.2), |     |              |          |                    |     |        |         |               |     |     |
proxy-compressedinputssubstantiallyoutperformpure
whichusesconventionaltokenizersasproxycompressors;
neural proxy compressors (§2.3), which combine a sep- raw-bytebaselinesandrivaltokenizer-basedapproaches
atscale,withtheperformancegapnarrowingasthemodel
| arately trained | byte-level | model with | arithmetic | coding |     |     |     |     |     |     |     |
| --------------- | ---------- | ---------- | ---------- | ------ | --- | --- | --- | --- | --- | --- | --- |
scaleincreases.
| (Lesteretal.,2024);    | andgeneric,structure-agnosticcom- |     |     |     |     |     |     |     |     |     |     |
| ---------------------- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pressionviagzip(§2.4). | Ourexperimentsoncodelanguage      |     |     |     |     |     |     |     |     |     |     |
• Wesystematicallystudyseveralproxycompressors,in-
modeling(§3)demonstratethatproxycompressionyields cludinggenericgzip,tokenizer-basedcompression,and
| strong transfer | from compressed | training | to  | raw-byte in- |     |     |     |     |     |     |     |
| --------------- | --------------- | -------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
arithmetic-codedneuralproxies,showingthatmorestruc-
ference. Ondownstreambenchmarks(§3.2), modelsthat turedcompressors(tokenizer-basedandneural)arehighly
see only about 10% of their training tokens in raw UTF- effectiveproxiesfortraininglanguagemodels,whilegzip-
2

ProxyCompressionforLanguageModeling
Tokenizer-based efficiencywhileretainingauniversalbyte-levelinterface.
| 50.0 |     |     |     |     | +4.0 |     |     |     |     |     |     |     |     |
| ---- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
Byte-level
Proxy (Neural)
|      | Proxy (Tokenizer) |     |     |     | 1.3 +2.0 |     |     |     |     |     |     |     |     |
| ---- | ----------------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
| 45.0 |                   |     |     | 1.1 |          |     |     |     |     |     |     |     |     |
)%( 1@ssaP sulP-PPBM  Byte-level FormatSentinelTokens. Tomakedifferentrepresenta-
|     |  Proxy (Neural) |     |     |     | .freP rezinekoT ot  |     |     |     |     |     |     |     |     |
| --- | --------------- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
40.0  Proxy (Tokenizer) +0.0 tions explicitly distinguishable, we wrap each sequence
-1.9
|      |      |      |      |      | -2.0 | withspecialsentineltokensthatindicateitsformat. |         |                       |                             |         |                     |     | Raw |
| ---- | ---- | ---- | ---- | ---- | ---- | ----------------------------------------------- | ------- | --------------------- | --------------------------- | ------- | ------------------- | --- | --- |
| 35.0 |      |      |      |      |      |                                                 |         |                       |                             |         | (cid:2)             |     |     |
|      | -3.4 |      |      |      |      | andcom                                          | pres    | sedsequencesareencode |                             |         | das ⟨raw⟩◦x         |     | ◦   |
|      | -4.0 |      |      |      |      |                                                 |         |                       |                             |         |                     |     | raw |
|      |      | -4.5 | -4.5 |      | -4.0 |                                                 | (cid:3) | (cid:2)               |                             | (cid:3) |                     |     |     |
| 30.0 |      |      |      |      |      | ⟨/raw⟩                                          | and     | ⟨comp⟩◦x              | ◦⟨/comp⟩                    |         | ,respectively,where |     |     |
|      |      |      |      | -6.1 |      |                                                 |         |                       | comp                        |         |                     |     |     |
|      |      |      |      |      | -6.0 | ◦denotesconcatenation.                          |         |                       | Thesemarkersallowthemodelto |         |                     |     |     |
25.0
|     | -7.4 |     |     |     |     | conditionitspredictionsontherepresentationtype.2 |     |     |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
-8.0
20.0
|     | 0.5B | 4B  |     | 14B |     |     |     |     |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Model Size
|     |     |     |     |     |     | In-contextTranslationPairing. |     |     |     | Thesamplingscheme |     |     |     |
| --- | --- | --- | --- | --- | --- | ----------------------------- | --- | --- | --- | ----------------- | --- | --- | --- |
Figure2. Modelperformance(Pass@1)onMBPP-Plusacross above treats raw and compressed samples independently.
modelscales. Barsshowabsoluteperformance(leftaxis);lines To further encourage cross-representation alignment, we
showtheperformancegap(∆)relativetothetokenizerbaseline
introducein-contexttranslationpairing,whichoptionally
(rightaxis).Whilebyte-levelmodelsexhibitapersistentorwiden-
presentsbothviewsofthesamesampleconcatenatedwithin
inggap,proxy-basedmodelsprogressivelyclosethegapasthe
modelscaleincreases. a single context (the ordering between x raw and x comp is
randomizedwithequalprobability),
basedcompressionfailstotransfereffectively.
|     |     |     |     |     |     |     | (cid:2) ⟨raw⟩◦x | ◦⟨/raw⟩◦⟨comp⟩◦x |     |     | ◦⟨/comp⟩ |     | (cid:3) . |
| --- | --- | --- | --- | --- | --- | --- | --------------- | ---------------- | --- | --- | -------- | --- | --------- |
|     |     |     |     |     |     |     |                 | raw              |     |     | comp     |     |           |
2.ProxyCompression
Thesepairedsequencesencouragethemodeltopredictone
representationconditionedontheother,effectivelylearning
| We introduce | proxy compression, |     | a   | training | scheme that |     |            |               |         |          |     |             |     |
| ------------ | ------------------ | --- | --- | -------- | ----------- | --- | ---------- | ------------- | ------- | -------- | --- | ----------- | --- |
|              |                    |     |     |          |             | an  | in-context | “translation” | between | formats. |     | By default, |     |
retainstheefficiencyofcompressedinputswhileexposing
|               |            |           |     |            |          | pairing | is  | enabled only | during | an initial | warm-up |     | phase |
| ------------- | ---------- | --------- | --- | ---------- | -------- | ------- | --- | ------------ | ------ | ---------- | ------- | --- | ----- |
| an end-to-end | byte-level | interface | at  | inference. | §2.1 de- |         |     |              |        |            |         |     |       |
(§2.5);furtheranalysisisprovidedinAppendixD.8.
scribesthecoreframework,§§2.2to2.4presentconcrete
instantiationsoftheproxycompressor,and§2.5provides Note that mixed-representation training usually yields a
implementationdetails. lowereffectivecompressionratethantheproxycompressor
|     |     |     |     |     |     | f   | alone;seeAppendixAformoredetaileddiscussion. |     |     |     |     |     | We  |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- | --- | --- |
2.1.Overview nextdescribeconcreteinstantiationsoff thatproducedis-
cretesymbolsequencesamenabletoofflinepreprocessing.
Letx denotearawinputsampleinUTF-8bytes,andlet
raw
| x :=f(x | )bearepresentationcompressedbyaproxy |     |     |     |     |     |     |     |     |     |     |     |     |
| ------- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| comp    | raw                                  |     |     |     |     |     |     |     |     |     |     |     |     |
2.2.Tokenizer-basedCompressors
| compressorf. | Weassumex |     | isasequenceofdiscrete |     |     |     |     |     |     |     |     |     |     |
| ------------ | --------- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
comp
symbolsfromafinitevocabulary,sothatbothformatscan Anaturalinstantiationoftheproxycompressorf isstan-
behandledseamlesslybyastandardlanguagemodel. dard tokenization. Given a trained tokenizer (Sennrich
etal.,2016;Kudo&Richardson,2018;Liuetal.,2025),
Mixed-RepresentationTraining. Ourtrainingpipeline it segments x raw into token indices from a fixed-size vo-
operatesatthesamplelevel. Foreachinputx ,wedrawa cabularytoobtainx . Thissatisfiesourdesigncriteria:
|     |     |     |     | raw |     |     |     | comp |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
theoutputisadiscretesequence,andtokenizationcanbe
Bernoullivariablesuchthatwithprobabilityr,thesample
ispresentedincompressedformx ,otherwiseitremains performed entirely offline. Conceptually, the use of tok-
comp
enizationforproxycompressiondiffersfromconventional
| as x raw . | The resulting | sequences | are | packed | into fixed- |     |     |     |     |     |     |     |     |
| ---------- | ------------- | --------- | --- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
lengthcontexts,whichmaycontainbothformatswithinthe tokenizer-basedlanguagemodeltraining. Whereasastan-
samecontext,andasinglestandardautoregressivemodel dardtokenizer-basedmodeloperatesexclusivelyintoken
spaceandalmostneverseesrawbytes,ourapproachinstead
| is trained | with the usual | next-token |     | prediction | objective |     |     |     |     |     |     |     |     |
| ---------- | -------------- | ---------- | --- | ---------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
on both compressed and raw sequences. Crucially, this treatstokens asatraining-timeproxyforefficient, which
schemerequiresnoarchitecturalchanges;allmodifications still retaining a raw-byte interface at inference. We also
exploredalternativetokenencodings(e.g.,mappingtoken
areconfinedtothedatapreprocessingpipeline.
IDstofixed-lengthbytesequences);thesevariantsdidnot
|                      |     |                               |     |     |     | improve |     | over direct token-index |     | representations |     | and | are |
| -------------------- | --- | ----------------------------- | --- | --- | --- | ------- | --- | ----------------------- | --- | --------------- | --- | --- | --- |
| Byte-levelInference. |     | Atinferencetime,themodeloper- |     |     |     |         |     |                         |     |                 |     |     |     |
discussedinAppendixB.1.
atesexclusivelyonrawUTF-8bytes;theproxycompressor
is used only during training and can be discarded after- 2Sentineltokensalsoimproveperformanceatsmallermodel
wards. Thisdecouplingleveragescompressionfortraining
scaleswithdiminishinggainsatlargerscales;seeAppendixD.10.
3

ProxyCompressionforLanguageModeling
2.3.NeuralCompressors frequentlossspikes;moreover,ityieldsweakorevennega-
|     |     |     |     |     |     |     | tivetransfertoraw-byteperformance. |     | Wehypothesizethat |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | ----------------- | --- | --- |
Beyondtokenization,westudyneuralproxycompressors
gzip’sdynamicformat(withalgorithm-inducedlong-range
| basedonarithmeticcoding(Lesteretal.,2024). |     |     |     |     | Wetrain |     |     |     |     |     |     |
| ------------------------------------------ | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
dependenciesandlimitedstructuralregularityacrosssam-
asmallbyte-levellanguagemodel(∼40Mparameters)on
ples)producespatternsthataredifficultforlanguagemodels
rawUTF-8datatoobtainconditionalprobabilityestimates
|          |               |     |              |        |      |       | tolearn. | Weanalyzethisfailuremodeindetailin§3.4. |     |     |     |
| -------- | ------------- | --- | ------------ | ------ | ---- | ----- | -------- | --------------------------------------- | --- | --- | --- |
| for each | byte position |     | of the input | x . We | then | apply |          |                                         |     |     |     |
raw
arithmeticcodingwithequal-informationwindows(Lester
2.5.ImplementationDetails
| etal.,2024)tox |     | usingtheseprobabilitiestoproducea |     |     |     |     |     |     |     |     |     |
| -------------- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
raw
| compressedbitstream, |     |     | whichisthenpackedintodiscrete |     |     |     |                         |     |                     |     |     |
| -------------------- | --- | --- | ----------------------------- | --- | --- | --- | ----------------------- | --- | ------------------- | --- | --- |
|                      |     |     |                               |     |     |     | MixingTrainingSchedule. |     | Wesetthemixingrater |     | =   |
symbolstoformx comp . 0.9,sothat90%oftrainingsamplesarepresentedincom-
|     |     |     |     |     |     |     | pressed | form and only 10% | as raw bytes. | In this | case, |
| --- | --- | --- | --- | --- | --- | --- | ------- | ----------------- | ------------- | ------- | ----- |
Anaiveimplementationofthispipelineisprohibitivelyslow
tokenizer-basedandneuralproxycompressorsachieveav-
| duetothesequentialnatureofarithmeticcoding. |     |     |     |     | Toenable |     |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
eragecompressionratesofroughly2.9×and2.6×,respec-
neuralcompressorsatscale,weintroduceanentropy-based
segmentationstrategy: weusethecompressormodeltoesti- tively. During an initial warm-up phase (first 10k steps),
weenablein-contexttranslationpairing(§2.1)andlinearly
mateper-byteentropy,identifysegmentboundariesathigh-
increaserfrom0.4to0.9;afterwarm-up,pairingisdisabled
entropypositions,andcompresssegmentsindependentlyin
|     |     |     |     |     |     |     | andrremainsfixedat0.9. |     | Wealsoexploredstartingfrom |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | -------------------------- | --- | --- |
parallel. Thisisessentialformakingneuralproxycompres-
|     |     |     |     |     |     |     | differentratessuchasr | =0.1andobservednosignificant |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------- | ---------------------------- | --- | --- | --- |
sionpracticalonlarge-scalecorpus,notonlyimprovingthe
|     |     |     |     |     |     |     | differenceinfinalperformance. |     | Allproxy-trainedmodels |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------- | --- | ---------------------- | --- | --- |
compressionthroughputbutalsoyieldingbetterempirical
|     |     |     |     |     |     |     | are evaluated | exclusively | on raw byte inputs | at inference |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | ----------- | ------------------ | ------------ | --- |
performance;fulldetailsareprovidedinAppendixB.2.
timeunlessotherwisenoted(§3.6).
| NeurallyCompressedRepresentationsareFuzzy. |     |        |                   |      |            | Neu- |             |                                     |     |     |     |
| ------------------------------------------ | --- | ------ | ----------------- | ---- | ---------- | ---- | ----------- | ----------------------------------- | --- | --- | --- |
|                                            |     |        |                   |      |            |      | Vocabulary. | Sinceinputsequencesnowconsistofboth |     |     |     |
| ral compressors                            |     | behave | quite differently | from | tokenizer- |      |             |                                     |     |     |     |
compressedandrawsequences,weuseasharedvocabulary
| based compressors. |     | Although | each | raw input | x raw | maps |     |     |     |     |     |
| ------------------ | --- | -------- | ---- | --------- | ----- | ---- | --- | --- | --- | --- | --- |
toaccommodatebothrawbytesandcompressedsymbols,
| deterministicallytoauniquecompressedsequencex |     |     |     |     |     |      | ,                     |                                  |     |     |     |
| --------------------------------------------- | --- | --- | --- | --- | --- | ---- | --------------------- | -------------------------------- | --- | --- | --- |
|                                               |     |     |     |     |     | comp | partitionedasfollows: | thefirst64indicesinthevocabulary |     |     |     |
not
| the reverse | mapping   | is  | generally       | unique: | given      | only |                                                   |             |                  |             |     |
| ----------- | --------- | --- | --------------- | ------- | ---------- | ---- | ------------------------------------------------- | ----------- | ---------------- | ----------- | --- |
|             |           |     |                 |         |            |      | are reserved                                      | for special | sentinel tokens, | followed by | 256 |
| x and       | no record | of  | the compressing | model   | probabili- |      |                                                   |             |                  |             |     |
| comp        |           |     |                 |         |            |      | entriesforrawUTF-8bytevalues,withremainingindices |             |                  |             |     |
tiesusedduringencoding,theremightbemultipledistinct
|     |     |     |     |     |     |     | assignedtocompressedsymbols. |     | Fortokenizer-basedproxy |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------- | --- | ----------------------- | --- | --- |
rawbytesequencescorrespondingtothesamecompressed
compressors,weusetheOpenCodertokenizervocabulary
| stream. | We refer | to the | compressed | inputs | as “fuzzy” | in  |                                      |     |     |               |     |
| ------- | -------- | ------ | ---------- | ------ | ---------- | --- | ------------------------------------ | --- | --- | ------------- | --- |
|         |          |        |            |        |            |     | (Huangetal.,2024a)with96,640symbols. |     |     | Forneuralcom- |     |
thesensethatneuralcompressioninducesamany-to-one
pression,wepackevery16bitsintoacompressedsymbol
mappingfromrawbytestocompressedsymbols.
|     |     |     |     |     |     |     | (a65,536-wayalphabet). |     | Thegzip-basedproxycompressor |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | ---------------------------- | --- | --- |
Importantly,thisambiguityishighlystructuredratherthan worksatthebytelevelover256compressedsymbols.
arbitrary. Asweanalyzein§3.4,collisionstypicallygroup
togetherrawbytesequencesthatdifferonlyinsuperficial,
3.Experiments
low-entropydetails(suchaswhitespace,newlines,andin-
dentation),whilepreservingtheirsemanticcontent. Unlike Inthissection,weempiricallyevaluateproxycompressed
tokenization,wecannotlosslesslydecodex backtox . inputs. We first describe the experimental setup in §3.1,
|     |     |     |     | comp |     | raw |     |     |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
However,forproxycompressionthiscontrolledambiguity study transfer from proxy compressors at scale in §§3.2
turnsouttobebeneficial: itabstractsawayformattingnoise and3.3,comparesdifferentproxycompressors(§3.4),and
and implicitly shares representations across semantically finallyevaluatetherobustnessofourapproachin§3.5.
equivalentpatterns.
3.1.Setup
2.4.GzipCompressors
AlltrainingexperimentsusetheRefineCodecorpus(Huang
We also instantiate f using general-purpose compres- et al., 2024a), where we primarily use its Python subset,
sors. We apply gzip (via Python’s standard library with totalingroughly270GBofPythonsourcecode,anditsfull
gzip(*,mtime=0)toremovevariationduetoheaders GitHubsplit(usedin§3.2)withapproximately3.3TBof
andtrailers)directlytox andtreattheoutputbytestream codeacrossmultipleprogramminglanguages. Wetraina
raw
asx . Onourcorpus,gzipachievesacompressionrate familyoflanguagemodelsfollowingtheEvaBytearchitec-
comp
ofroughly2.5overx raw . Despiteitssimplicity,gzipproves ture(Zhengetal.,2025b)at0.5B,1.5B,4B,7B,and14B
tobeapoorproxyrepresentation. Trainingonmixedgzip- parameters. Trainingrunsfor50Kstepswithafixedbatch
compressedandrawbytesishighlyunstableandexhibits size of 2M sequence symbols (e.g., UTF-8 bytes, tokens,
4

ProxyCompressionforLanguageModeling
Table1. Downstreampass@1performanceonHumanEval-Plus
|     |     |     |     |     |     | 0.300 |     |     |     | 0.300 |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ----- | --- | --- |
andMBPP-Plusacrossdifferentmodelsizesandinputrepresenta-
|     |     |     |     |     |     | 0.275 |     |     |     | 0.275 |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ----- | --- | --- |
tions.CRdenotescompressionrate(avg.bytespersymbol).All
|     |     |     |     |     |     | 0.250 |     |     |     | 0.250 |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ----- | --- | --- |
modelsaretrainedwithafixedbudgetof100Bsymbols(tokens 1@ssaP 0.225 1@ssaP 0.225
orbytes);largermodels(7B,14B)maybeundertrainedrelativeto 0.200 0.200
| compute-optimalscaling(Hoffmannetal.,2022). |                 |     |           |        |           | 0.175 |                              |                              |      | 0.175 |                              |             |
| ------------------------------------------- | --------------- | --- | --------- | ------ | --------- | ----- | ---------------------------- | ---------------------------- | ---- | ----- | ---------------------------- | ----------- |
|                                             |                 |     |           |        |           | 0.150 | B y                          | te - l e v e l               |      | 0.150 | Byte-level                   |             |
|                                             |                 |     |           |        |           |       | Pr o                         | x y   C o m pressor (Neural) |      |       | Proxy Compressor (Neural)    |             |
|                                             |                 |     |           |        |           | 0.125 | Proxy Compressor (Tokenizer) |                              |      | 0.125 | Proxy Compressor (Tokenizer) |             |
|                                             |                 |     |           | Mod el | Size      |       | Tokenizer-based              |                              |      |       | Tokenizer-based              |             |
| Task                                        | Model           | CR  |           |        |           | 0.100 |                              |                              |      | 0.100 |                              |             |
|                                             |                 |     | 0.5B 1.5B | 4 B    | 7B 14B    | 2     | 4                            | 6                            | 8    |       | 50 100 150 200               | 250 300 350 |
|                                             |                 |     |           |        |           |       | T otal Trainin               | g FLOPs                      | 1e21 |       | Training Bytes (B)           |             |
|                                             | Tokenizer-based | 3.7 | 17.7 18.3 | 28.0   | 28.7 29.3 |       |                              |                              |      |       |                              |             |
Figure3.Pass@1performanceonHumanEval-Plusfor14Bmod-
|     | Byte-level | 1.0 | 15.9 18.3 | 22.0 | 23.8 24.4 |     |     |     |     |     |     |     |
| --- | ---------- | --- | --------- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
HumanEval-Plus elsunderdifferentinputrepresentations,comparedasafunction
|     | Proxy(Neural) | 2.6 | 13.4 18.3 | 22.6 | 26.8 29.9 |     |     |     |     |     |     |     |
| --- | ------------- | --- | --------- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
Proxy(Tokenizer) 2.9 12.2 20.7 24.4 26.2 30.5 oftrainingFLOPs(left)andamountoftrainingdata(right).
|     | Tokenizer-based | 3.7 | 29.4 41.0 | 46.3 | 45.2 48.1 |     |     |     |     |     |     |     |
| --- | --------------- | --- | --------- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
|     | Byte-level      | 1.0 | 25.9 33.6 | 41.8 | 41.3 42.1 |     |     |     |     |     |     |     |
MBPP-Plus
|     | Proxy(Neural)    | 2.6 | 22.0 29.6 | 41.8 | 41.8 49.2 |     |     |     |     |     |     |     |
| --- | ---------------- | --- | --------- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- |
|     | Proxy(Tokenizer) | 2.9 | 25.4 38.4 | 44.4 | 45.5 49.5 |     |     |     |     |     |     |     |
competitively,withneuralcompressionachievingslightly
|     |     |     |     |     |     | lower | compression | (2.6×) | than | the | tokenizer-based | com- |
| --- | --- | --- | --- | --- | --- | ----- | ----------- | ------ | ---- | --- | --------------- | ---- |
etc.);thisyieldsacomparabletrainingFLOPsbudgetacross pressor(2.9×),yetstillmatchingitsperformanceatscale.
| representations. | Asaresult,modelsoperatingondifferent |     |     |     |     |     |     |     |     |     |     |     |
| ---------------- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
representationscanconsumedifferentamountsofrawdata
|           |                    |     |                |     |             | Data | versus | Compute |     | Efficiency. | Byte-level | and |
| --------- | ------------------ | --- | -------------- | --- | ----------- | ---- | ------ | ------- | --- | ----------- | ---------- | --- |
| per step. | We compare against |     | two baselines: |     | (i) a byte- |      |        |         |     |             |            |     |
levelmodeltrainedentirelyonrawUTF-8bytes, and(ii) tokenizer-basedmodelsexhibitawell-knowntrade-off(Xue
atokenizer-basedmodeltrainedonBPEtokensusingthe et al., 2022; Zheng et al., 2025b): tokenizer-based mod-
OpenCodertokenizer(Huangetal.,2024a). Forevaluation, elsaremorecompute-efficient(betterperformanceundera
weprimarilyfocusondownstreamcodegenerationtasks fixedFLOPsbudget,astheyconsumemoredataperunitof
compute),whilebytemodelsaremoredata-efficient(better
includingHumanEval(Chenetal.,2021),MBPP(Austin
etal.,2021),andtheirEvalPlusvariants(Liuetal.,2023). performanceunderthesameamountoftrainingdata,asthey
FullexperimentaldetailsareprovidedinAppendixC. allocate more optimization steps and thus more compute
|     |     |     |     |     |     | pertrainingexample).3 |     |     | Figure3showsthatproxycompres- |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | ----------------------------- | --- | --- | --- |
3.2.MainResults: ScalableDownstreamTransfer sionisabletocapturethebestofbothregimesforour14B
modelruns(seeFigures19to22forcomparisonsatdiffer-
| In this section, | we address | the | central | question: | can we |                  |     |                    |     |     |               |     |
| ---------------- | ---------- | --- | ------- | --------- | ------ | ---------------- | --- | ------------------ | --- | --- | ------------- | --- |
|                  |            |     |         |           |        | entmodelscales). |     | UndermatchedFLOPs, |     |     | proxy-trained |     |
trainprimarilyonproxy-compressedinputsyetdeploythe
modelsperformcomparablytotokenizerbaselines;while
model purely on raw bytes, without ever exposing com- undermatcheddata,theyretainthedataefficiencyofbyte-
| pressedformatsatinferencetime? |     |     | Concretely,weevaluate |     |     |     |     |     |     |     |     |     |
| ------------------------------ | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
leveltrainingwhilesubstantiallyoutperformingtokenizer
whethermixed-representationtrainingwithproxycompres- baselines. Theseresultssuggestproxycompressionlever-
sorsyieldseffectivetransfertorawbytestreamsondown-
agesdatamoreefficientlywhileapproachingthecompute
streamcodegenerationtasks.
efficiencyoftokenizedtraining.
| TransferScaleswithModelSizes. |     |     | AsshowninTable1, |     |     |     |     |     |     |     |     |     |
| ----------------------------- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
proxy-compressedinputsyieldstrongandscalabletransfer LongerTrainingHorizons. Totestwhetherthesetrends
ondownstreamtasks. Despiteobservingrawbytesononly hold at larger scale, we extend training to 320B symbols
10%oftrainingsamples,proxy-trainedbytemodelsclosely
(tokensorbytes)onthefullRefineCodeGitHubsplit,fol-
trackoroutperformthefullybyte-levelbaselineatallmodel lowingtheOpenCodersetup(Huangetal.,2024a). Table2
sizes. Thisindicatesthatcompressedviewseffectivelycom- confirms consistent patterns: at 1.5B parameters, proxy
pensateforthesignificantlyreducedraw-byteexposureby models outperform byte baselines but still trail tokenizer
consumingmoredataandthatcross-representationtransfer baselines; at 7B, they close the gap and often match or
isstrongenoughtorecovermostoftheperformanceoffully
|     |     |     |     |     |     | exceedtokenizer-basedmodels. |     |     |     | Thisshowsthatproxycom- |     |     |
| --- | --- | --- | --- | --- | --- | ---------------------------- | --- | --- | --- | ---------------------- | --- | --- |
byte-leveltraining. Moreover,theadvantageofproxytrain- pressionremainseffectiveunderlongertraininghorizons.
| ingbecomesmorepronouncedwithscale. |        |     |                    | Atlargermodel |         |          |       |         |      |                       |     |        |
| ---------------------------------- | ------ | --- | ------------------ | ------------- | ------- | -------- | ----- | ------- | ---- | --------------------- | --- | ------ |
|                                    |        |     |                    |               |         | Overall, | these | results | show | that proxy-compressed |     | train- |
| sizes, proxy-trained               | models | not | only significantly |               | outper- |          |       |         |      |                       |     |        |
ingenablesefficientlearningfromcompresseddata,while
formbyte-levelbaselines,butalsostarttoachieveorsurpass
achievingscalabledownstreamtransfertoraw-byteinfer-
| the performance | of tokenizer-based |     | models. |     | This can be |     |     |     |     |     |     |     |
| --------------- | ------------------ | --- | ------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
ence,withbenefitsthatamplifyatscale.
attributedtogreatertransfercapabilityoflargermodelsto
storethealignmentbetweencompressedandrawviewsin 3Thistrade-offdoesnotalwaysholdwhenvaryingthescale
weights. Bothneuralandtokenizer-basedproxiesperform
andtraininghorizon;pleaseseeAppendixD.7forfurtheranalysis.
5

ProxyCompressionforLanguageModeling
Table2.Downstreampass@1onHumanEval-PlusandMBPP-Plus Table3. Ordinarypass@1(%)at50ktrainingstepsandoracle-
aftertraining320BtokensonthefullRefineCodeGitHubdata. translationpass@1(%)at10k,20k,30k,40k,and50ktraining
stepsonHumanEval-Plusfordifferentcompressortypesandpair-
#Parameters Model HumanEval-Plus MBPP-Plus ingschedules(1.5Bmodel;higherisbetter). Wehighlightcells
withpassrateshigherthan90%.
|      | Tokenizer-based  |     |     | 17.1 |     | 28.0 |                |              |     |          |                         |           |           |
| ---- | ---------------- | --- | --- | ---- | --- | ---- | -------------- | ------------ | --- | -------- | ----------------------- | --------- | --------- |
|      | Byte-level       |     |     | 9.1  |     | 23.3 |                |              |     |          |                         |           |           |
| 1.5B |                  |     |     |      |     |      |                |              |     | Pass@1   | OracleTranslationPass@1 |           |           |
|      | Proxy(Neural)    |     |     | 14.0 |     | 24.1 | CompressorType | ModelVariant |     |          |                         |           |           |
|      |                  |     |     |      |     |      |                |              |     | 50ksteps | 10k                     | 20k 30k   | 40k 50k   |
|      | Proxy(Tokenizer) |     |     | 12.8 |     | 25.1 |                |              |     |          |                         |           |           |
|      |                  |     |     |      |     |      |                | Nopairs      |     | 17.0     | 7.30                    | 29.3 40.2 | 44.5 45.7 |
|      | Tokenizer-based  |     |     | 21.3 |     | 36.0 |                |              |     |          |                         |           |           |
|      |                  |     |     |      |     |      | Tokenizer      | Warmup-only  |     | 20.7     | 90.9                    | 31.1 42.1 | 53.7 45.7 |
|      | Byte-level       |     |     | 14.6 |     | 32.5 |                | Always-on    |     | 17.0     | 93.3                    | 95.7 96.3 | 96.3 96.3 |
7B
|     | Proxy(Neural) |     |     | 21.3 |     | 36.0 |     | Nopairs |     | 14.6 | 0.6 | 3.0 7.9 | 20.7 32.9 |
| --- | ------------- | --- | --- | ---- | --- | ---- | --- | ------- | --- | ---- | --- | ------- | --------- |
Proxy(Tokenizer) 22.0 34.9 Neural Warmup-only 18.9 90.9 39.0 14.6 22.0 38.4
|     |     |     |     |     |     |     |     | Always-on |     | 14.6 | 94.5 | 92.1 93.9 | 95.1 95.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | ---- | ---- | --------- | --------- |
3.3.In-contextCross-RepresentationTransfer
Theresultsin§3.2demonstratein-weighttransfer: knowl- Proxy compressor
6
Gzip
edgelearnedfromcompressedinputstransferstoraw-byte
|                                     |     |     |     |     |       |         | 5   |     |     |     |     | Tokenizer |     |
| ----------------------------------- | --- | --- | --- | --- | ----- | ------- | --- | --- | --- | --- | --- | --------- | --- |
| inferencethroughthemodelparameters. |     |     |     |     | Here, | weprobe |     |     |     |     |     |           |     |
Neural
4
| amoreexplicitformoftransfercalledin-contexttransla- |      |            |     |           |     |          | ytisneD |     |     |     |     |     |     |
| --------------------------------------------------- | ---- | ---------- | --- | --------- | --- | -------- | ------- | --- | --- | --- | --- | --- | --- |
| tion, where                                         | both | compressed | and | raw views | of  | the same | 3       |     |     |     |     |     |     |
inputappearinasinglecontext,andthemodelmusttrans-
2
| latebetweenrepresentationsonthefly. |     |       |                    | Foreachproblem |             |           |     |         |     |     |     |     |     |
| ----------------------------------- | --- | ----- | ------------------ | -------------- | ----------- | --------- | --- | ------- | --- | --- | --- | --- | --- |
| on HumanEval-Plus                   |     | (Chen | et al.,            | 2021;          | Liu et al., | 2023),    | 1   |         |     |     |     |     |     |
| wetaketherawpromptp                 |     |       | andoraclesolutions |                |             | raw ,com- | 0   |         |     |     |     |     |     |
|                                     |     |       | raw                |                |             |           | 0.0 | 0.2 0.4 | 0.6 | 0.8 | 1.0 | 1.2 | 1.4 |
press them into p and s , and construct a mixed- Normalized Levenshtein Distance
|     |     | comp | comp |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
representationprompt
Figure4.Compressorstabilityanalysisunderinputperturbation:
(cid:2) (cid:3) we apply random 10% character deletion to 80K samples and
| ⟨comp⟩◦p |     | ◦s  | ◦⟨/comp⟩◦⟨raw⟩◦p |     |     | .   |     |     |     |     |     |     |     |
| -------- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
comp comp raw measurenormalizedLevenshteindistancebetweencompressed
outputsbeforeandafterperturbation.
Themodelmustdecodethecorrespondingrawsolutions
raw
inrawbytes.Wereportoracle-translationpass@1:whether
themodelrecoversthecorrectsolutiongivenitscompressed
| formincontext. |     | Tostudyhowin-contexttransferdepends |     |     |     |     |     |     |     |     |     |     |     |
| -------------- | --- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
forWarmup-only,likelyduetobettereffectivecompression
onexplicitpairingasdescribedin§2.1,wecomparethree
whensamplesarenotduplicatedaspairs(AppendixA).This
| trainingschedules(allwithmixingratior=0.9): |     |     |     |     |     | Nopairs |     |     |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
suggeststransferoperatesatadeepersemanticlevelbeyond
(independentsamplingwithoutanypaireddata),Warmup-
|     |     |     |     |     |     |     | literalsequence-to-sequencetranslation: |     |     |     |     | themodelcanstill |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | ---------------- | --- |
only(enablingtranslationpairsforfirst10ktrainingsteps extractandleveragesharedstructureacrossrepresentations
| only), and | Always-on | (pairs | throughout |     | training). | More |     |     |     |     |     |     |     |
| ---------- | --------- | ------ | ---------- | --- | ---------- | ---- | --- | --- | --- | --- | --- | --- | --- |
in-weightevenwithoutmasteringperfectin-contexttransla-
detailsareinAppendixD.2.
|         |         |               |        |            |     |         | tion. ExtendedanalysesareprovidedinAppendixD.2. |     |     |     |     |     |     |
| ------- | ------- | ------------- | ------ | ---------- | --- | ------- | ----------------------------------------------- | --- | --- | --- | --- | --- | --- |
| Table 3 | reports | both ordinary | (i.e., | no-oracle) | and | oracle- |                                                 |     |     |     |     |     |     |
translationpass@1. Mixed-representationtraininginduces 3.4.WhatMakesaGoodProxyCompressor?
substantialin-contexttransferevenwithoutexplicitpairs:
|     |     |     |     |     |     |     | The results | above | show | that tokenizer-based |     |     | and neural |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ----- | ---- | -------------------- | --- | --- | ---------- |
underNopairs,oracle-translationpass@1reaches∼46%
|     |     |     |     |     |     |     | proxies | enable strong | transfer, | while | preliminary |     | experi- |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------- | --------- | ----- | ----------- | --- | ------- |
(tokenizer)and∼33%(neural),wellaboveno-oraclebase-
|             |           |     |          |                  |     |         | mentswithgzipcompressionfailedentirely. |     |     |     |     | Whatdistin- |     |
| ----------- | --------- | --- | -------- | ---------------- | --- | ------- | --------------------------------------- | --- | --- | --- | --- | ----------- | --- |
| lines. With | Always-on |     | pairing, | both compressors |     | rapidly |                                         |     |     |     |     |             |     |
guisheseffectiveproxycompressorsfromineffectiveones?
achievenear-perfecttranslation(>95%pass@1),demon-
Wehypothesizethatsuccessfulproxiesproducestructured
| strating | that even     | ambiguous | neural      | compression |              | can be |                             |         |        |                        |            |         |     |
| -------- | ------------- | --------- | ----------- | ----------- | ------------ | ------ | --------------------------- | ------- | ------ | ---------------------- | ---------- | ------- | --- |
|          |               |           |             |             |              |        | compressions:               | similar | inputs | map                    | to similar | outputs | and |
| reliably | disambiguated |           | in context. | Under       | Warmup-only, |        |                             |         |        |                        |            |         |     |
|          |               |           |             |             |              |        | semanticcontentispreserved. |         |        | Wetestthishypothesisby |            |         |     |
No pairs
| translation | accuracy | decays | toward | the |     | baseline |           |            |            |     |          |        |     |
| ----------- | -------- | ------ | ------ | --- | --- | -------- | --------- | ---------- | ---------- | --- | -------- | ------ | --- |
|             |          |        |        |     |     |          | measuring | compressor | stability: |     | we apply | random | 10% |
oncepairingisremoved,yetstilloutperformingno-oracle
characterdeletionto80Ksamplesdrawnfromtrainingdata
baselines,indicatingretainedtransfercapability.
andcomputethenormalizedLevenshteindistancebetween
Interestingly, high translation accuracy is not necessary compressed outputs before and after transformation. As
for strong downstream performance (e.g., §3.2, which shown in Figure 4, tokenization is highly stable (similar
uses Warmup-only bydefault). ComparingWarmup-only inputsyieldsimilaroutputs),gzipissignificantlymoreun-
and Always-on, we observe a significant drop in oracle- stable(smalleditscauselargeoutputchanges),andneural
translationaccuracy,yetordinarypass@1isslightlybetter compressionliesinbetween.
6

ProxyCompressionforLanguageModeling
| 0.175 | Gzip:Raw = 0:100 |     |     |     |     |     |     |
| ----- | ---------------- | --- | --- | --- | --- | --- | --- |
)elacs gol( stnemges desserpmoC 105
| 1@ssaP sulP-lavEnamuH | Gzip:Raw = 50:50 |     |     |     |     |     |     |
| --------------------- | ---------------- | --- | --- | --- | --- | --- | --- |
| 0.150                 | Gzip:Raw = 75:25 |     |     |     |     |     |     |
|                       | Gzip:Raw = 90:10 |     |     | 104 |     |     |     |
0.125
103
0.100
102
0.075
101
0.050
| 0.025 |     |     |     | 100 |       |       |       |
| ----- | --- | --- | --- | --- | ----- | ----- | ----- |
|       |     |     |     | 0   | 10 20 | 30 40 | 50 60 |
Raw chunks per compressed segment
|     | 20 40 | 60 80 | 100 |     |     |     |     |
| --- | ----- | ----- | --- | --- | --- | --- | --- |
Training Bytes (B) Figure6. Collisionstatisticsfortheneuralcompressor. Thex-
Figure5. HumanEval-Pluspass@1of1.5Bgzip-proxymodels axis is the number of distinct byte chunks that collide on the
withdifferentmixingratiosrasafunctionoftrainingdata. samecompressedsegment,andthey-axisisthenumberofsuch
compressedsegmentsinlogscale.
| Gzip Proxies | Fail to Transfer. | Figure 5 shows | down- |     |     |     |     |
| ------------ | ----------------- | -------------- | ----- | --- | --- | --- | --- |
streamperformancefor1.5Bmodelstrainedwithvarying
| gzip-versus-rawratios. | Unliketokenizerandneuralproxies, |     |     |     |     |     |     |
| ---------------------- | -------------------------------- | --- | --- | --- | --- | --- | --- |
increasingtheproportionofgzipcompresseddatadegrades
performance: modelstrainedonpurerawbytes(0%gzip) 3.5.RobustnessEvaluation
alwaysoutperformgzip-mixedvariants.Thisindicatesweak
Byte-levelmodelshavebeenshowntobemorerobustto
orevennegativetransferfromgzip-compressedsequences
inputperturbationsthantokenizer-basedmodels(Pagnoni
| torawbytes. | Weattributethisfailuretothehighlyunstable |     |     |                              |     |                        |     |
| ----------- | ----------------------------------------- | --- | --- | ---------------------------- | --- | ---------------------- | --- |
|             |                                           |     |     | etal.,2024;Hwangetal.,2025). |     | Inthissection,weinves- |     |
andunstructuredoutputsfromgzip(Figure4),wheresmall
tigatewhetherproxy-trainedmodelsinheritthisadvantage.
inputperturbationscausedrasticchangesinthecompressed
WeevaluaterobustnessontheHumanEvalsplitofReCode
sequence,makingitdifficultforthemodeltolearnconsis-
|               |                                            |     |     | (Wang et      | al., 2023), which | applies semantics-preserving |          |
| ------------- | ------------------------------------------ | --- | --- | ------------- | ----------------- | ---------------------------- | -------- |
| tentpatterns. | Inaddition,gzipexploitslow-levelbyteredun- |     |     |               |                   |                              |          |
|               |                                            |     |     | perturbations | to coding         | problems four families:      | function |
danciespersamplewithoutrespectingsemantics,producing
|                                           |     |     |         | name rewrites | (Function), | formatting changes | (Format), |
| ----------------------------------------- | --- | --- | ------- | ------------- | ----------- | ------------------ | --------- |
| outputsthatresemblenoisetoalanguagemodel. |     |     | Empiri- |               |             |                    |           |
syntacticrewrites(Syntax),anddocstringparaphrases(Doc-
cally,weobservethatmodelstrainedongzip-compressed
strings). Wereportstandardpass@1onunperturbedinputs
datafailtocompletepartialgzipsequencescoherently,sug-
andRobustPass@1(RP),theworst-casepass@1across5
gestingtheyneverlearntheunderlyingcompressionscheme.
|     |     |     |     | perturbedvariantsperproblem. |     | Fullmetricdefinitionsand |     |
| --- | --- | --- | --- | ---------------------------- | --- | ------------------------ | --- |
per-familybreakdownsareinAppendixD.4.
Neural Compression: Structured Fuzziness. As dis- Table4reportsstandardpass@1andmacro-averagedrobust
cussed in §2.3, neural compression is non-invertible: a pass@1 (RP). Although lower no-perturbation pass@1,
single compressed sequence may correspond to multiple thebyte-levelmodelexhibitsmuchbetterrobustnessthan
raw byte chunks (collisions). Despite the ambiguity and tokenizerbaselines(RP: 18.7vs.14.9). Proxy-trainedmod-
unstable mapping (Figure 4), neural proxies still achieve elsinheritandamplifytheserobustnessadvantages: neural
strongtransfer. WeanalyzethisinFigure6,showingthat proxiesattainthehighestRP,whiletokenizerproxiessub-
mostcompressedsegmentsexhibitcollision. Toquantify stantially improve robustness over the tokenizer baseline.
similarityamongcollidingchunks,wecomputethelongest Oneplausibleexplanationisthatthefuzzyrepresentations
commonprefix(LCP)ratio:
thelengthofthesharedprefix induced by neural compression (§3.4) help smooth over
dividedbyaveragechunklength. Crucially,thesecollisions superficialnoise,encouragingthemodeltofocusoninvari-
arehighlystructured: over90%ofcollisionshaveLCPra- antstructureduringtraining. Figure7revealsthatFormat
tiosabove0.8,meaningmostcollidingchunksarenearly perturbations drive the largest gap: byte-level and proxy
identical except for short suffixes (Figure 12), likely due modelsremainnear-nominalunderwhitespaceandinden-
to the entropy for these suffixes being too small for the tation changes, whereas the tokenizer baseline degrades
arithmeticcodertoallocateadditionalbits. Thisstructured sharply.OnSyntax,allmodelssufferhighRD,thoughproxy
fuzzinessabstractsawayformattingnoisewhilepreserving modelsstillimproveRP.Overall,despitebeingtrainedpre-
semantics,potentiallyexplainingwhyneuralproxiesmatch dominantlyoncompressedinputs,ourproxy-compressed
tokenizer-basedproxiesdespitetheirambiguity. Pleasesee modelscanmostlyretainandinsomecasesimproveupon
AppendixD.3fordetailedanalysis. therobustnessofbyte-levelmodels.
7

ProxyCompressionforLanguageModeling
| 0.35             |     | Tokenizer-based   | 0.60             |     |     |      |     |     |     |     |     |
| ---------------- | --- | ----------------- | ---------------- | --- | --- | ---- | --- | --- | --- | --- | --- |
|                  |     | Byte-level        |                  |     |     | 0.18 |     |     |     |     |     |
| 0.30             |     |                   | 0.50             |     |     |      |     |     |     |     | 3.5 |
| )PR( ssaP tsuboR |     | Proxy (Tokenizer) | )DR( porD tsuboR |     |     |      |     |     |     |     |     |
0.25 Proxy (Neural) 0.40 1@ssap sulP-lavEnamuH )dezilamroN( tnuoC coD
| 0.20 |     |     | 0.30 |     |     | 0.16 |     |     |     |     | 3.0 |
| ---- | --- | --- | ---- | --- | --- | ---- | --- | --- | --- | --- | --- |
| 0.15 |     |     | 0.20 |     |     |      |     |     |     |     |     |
| 0.10 |     |     | 0.10 |     |     |      |     |     |     |     | 2.5 |
0.14
| 0.05     |                     |            | 0.00     |                     |                   |      |     |     |     |     |     |
| -------- | ------------------- | ---------- | -------- | ------------------- | ----------------- | ---- | --- | --- | --- | --- | --- |
| 0.00     |                     |            | -0.10    |                     |                   |      |     |     |     |     | 2.0 |
| Function | Format Syntax       | Docstrings | Function | Format              | Syntax Docstrings | 0.12 |     |     |     |     |     |
|          | Perturbation Family |            |          | Perturbation Family |                   |      |     |     |     |     |     |
Figure7.Robustpass(left,higherisbetter)androbustdrop(right, 1.5
lowerisbetter)performanceonReCodeperperturbationfamily 0.10 Inference on Bytes
| withdifferentmodels. |     |     |     |     |     |     | Inference on Tokens |     |     |     | 1.0 |
| -------------------- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | --- | --- |
Doc Count (Normalized)
0.08
| Table4.RobustnessevaluationontheHumanEvalsplitofReCode |     |     |     |     |     |     |     |     |     |     | 0.5 |
| ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
with7Bmodels.Wereportstandardpass@1androbustpass@1 0.0 0.2 0.4 0.6 0.8 1.0
Proportion of Raw Bytes
(RP),themacroaverageacrossperturbationfamilies.
Figure9.PerformanceonHumanEval-PlusPass@1asafunction
Model Pass@1 RobustPass@1(RP)↑ ofrawbyteproportioninthetrainingmixturefor1.5Bmodelswith
|     |     |     |     |     |     | tokenproxycompression. |     | Solidanddashedlinesshowmodels |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------------------- | --- | ----------------------------- | --- | --- | --- |
Tokenizer-based 32.9 14.9 performingbyte-levelandtoken-levelinference,respectively.The
Byte-level 26.2 18.7 dash-dot line (right y-axis) indicates the normalized document
Proxy(Tokenizer) 32.9 19.1 countseenduringtrainingwithinafixedtrainingFLOPsbudget.
| Proxy(Neural) |     | 30.5 |     | 19.8 |     |                |                                        |     |     |     |     |
| ------------- | --- | ---- | --- | ---- | --- | -------------- | -------------------------------------- | --- | --- | --- | --- |
|               |     |      |     |      |     | trainingsteps. | Figure9revealsthatmodelswithbyte-level |     |     |     |     |
3.6.Analyses inferencedonotdegradeperformancemonotonicallywith
|                |     |            |     |                 |       | mixture ratios:                   | it performs | strongly |     | with 10%         | raw bytes, |
| -------------- | --- | ---------- | --- | --------------- | ----- | --------------------------------- | ----------- | -------- | --- | ---------------- | ---------- |
| Inference-Time |     | Interface. | For | tokenizer-based | proxy |                                   |             |          |     |                  |            |
|                |     |            |     |                 |       | besidesattheextremeof100%rawdata. |             |          |     | Thispatternisex- |            |
compression,wecanperforminferenceoneitherrawbytes plainedbythedocumentcountcurve(dash-dotline),which
or compressed tokens. Surprisingly, byte-level inference showsthatreducingrawbyteproportioninthemixincreases
| often matches | or  | exceeds | token-level | inference, | despite |     |     |     |     |     |     |
| ------------- | --- | ------- | ----------- | ---------- | ------- | --- | --- | --- | --- | --- | --- |
thenumberofuniquetrainingsamplesseenwithinafixed
90%oftrainingdatabeingincompressedform,asshown computebudget. Atr=0.9,modelsobserveapproximately
| in Figure | 8. We | attribute | this to | two factors: | (i) cross- |                 |      |          |       |     |             |
| --------- | ----- | --------- | ------- | ------------ | ---------- | --------------- | ---- | -------- | ----- | --- | ----------- |
|           |       |           |         |              |            | 3× more samples | than | at r=0.0 | (100% | raw | bytes), and |
representationtransferissufficientlystrongthatthemodel
strongcompressed-to-rawtransferallowsthemtobenefit
performswellonrawbytesevenwithlimitedexposure,and from this additional data. The mixing ratio ablation also
| (ii) longer | byte sequences |     | afford more | test-time | compute |     |     |     |     |     |     |
| ----------- | -------------- | --- | ----------- | --------- | ------- | --- | --- | --- | --- | --- | --- |
revealsanasymmetryintransferdirection.Forbyte-levelin-
per problem instance. Note that for neural compression, ference(solidlineinFigure9),performanceremainsstrong
token-levelinferenceisintractable,andthusitonlyadmits
evenwithonly10%rawdata,indicatingrobusttransferfrom
inferenceonrawbytes(§2.3).
|     |     |     |     |     |     | compressedtorawrepresentations. |     |     | Incontrast,fortoken- |     |     |
| --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | -------------------- | --- | --- |
levelinference(dashedline),performancedegradesnearly
| Compression-rawMixingRatioAblation. |     |     |     |     | Throughout |     |     |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
monotonicallyasrawbyteproportionincreases,suggesting
our experiments, we maintain a fixed ratio r = 0.9 to be weaktransferfromrawbacktocompressedrepresentations.
theproportionofcompressedsamplesinthetrainingcorpus.
Tostudytheeffectofraw-compresseddatacompositionin
4.RelatedWork
proxycompressiontraining,wetrain1.5Bparametermod-
elsonmixturescontainingvaryingproportionsofrawand
|     |     |     |     |     |     | Input Representations |     | for | Language | Models. | Most |
| --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | -------- | ------- | ---- |
compresseddata,maintainingaconstantbudgetof50000 modernlanguagemodelsrelyonexternaltokenizationthat
segmentstextualdataintosequencesofdiscretetokens,such
asByte-PairEncoding(Gage,1994;Sennrichetal.,2016),
0.50
| 0.30                  |     |     |      |     |     | WordPiece(Schuster&Nakajima,2012;Wuetal.,2016; |     |     |     |     |     |
| --------------------- | --- | --- | ---- | --- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- |
| 1@ssaP sulP-lavEnamuH |     |     | 0.45 |     |     |                                                |     |     |     |     |     |
1@ssaP sulP-PPBM
| 0.25 |     |     | 0.40 |     |     | Devlinetal.,2019),UnigramLM(Kudo,2018),andSenten- |     |     |     |     |      |
| ---- | --- | --- | ---- | --- | --- | ------------------------------------------------- | --- | --- | --- | --- | ---- |
|      |     |     |      |     |     | cePieceimplementations(Kudo&Richardson,2018).     |     |     |     |     | Tok- |
| 0.20 |     |     | 0.35 |     |     |                                                   |     |     |     |     |      |
enizationcompressesrawtextintoshortertokensequences,
0.30
|     | Byte-level |     |     | Byte-level |     |     |     |     |     |     |     |
| --- | ---------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
0.15 Proxy (Tokenizer): Inference on Bytes 0.25 Proxy (Tokenizer): Inference on Bytes andrecentworkhaspushedthisdesignalongmultipleaxes,
|     | Proxy (Tokenizer): Inference on Tokens |     |     | Proxy (Tokenizer): Inference on Tokens |     |     |     |     |     |     |     |
| --- | -------------------------------------- | --- | --- | -------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
Tokenizer-based 0.20 Tokenizer-based includinganalyzingtheoveralltokenizationpipelinedesign
0.10
| 2   | 4 6 | 8   | 2   | 4   | 6 8 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Total Training FLOPs 1e21 Total Training FLOPs 1e21 (Bostrom & Durrett, 2020; Zouhar et al., 2023; Schmidt
Figure8.Inference-timeinterfacecomparisononHumanEval-Plus etal.,2024;Daganetal.,2024),studyingnon-canonicalto-
(left)andMBPP-Plus(right)for14Btoken-proxymodels. kenizationbehavior(Cao&Rimell,2021;Gehetal.,2024;
8

ProxyCompressionforLanguageModeling
2025; Zheng et al., 2025a), exploring vocabulary scaling resentations and transfer effectively from compressed in-
(Taoetal.,2024;Yuetal.,2025;Huangetal.,2025),and putstoraw-byteinference. Extensiveexperimentsoncode
improvingcompression(Friedetal.,2023;Geeetal.,2023; languagemodelingdemonstratethatproxy-trainedmodels
Schmidtetal.,2025;Liuetal.,2025). substantially outperform pure byte-level baselines under
fixedcomputebudgets,andatscalematchorrivaltokenizer-
Besidestokenization,recentworkalsoexploresdistinctap-
|     |     |     |     |     |     |     | basedmodels,allwhileoperatingsolelyonrawbytes. |     |     |     |     |     | Our |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- | --- |
proachestoconstructingcompressedrepresentations,such
systematicstudyofproxycompressorsfurtherrevealsthat
asgzip-basedcompressors(Jiangetal.,2023;Lesteretal.,
tokenizer-basedandneuralproxiessupportstrongtransfer,
2024),arithmeticcodingwithequal-informationwindows
|     |     |     |     |     |     |     | whereas | generic compression |     | (gzip) | fails to | provide | use- |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------------- | --- | ------ | -------- | ------- | ---- |
(Lesteretal.,2024),concept-levelsemanticunits(Barrault
fultrainingsignal,suggestingthatstructured,semantically
etal.,2024;Quetal.,2025),morphology-drivenbyterepre-
meaningfulcompressioniskeytoeffectiveproxytraining.
sentations(Limisiewiczetal.,2024)thatimproveefficiency
andfairnessinmultilingualsettings,andpixel-renderedtext
|     |     |     |     |     |     |     | Limitations. | Ourstudyfocusesoncodelanguagemodel- |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ----------------------------------- | --- | --- | --- | --- | --- |
(Saleskyetal.,2021;Rustetal.,2023;Saleskyetal.,2023;
|     |     |     |     |     |     |     | ing; whether | proxy | compression | generalizes |     | to other | do- |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ----- | ----------- | ----------- | --- | -------- | --- |
Lietal.,2023;Leeetal.,2023;Lotzetal.,2023;Taietal.,
|     |     |     |     |     |     |     | mains remains | to  | be validated. | The | trade-offs | between |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ------------- | --- | ---------- | ------- | --- |
2024;Gaoetal.,2024;Weietal.,2025;Chengetal.,2025).
compressionrate,transferstrength,andcomputeefficiency
arenotyetfullycharacterized(e.g.,moreaggressivecom-
| Byte-level | Models. | Alternatively, |     | one | can | directly use |          |             |            |       |           |         |     |
| ---------- | ------- | -------------- | --- | --- | --- | ------------ | -------- | ----------- | ---------- | ----- | --------- | ------- | --- |
|            |         |                |     |     |     |              | pression | may amplify | efficiency | gains | but could | degrade |     |
byte-levelsequencesastheinputrepresentation(Sutskever transferquality). Finally,incorporatingproxycompression
| et al., 2011; | Graves, | 2013; | Radford | et  | al., 2017; | Chung |     |     |     |     |     |     |     |
| ------------- | ------- | ----- | ------- | --- | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- |
directlyintomodelarchitecturedesign,ratherthantreating
| et al., 2017; | Hwang | &   | Sung, 2017; | Al-Rfou |     | et al., 2019; |     |     |     |     |     |     |     |
| ------------- | ----- | --- | ----------- | ------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
itpurelyasadatapreprocessingstep,mayunlockfurther
Choe et al., 2019; Xue et al., 2022; Wang et al., 2024b; performanceorefficiencyimprovements.
| Neitemeier   | et al.,                                | 2025; | Zheng | et al., | 2025b; | Minixhofer |     |     |     |     |     |     |     |
| ------------ | -------------------------------------- | ----- | ----- | ------- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- |
| etal.,2025). | Tomitigatethecomputationalcostoflonger |       |       |         |        |            |     |     |     |     |     |     |     |
ImpactStatement
sequences,recentworkaimstopoolinputsequencesinto
| shorter representations |     |     | inside the | model | architecture, | in- |     |     |     |     |     |     |     |
| ----------------------- | --- | --- | ---------- | ----- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Thispaperpresentsworkwhosegoalistoadvancethefield
cludingdownsamplingtheinputinacontext-independent of Machine Learning. There are many potential societal
manner(Jaegleetal.,2021b;a;Hawthorneetal.,2022;Clark
|     |     |     |     |     |     |     | consequences | of our | work, | none which | we  | feel must | be  |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ------ | ----- | ---------- | --- | --------- | --- |
etal.,2022;Nawrotetal.,2022;Yuetal.,2023;Pagnoni
specificallyhighlightedhere.
| etal.,2024;Slagle,2024;Videauetal.,2025). |          |             |     |      |             | Recentwork |     |     |     |     |     |     |     |
| ----------------------------------------- | -------- | ----------- | --- | ---- | ----------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
| also explores                             | adaptive | compression |     | with | dynamically | ad-        |     |     |     |     |     |     |     |
References
| justed granularity |     | based | on the | input | content | (Tay et al., |     |     |     |     |     |     |     |
| ------------------ | --- | ----- | ------ | ----- | ------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
2022;Godeyetal.,2022;Nawrotetal.,2023;Kallinietal., Ahia, O., Kumar, S., Gonen, H., Kasai, J., Mortensen,
2024;Ahiaetal.,2024;Owodunnietal.,2025;Gengetal.,
|     |     |     |     |     |     |     | D., Smith, | N., and | Tsvetkov, | Y. Do | all languages |     | cost |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------- | --------- | ----- | ------------- | --- | ---- |
2025; Hwang et al., 2025; Minixhofer et al., 2025). Be- the same? tokenization in the era of commercial lan-
| yondtext-onlylanguagemodeling, |     |     |     | byte-levelmodelsare |     |     |              |                                  |     |     |     |     |     |
| ------------------------------ | --- | --- | --- | ------------------- | --- | --- | ------------ | -------------------------------- | --- | --- | --- | --- | --- |
|                                |     |     |     |                     |     |     | guagemodels. | InProceedingsofthe2023Conference |     |     |     |     |     |
alsousedformulti-modallearning(Eglietal.,2025;Zheng onEmpiricalMethodsinNaturalLanguageProcessing,
et al., 2025b). More generally, byte-level models can be 2023. URLhttps://aclanthology.org/2023.
usedtoprocessvarioustypesofdigitalfilecontents(Park&
emnlp-main.614/.
Johnson,2023;Wuetal.,2024;Pe´rezetal.,2024;Hanetal.,
2024;Hortonetal.,2024;Jolicoeur-Martineau&Gervais, Ahia,O.,Kumar,S.,Gonen,H.,Hoffman,V.,Limisiewicz,
|     |     |     |     |     |     |     | T., Tsvetkov, | Y., | and Smith, | N. A. | Magnet: | Improv- |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ---------- | ----- | ------- | ------- | --- |
2025;Li&Chen,2025;Alcazaretal.,2025).
|     |     |     |     |     |     |     | ing the | multilingual | fairness | of language |     | models | with |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------ | -------- | ----------- | --- | ------ | ---- |
Ourworkdiffersfrompriorapproachesbyleveragingcom-
|         |                 |     |            |        |          |       | adaptive | gradient-based |     | tokenization. | arXiv | preprint |     |
| ------- | --------------- | --- | ---------- | ------ | -------- | ----- | -------- | -------------- | --- | ------------- | ----- | -------- | --- |
| pressed | representations |     | as a proxy | during | training | while |          |                |     |               |       |          |     |
arXiv:2407.08818,2024.
| still retaining | a byte-level |     | interface | at  | inference, | without |     |     |     |     |     |     |     |
| --------------- | ------------ | --- | --------- | --- | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- |
architecturalmodifications.
Al-Rfou,R.,Choe,D.,Constant,N.,Guo,M.,andJones,
L. Character-levellanguagemodelingwithdeeperself-
5.Conclusion attention. In Proceedings of the AAAI conference on
artificialintelligence,2019.
Weintroducedproxycompression,amixed-representation
training scheme that decouples the efficiency benefits of Alcazar,J.C.L.,Soldan,M.,Saatialsoruji,M.,Pardo,A.,
compressedtrainingfromtheinference-timeinterface. By Itani, H., Perez, J. C., and Ghanem, B. Transform-
jointly training on raw inputs and compressed views pro- ers from compressed representations. arXiv preprint
ducedbyexternalcompressors,modelslearntoalignrep- arXiv:2510.23665,2025.
9

ProxyCompressionforLanguageModeling
Athiwaratkun, B., Wang, S., Shang, M., Tian, Y., Wang, Clark,J.H.,Garrette,D.,Turc,I.,andWieting,J. Canine:
Z., Gonugondla, S. K., Gouda, S. K., Kwiatowski, R., Pre-training an efficient tokenization-free encoder for
Nallapati,R.,andXiang,B. Tokenalignmentviachar- languagerepresentation. TransactionsoftheAssociation
actermatchingforsubwordcompletion. arXivpreprint forComputationalLinguistics,2022. URLhttps://
| arXiv:2403.08688,2024. |     |     |     |     | aclanthology.org/2022.tacl-1.5. |     |     |     |     |     |     |     |
| ---------------------- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | --- | --- | --- |
Austin,J.,Odena,A.,Nye,M.,Bosma,M.,Michalewski, Dagan, G., Synnaeve, G., and Roziere, B. Getting the
H.,Dohan,D.,Jiang,E.,Cai,C.,Terry,M.,Le,Q.,etal.
mostoutofyourtokenizerforpre-traininganddomain
Program synthesis with large language models. arXiv adaptation. arXivpreprintarXiv:2402.01035,2024.
preprintarXiv:2108.07732,2021.
|     |     |     |     |     | Deletang, | G., Ruoss, | A., | Duquenne, | P.-A., |     | Catt, E., | Ge- |
| --- | --- | --- | --- | --- | --------- | ---------- | --- | --------- | ------ | --- | --------- | --- |
Barrault,L.,Duquenne,P.-A.,Elbayad,M.,Kozhevnikov,
newein,T.,Mattern,C.,Grau-Moya,J.,Wenliang,L.K.,
A.,Alastruey,B.,Andrews,P.,Coria,M.,Couairon,G.,
|     |     |     |     |     | Aitchison, | M., | Orseau, | L., Hutter, |     | M., and | Veness, | J.  |
| --- | --- | --- | --- | --- | ---------- | --- | ------- | ----------- | --- | ------- | ------- | --- |
Costa-jussa`,M.R.,Dale,D.,etal. Largeconceptmodels: The Twelfth
|     |     |     |     |     | Language | modeling | is  | compression. |     | In  |     |     |
| --- | --- | --- | --- | --- | -------- | -------- | --- | ------------ | --- | --- | --- | --- |
Languagemodelinginasentencerepresentationspace.
InternationalConferenceonLearningRepresentations,
arXivpreprintarXiv:2412.08821,2024.
2024. URLhttps://openreview.net/forum?
Bengio, Y., Ducharme, R., Vincent, P., and Jauvin, C. A id=jznbgiynus.
| neuralprobabilisticlanguagemodel. |     |     | Journalofmachine |     |     |     |     |     |     |     |     |     |
| --------------------------------- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Devlin,J.,Chang,M.-W.,Lee,K.,andToutanova,K.BERT:
learningresearch,2003.
|     |     |     |     |     | Pre-training | of  | deep bidirectional |     | transformers |     | for | lan- |
| --- | --- | --- | --- | --- | ------------ | --- | ------------------ | --- | ------------ | --- | --- | ---- |
Bostrom, K. and Durrett, G. Byte pair encoding is sub- guageunderstanding. InProceedingsofthe2019Confer-
optimalforlanguagemodelpretraining. InFindingsof enceoftheNorthAmericanChapteroftheAssociationfor
theAssociationforComputationalLinguistics: EMNLP ComputationalLinguistics: HumanLanguageTechnolo-
2020,2020. URLhttps://aclanthology.org/ gies,Volume1(LongandShortPapers),pp.4171–4186,
2020.findings-emnlp.414/. Minneapolis, Minnesota, June 2019. Association for
|              |               |                |        |           | ComputationalLinguistics. |     |     | doi: | 10.18653/v1/N19-1423. |     |     |     |
| ------------ | ------------- | -------------- | ------ | --------- | ------------------------- | --- | --- | ---- | --------------------- | --- | --- | --- |
| Cai, T., Li, | Y., Geng, Z., | Peng, H., Lee, | J. D., | Chen, D., |                           |     |     |      |                       |     |     |     |
URLhttps://aclanthology.org/N19-1423.
| andDao, | T. Medusa: | SimpleLLMinferenceaccelera- |     |     |     |     |     |     |     |     |     |     |
| ------- | ---------- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tionframeworkwithmultipledecodingheads. InForty- Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle,
first International Conference on Machine Learning, A.,Letman,A.,Mathur,A.,Schelten,A.,Yang,A.,Fan,
2024. URLhttps://openreview.net/forum?
|                |                   |             |            |         | A., et al.             | The llama | 3 herd       | of        | models.      | arXiv      | preprint   |      |
| -------------- | ----------------- | ----------- | ---------- | ------- | ---------------------- | --------- | ------------ | --------- | ------------ | ---------- | ---------- | ---- |
| id=PEpbUobfJv. |                   |             |            |         | arXiv:2407.21783,2024. |           |              |           |              |            |            |      |
| Cao, K. and    | Rimell, L.        | You should  | evaluate   | your    |                        |           |              |           |              |            |            |      |
|                |                   |             |            |         | Egli, E.,              | Manica,   | M., and      | Born,     | J.           | Multiscale |            | byte |
| language       | model on marginal | likelihood  | over       | tokeni- |                        |           |              |           |              |            |            |      |
|                |                   |             |            |         | language               | models–a  | hierarchical |           | architecture |            | for causal |      |
| sations.       | In Proceedings    | of the 2021 | Conference | on      |                        |           |              |           |              |            |            |      |
|                |                   |             |            |         | million-length         |           | sequence     | modeling. |              | arXiv      | preprint   |      |
Empirical Methods in Natural Language Processing, arXiv:2502.14553,2025.
2021. URLhttps://aclanthology.org/2021.
emnlp-main.161/.
|     |     |     |     |     | Fried, D., | Aghajanyan, | A., | Lin, | J., Wang,        |     | S., Wallace, |     |
| --- | --- | --- | --- | --- | ---------- | ----------- | --- | ---- | ---------------- | --- | ------------ | --- |
|     |     |     |     |     | E., Shi,   | F., Zhong,  | R., | Yih, | S., Zettlemoyer, |     | L.,          | and |
Chen,M.,Tworek,J.,Jun,H.,Yuan,Q.,Pinto,H.P.d.O.,
|     |     |     |     |     | Lewis,M. | Incoder: | Agenerativemodelforcodeinfilling |     |     |     |     |     |
| --- | --- | --- | --- | --- | -------- | -------- | -------------------------------- | --- | --- | --- | --- | --- |
Kaplan,J.,Edwards,H.,Burda,Y.,Joseph,N.,Brockman,
|           |                                        |     |     |     | and synthesis.                      |     | In The | Eleventh | International |           | Confer- |     |
| --------- | -------------------------------------- | --- | --- | --- | ----------------------------------- | --- | ------ | -------- | ------------- | --------- | ------- | --- |
| G., etal. | Evaluatinglargelanguagemodelstrainedon |     |     |     |                                     |     |        |          |               |           |         |     |
|           |                                        |     |     |     | enceonLearningRepresentations,2023. |     |        |          |               | URLhttps: |         |     |
code. arXivpreprintarXiv:2107.03374,2021.
//openreview.net/forum?id=hQwb-lbM6EL.
Cheng,J.,Liu,Y.,Zhang,X.,Fei,Y.,Hong,W.,Lyu,R.,
Wang, W., Su, Z., Gu, X., Liu, X., et al. Glyph: Scal- Fujii, K., Tajima, Y., Mizuki, S., Shimada, H., Shiotani,
|                                             |     |     |     |       | T., Saito, | K., Ohi, | M.,           | Kawamura, |              | M., Nakamura, |             | T., |
| ------------------------------------------- | --- | --- | --- | ----- | ---------- | -------- | ------------- | --------- | ------------ | ------------- | ----------- | --- |
| ingcontextwindowsviavisual-textcompression. |     |     |     | arXiv |            |          |               |           |              |               |             |     |
|                                             |     |     |     |       | Okamoto,   | T., et   | al. Rewriting |           | pre-training |               | data boosts |     |
preprintarXiv:2510.17800,2025.
|     |     |     |     |     | llm performance |     | in math | and | code. | arXiv | preprint |     |
| --- | --- | --- | --- | --- | --------------- | --- | ------- | --- | ----- | ----- | -------- | --- |
Choe, D., Al-Rfou, R., Guo, M., Lee, H., and Constant, arXiv:2505.02881,2025.
N. Bridgingthegapfortokenizer-freelanguagemodels.
|     |     |     |     |     | Gage,P. Anewalgorithmfordatacompression. |     |     |     |     |     | CUsers |     |
| --- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- | ------ | --- |
arXivpreprintarXiv:1908.10322,2019.
Journal,1994.
| Chung,J.,Ahn,S.,andBengio,Y. |     | Hierarchicalmultiscale |     |     |     |     |     |     |     |     |     |     |
| ---------------------------- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
recurrentneuralnetworks. InInternationalConference Gao,T.,Wang,Z.,Bhaskar,A.,andChen,D. Improving
on Learning Representations, 2017. URL https:// languageunderstandingfromscreenshots. arXivpreprint
| openreview.net/forum?id=S1di0sfgl. |     |     |     |     | arXiv:2402.14073,2024. |     |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- |
10

ProxyCompressionforLanguageModeling
Gee,L.,Rigutini,L.,Ernandes,M.,andZugarini,A. Multi- 2022.URLhttps://proceedings.mlr.press/
word tokenization for sequence compression. In Pro- v162/hawthorne22a.html.
| ceedings | of the  | 2023 Conference |             | on  | Empirical | Meth-  |                                              |     |     |     |     |     |     |      |
| -------- | ------- | --------------- | ----------- | --- | --------- | ------ | -------------------------------------------- | --- | --- | --- | --- | --- | --- | ---- |
|          |         |                 |             |     |           |        | Hayase,J.,Liu,A.,Choi,Y.,Oh,S.,andSmith,N.A. |     |     |     |     |     |     | Data |
| ods in   | Natural | Language        | Processing: |     | Industry  | Track, |                                              |     |     |     |     |     |     |      |
2023. URLhttps://aclanthology.org/2023. mixtureinference: Whatdobpetokenizersrevealabout
|     |     |     |     |     |     |     | their | training | data? | arXiv preprint |     | arXiv:2407.16607, |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | -------- | ----- | -------------- | --- | ----------------- | --- | --- |
emnlp-industry.58/.
2024.
| Geh, R.,    | Zhang, | H., Ahmed, | K.,    | Wang,  | B.,             | and Van |                                      |     |     |     |     |              |     |     |
| ----------- | ------ | ---------- | ------ | ------ | --------------- | ------- | ------------------------------------ | --- | --- | --- | --- | ------------ | --- | --- |
|             |        |            |        |        |                 |         | Hayase,J.,Liu,A.,Smith,N.A.,andOh,S. |     |     |     |     | Samplingfrom |     |     |
| Den Broeck, | G.     | Where      | is the | signal | in tokenization |         |                                      |     |     |     |     |              |     |     |
space? In Proceedings of the 2024 Conference on yourlanguagemodelonebyteatatime. arXivpreprint
arXiv:2506.14123,2025.
| Empirical | Methods | in Natural |     | Language | Processing, |     |     |     |     |     |     |     |     |     |
| --------- | ------- | ---------- | --- | -------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2024. URLhttps://aclanthology.org/2024.
Hoffmann,J.,Borgeaud,S.,Mensch,A.,Buchatskaya,E.,
emnlp-main.230/.
Cai,T.,Rutherford,E.,Casas,D.d.L.,Hendricks,L.A.,
Geh,R.,Shao,Z.,andVanDenBroeck,G. Adversarialtok- Welbl, J., Clark, A., et al. Training compute-optimal
|                                                    |                                       |     |     |     |     |     | largelanguagemodels. |     |     | arXivpreprintarXiv:2203.15556, |     |     |     |     |
| -------------------------------------------------- | ------------------------------------- | --- | --- | --- | --- | --- | -------------------- | --- | --- | ------------------------------ | --- | --- | --- | --- |
| enization.                                         | InProceedingsofthe63rdAnnualMeetingof |     |     |     |     |     |                      |     |     |                                |     |     |     |     |
| theAssociationforComputationalLinguistics(Volume1: |                                       |     |     |     |     |     | 2022.                |     |     |                                |     |     |     |     |
LongPapers),2025.URLhttps://aclanthology.
|     |     |     |     |     |     |     | Holtzman, | A., | Buys, | J., Du, | L., Forbes, | M., | and | Choi, |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ----- | ------- | ----------- | --- | --- | ----- |
org/2025.acl-long.1012/.
|     |     |     |     |     |     |     | Y. The | curious | case | of neural | text | degeneration. |     | In  |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------- | ---- | --------- | ---- | ------------- | --- | --- |
InternationalConferenceonLearningRepresentations,
Geng,S.,Ranchin,N.,Yao,Y.,Peyrard,M.,Wendler,C.,
Gastpar,M.,andWest,R. zip2zip: Inference-timeadap- 2020. URLhttps://openreview.net/forum?
id=rygGQyrFvH.
| tivetokenizationviaonlinecompression. |                   |                        |     |        | InTheThirty- |      |         |            |     |                    |     |     |            |     |
| ------------------------------------- | ----------------- | ---------------------- | --- | ------ | ------------ | ---- | ------- | ---------- | --- | ------------------ | --- | --- | ---------- | --- |
| ninth                                 | Annual Conference |                        | on  | Neural | Information  | Pro- |         |            |     |                    |     |     |            |     |
|                                       |                   |                        |     |        |              |      | Horton, | M., Mehta, | S., | Farhadi,           | A., | and | Rastegari, | M.  |
| cessingSystems,2025.                  |                   | URLhttps://openreview. |     |        |              |      |         |            |     |                    |     |     |            |     |
|                                       |                   |                        |     |        |              |      | Bytes   | are all    | you | need: Transformers |     |     | operating  | di- |
net/forum?id=Hmepi1Fm2g.
|     |     |     |     |     |     |     | rectly        | on file | bytes. | Transactions |            | on Machine |            | Learn- |
| --- | --- | --- | --- | --- | --- | --- | ------------- | ------- | ------ | ------------ | ---------- | ---------- | ---------- | ------ |
|     |     |     |     |     |     |     | ing Research, |         | 2024.  | ISSN         | 2835-8856. |            | URL https: |        |
Gloeckle,F.,Idrissi,B.Y.,Rozie`re,B.,Lopez-Paz,D.,and
Synnaeve,G. Better&fasterlargelanguagemodelsvia //openreview.net/forum?id=RkaqxxAOfN.
| multi-tokenprediction. |     | arXivpreprintarXiv:2404.19737, |     |     |     |     |        |          |         |     |       |           |     |      |
| ---------------------- | --- | ------------------------------ | --- | --- | --- | --- | ------ | -------- | ------- | --- | ----- | --------- | --- | ---- |
|                        |     |                                |     |     |     |     | Huang, | H., Zhu, | D., Wu, | B., | Zeng, | Y., Wang, | Y., | Min, |
2024.
|     |     |     |     |     |     |     | Q., and | Xun, | Z. Over-tokenized |     | transformer: |     | Vocabu- |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ---- | ----------------- | --- | ------------ | --- | ------- | --- |
E´.,
Godey, N., Castagne´, R., de la Clergerie, and Sagot, lary is generally worth scaling. In Proceedings of the
B. MANTa: Efficient gradient-based tokenization for 42ndInternationalConferenceonMachineLearning,pp.
end-to-end robust language modeling. In Findings of 26261–26282,2025. URLhttps://proceedings.
theAssociationforComputationalLinguistics: EMNLP mlr.press/v267/huang25bb.html.
| 2022,2022. | URLhttps://aclanthology.org/ |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ---------- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2022.findings-emnlp.207. Huang,S.,Cheng,T.,Liu,J.K.,Hao,J.,Song,L.,Xu,Y.,
|         |               |           |     |      |           |        | Yang,J.,Liu,J.,Zhang,C.,Chai,L.,etal. |     |     |     |     |     | Opencoder: |     |
| ------- | ------------- | --------- | --- | ---- | --------- | ------ | ------------------------------------- | --- | --- | --- | --- | --- | ---------- | --- |
| Graves, | A. Generating | sequences |     | with | recurrent | neural |                                       |     |     |     |     |     |            |     |
Theopencookbookfortop-tiercodelargelanguagemod-
networks. arXivpreprintarXiv:1308.0850,2013. els. arXivpreprintarXiv:2411.04905,2024a.
Grivas,A.,Loconte,L.,vanKrieken,E.,Nawrot,P.,Zhao, Huang, Y., Zhang, J., Shan, Z., and He, J. Compres-
Y.,Wielewski,E.,Minervini,P.,Ponti,E.,andVergari, sion represents intelligence linearly. In First Confer-
A. Fastandexpressivemulti-tokenpredictionwithproba-
|                        |     |     |     |     |     |     | ence                                  | on Language |     | Modeling, | 2024b. |     | URL https: |     |
| ---------------------- | --- | --- | --- | --- | --- | --- | ------------------------------------- | ----------- | --- | --------- | ------ | --- | ---------- | --- |
| bilisticcircuits,2025. |     |     |     |     |     |     | //openreview.net/forum?id=SHMj84U5SH. |             |     |           |        |     |            |     |
Han,X.,Ghazvininejad,M.,Koh,P.W.,andTsvetkov,Y. Hwang,K.andSung,W.Character-levellanguagemodeling
Jpeg-lm: Llmsasimagegeneratorswithcanonicalcodec withhierarchicalrecurrentneuralnetworks.In2017IEEE
| representations. |     | arXivpreprintarXiv:2408.08459,2024. |     |     |     |     |     |     |     |     |     |     |     |     |
| ---------------- | --- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
internationalconferenceonacoustics,speechandsignal
processing(ICASSP),pp.5720–5724.IEEE,2017.
| Hawthorne, | C., Jaegle,     | A.,       | Cangea,       | C.,    | Borgeaud,    | S.,      |                |           |              |         |          |           |          |       |
| ---------- | --------------- | --------- | ------------- | ------ | ------------ | -------- | -------------- | --------- | ------------ | ------- | -------- | --------- | -------- | ----- |
| Nash,      | C., Malinowski, |           | M., Dieleman, |        | S., Vinyals, | O.,      |                |           |              |         |          |           |          |       |
|            |                 |           |               |        |              |          | Hwang,         | S., Wang, | B.,          | and Gu, | A.       | Dynamic   | chunking |       |
| Botvinick, | M., Simon,      | I.,       | Sheahan,      | H.,    | Zeghidour,   | N.,      |                |           |              |         |          |           |          |       |
|            |                 |           |               |        |              |          | for end-to-end |           | hierarchical |         | sequence | modeling. |          | arXiv |
| Alayrac,   | J.-B.,          | Carreira, | J., and       | Engel, | J.           | General- |                |           |              |         |          |           |          |       |
preprintarXiv:2507.07955,2025.
| purpose, | long-context |     | autoregressive |     | modeling | with |     |     |     |     |     |     |     |     |
| -------- | ------------ | --- | -------------- | --- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
perceiver AR. In Proceedings of the 39th Interna- Jaegle, A., Borgeaud, S., Alayrac, J.-B., Doersch, C.,
tionalConferenceonMachineLearning,pp.8535–8558, Ionescu, C., Ding, D., Koppula, S., Zoran, D., Brock,
11

ProxyCompressionforLanguageModeling
A., Shelhamer, E., etal. Perceiverio: Ageneralarchi- Lester, B., Lee, J., Alemi, A., Pennington, J., Roberts,
tectureforstructuredinputs&outputs. arXivpreprint A., Sohl-Dickstein, J., and Constant, N. Training
arXiv:2107.14795,2021a. llms over neurally compressed text. arXiv preprint
arXiv:2404.03626,2024.
| Jaegle, A., | Gimeno, | F., Brock, | A., Vinyals, | O., Zisser- |     |     |     |     |
| ----------- | ------- | ---------- | ------------ | ----------- | --- | --- | --- | --- |
man, A., and Carreira, J. Perceiver: General per- Li,J.,Zhao,W.X.,Nie,J.-Y.,andWen,J.-R. Glyphdiffu-
| ception | with iterative | attention. | In Proceedings | of  |                                        |     |     |               |
| ------- | -------------- | ---------- | -------------- | --- | -------------------------------------- | --- | --- | ------------- |
|         |                |            |                |     | sion: Textgenerationasimagegeneration. |     |     | arXivpreprint |
the 38th International Conference on Machine Learn- arXiv:2304.12519,2023.
| ing, 2021b. | URL | https://proceedings.mlr. |     |     |                 |          |                           |     |
| ----------- | --- | ------------------------ | --- | --- | --------------- | -------- | ------------------------- | --- |
|             |     |                          |     |     | Li,Y.andChen,Z. | Bytegen: | Atokenizer-freegenerative |     |
press/v139/jaegle21a.html.
|     |     |     |     |     | modelfororderbookeventsinbytespace. |     |     | arXivpreprint |
| --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | ------------- |
Jiang, Z., Yang, M., Tsirlin, M., Tang, R., Dai, Y., and arXiv:2508.02247,2025.
| Lin,J. “low-resource”textclassification: |     |     |     | Aparameter- |                                                       |     |     |     |
| ---------------------------------------- | --- | --- | --- | ----------- | ----------------------------------------------------- | --- | --- | --- |
|                                          |     |     |     | InFindings  | Limisiewicz,T.,Blevins,T.,Gonen,H.,Ahia,O.,andZettle- |     |     |     |
freeclassificationmethodwithcompressors.
oftheAssociationforComputationalLinguistics: ACL moyer,L. Myte: Morphology-drivenbyteencodingfor
2023,2023. URLhttps://aclanthology.org/ betterandfairermultilinguallanguagemodeling. arXiv
preprintarXiv:2403.10691,2024.
2023.findings-acl.426.
Jolicoeur-Martineau, A. and Gervais, E. Bytecraft: Gen- Liu, A., Hayase, J., Hofmann, V., Oh, S., Smith, N. A.,
erating video games and animations through bytes. and Choi, Y. SuperBPE: Space travel for language
models. InSecondConferenceonLanguageModeling,
| Preprints, | 2025. | doi: 10.20944/preprints202503. |     |     |     |     |     |     |
| ---------- | ----- | ------------------------------ | --- | --- | --- | --- | --- | --- |
1962.v1. URL https://www.preprints.org/ 2025. URLhttps://openreview.net/forum?
| manuscript/202503.1962/v1. |     |     |     |     | id=lcDRvffeNP. |     |     |     |
| -------------------------- | --- | --- | --- | --- | -------------- | --- | --- | --- |
Kallini,J.,Murty,S.,Manning,C.D.,Potts,C.,andCsorda´s, Liu,J.,Xia,C.S.,Wang,Y.,andZHANG,L. Isyourcode
R. Mrt5: Dynamic token merging for efficient byte- generatedbychatGPTreallycorrect? rigorousevaluation
levellanguagemodels. arXivpreprintarXiv:2410.20771, oflargelanguagemodelsforcodegeneration. InThirty-
|     |     |     |     |     | seventh | Conference on Neural | Information | Processing |
| --- | --- | --- | --- | --- | ------- | -------------------- | ----------- | ---------- |
2024.
|     |     |     |     |     | Systems,2023. | URLhttps://openreview.net/ |     |     |
| --- | --- | --- | --- | --- | ------------- | -------------------------- | --- | --- |
Kingma,D.P.andBa,J. Adam: Amethodforstochastic forum?id=1qvx610Cu7.
| optimization. | arXivpreprintarXiv:1412.6980,2014. |     |     |     |                           |     |                          |     |
| ------------- | ---------------------------------- | --- | --- | --- | ------------------------- | --- | ------------------------ | --- |
|               |                                    |     |     |     | Loshchilov,I.andHutter,F. |     | Decoupledweightdecayreg- |     |
Kudo,T.Subwordregularization:Improvingneuralnetwork
|     |     |     |     |     | ularization. | In International | Conference | on Learning |
| --- | --- | --- | --- | --- | ------------ | ---------------- | ---------- | ----------- |
translationmodelswithmultiplesubwordcandidates. In Representations,2019.
Proceedingsofthe56thAnnualMeetingoftheAssocia-
| tionforComputationalLinguistics(Volume1: |     |     |     | LongPa- |                                          |     |     |             |
| ---------------------------------------- | --- | --- | --- | ------- | ---------------------------------------- | --- | --- | ----------- |
|                                          |     |     |     |         | Lotz,J.,Salesky,E.,Rust,P.,andElliott,D. |     |     | Textrender- |
pers),2018. URLhttps://aclanthology.org/ ing strategies for pixel language models. In Proceed-
P18-1007/. ings of the 2023 Conference on Empirical Methods in
|                         |     |                |     |            | NaturalLanguageProcessing,2023. |     |     | URLhttps:// |
| ----------------------- | --- | -------------- | --- | ---------- | ------------------------------- | --- | --- | ----------- |
| Kudo,T.andRichardson,J. |     | SentencePiece: |     | Asimpleand |                                 |     |     |             |
aclanthology.org/2023.emnlp-main.628.
languageindependentsubwordtokenizeranddetokenizer
forneural textprocessing. In Proceedingsofthe 2018 Lundberg,S.andRibeiro,M.T. Theartofpromptdesign:
ConferenceonEmpiricalMethodsinNaturalLanguage
|     |     |     |     |     | Promptboundariesandtokenhealing. |     |     | Medium,2023. |
| --- | --- | --- | --- | --- | -------------------------------- | --- | --- | ------------ |
Processing:SystemDemonstrations,2018.URLhttps:
//aclanthology.org/D18-2012/. Microsoft. Guidance, 2023. URL https://github.
com/microsoft/guidance.
| Land,S.andBartolo,M. |     | Fishingformagikarp: |     | Automat- |     |     |     |     |
| -------------------- | --- | ------------------- | --- | -------- | --- | --- | --- | --- |
ically detecting under-trained tokens in large language Minixhofer,B.,Murray,T.,Limisiewicz,T.,Korhonen,A.,
models. arXivpreprintarXiv:2405.05417,2024. Zettlemoyer,L.,Smith,N.A.,Ponti,E.M.,Soldaini,L.,
|                 |           |            |          |               | andHofmann,V.     | Bolmo:                         | Byteifyingthenextgeneration |     |
| --------------- | --------- | ---------- | -------- | ------------- | ----------------- | ------------------------------ | --------------------------- | --- |
| Lee, K., Joshi, | M., Turc, | I. R., Hu, | H., Liu, | F., Eisensch- |                   |                                |                             |     |
|                 |           |            |          |               | oflanguagemodels. | arXivpreprintarXiv:2512.15586, |                             |     |
los,J.M.,Khandelwal,U.,Shaw,P.,Chang,M.-W.,and
2025.
| Toutanova,K. | Pix2Struct: | Screenshotparsingaspretrain- |     |     |     |     |     |     |
| ------------ | ----------- | ---------------------------- | --- | --- | --- | --- | --- | --- |
ingforvisuallanguageunderstanding. InProceedingsof Molybog,I.,Albert,P.,Chen,M.,DeVito,Z.,Esiobu,D.,
the40thInternationalConferenceonMachineLearning, Goyal,N.,Koura,P.S.,Narang,S.,Poulton,A.,Silva,R.,
2023.URLhttps://proceedings.mlr.press/ etal. Atheoryonadaminstabilityinlarge-scalemachine
v202/lee23g.html. learning. arXivpreprintarXiv:2304.09871,2023.
12

ProxyCompressionforLanguageModeling
Nawrot,P.,Tworkowski,S.,Tyrolski,M.,Kaiser,L.,Wu,Y., languages. InThirty-seventhConferenceonNeuralIn-
Szegedy,C.,andMichalewski,H.Hierarchicaltransform- formation Processing Systems, 2023. URL https:
//openreview.net/forum?id=78yDLKi95p.
| ersaremoreefficientlanguagemodels.         |     |                              |     |     | InFindingsof |       |     |                   |     |              |     |              |        |
| ------------------------------------------ | --- | ---------------------------- | --- | --- | ------------ | ----- | --- | ----------------- | --- | ------------ | --- | ------------ | ------ |
| theAssociationforComputationalLinguistics: |     |                              |     |     |              | NAACL |     |                   |     |              |     |              |        |
|                                            |     |                              |     |     |              |       |     | Phan, B., Havasi, |     | M., Muckley, | M., | and Ullrich, | K. Un- |
| 2022,2022.                                 |     | URLhttps://aclanthology.org/ |     |     |              |       |     |                   |     |              |     |              |        |
derstandingandmitigatingtokenizationbiasinlanguage
2022.findings-naacl.117.
|     |     |     |     |     |     |     |     | models. | arXivpreprintarXiv:2406.16829,2024. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ----------------------------------- | --- | --- | --- | --- |
Nawrot,P.,Chorowski,J.,Lancucki,A.,andPonti,E.M.
Qu,X.,Wang,S.,Huang,Z.,Hua,K.,Yin,F.,Zhu,R.-J.,
Efficient transformers with dynamic token pooling. In Zhou,J.,Min,Q.,Wang,Z.,Li,Y.,etal. Dynamiclarge
Proceedingsofthe61stAnnualMeetingoftheAssocia-
conceptmodels:Latentreasoninginanadaptivesemantic
| tionforComputationalLinguistics(Volume1: |     |                              |     |     |     | LongPa- |     |                                            |     |     |     |     |     |
| ---------------------------------------- | --- | ---------------------------- | --- | --- | --- | ------- | --- | ------------------------------------------ | --- | --- | --- | --- | --- |
|                                          |     |                              |     |     |     |         |     | space. arXivpreprintarXiv:2512.24617,2025. |     |     |     |     |     |
| pers),2023.                              |     | URLhttps://aclanthology.org/ |     |     |     |         |     |                                            |     |     |     |     |     |
2023.acl-long.353. Radford, A., Jozefowicz, R., and Sutskever, I. Learning
|             |     |            |     |             |     |            |     | to generate | reviews | and discovering |     | sentiment. | arXiv |
| ----------- | --- | ---------- | --- | ----------- | --- | ---------- | --- | ----------- | ------- | --------------- | --- | ---------- | ----- |
| Neitemeier, | P., | Deiseroth, | B., | Eichenberg, | C., | andBalles, |     |             |         |                 |     |            |       |
preprintarXiv:1704.01444,2017.
| L. Hierarchicalautoregressivetransformers: |     |     |     |     |     | Combining |     |     |     |     |     |     |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
Radford,A.,Wu,J.,Child,R.,Luan,D.,Amodei,D.,and
byte-˜andword-levelprocessingforrobust,adaptablelan-
Sutskever,I.Languagemodelsareunsupervisedmultitask
| guagemodels. |     | arXivpreprintarXiv:2501.10322,2025. |     |     |     |     |     |     |     |     |     |     |     |
| ------------ | --- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
learners,2019.
OLMoTeam,Walsh,P.,Soldaini,L.,Groeneveld,D.,Lo,
|     |     |     |     |     |     |     |     | Rae, J. W., | Potapenko, | A., Jayakumar, |     | S. M., | Hillier, C., |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ---------- | -------------- | --- | ------ | ------------ |
K.,Arora,S.,Bhagia,A.,Gu,Y.,Huang,S.,Jordan,M.,
|           |     |          |     |          |               |     |        | andLillicrap,T.P.       |                  | Compressivetransformersforlong- |                           |     |          |
| --------- | --- | -------- | --- | -------- | ------------- | --- | ------ | ----------------------- | ---------------- | ------------------------------- | ------------------------- | --- | -------- |
| Lambert,  | N., | Schwenk, | D., | Tafjord, | O., Anderson, |     | T.,    |                         |                  |                                 |                           |     |          |
|           |     |          |     |          |               |     |        | rangesequencemodelling. |                  |                                 | InInternationalConference |     |          |
| Atkinson, | D., | Brahman, | F., | Clark,   | C., Dasigi,   | P., | Dziri, |                         |                  |                                 |                           |     |          |
|           |     |          |     |          |               |     |        | on Learning             | Representations, |                                 | 2020.                     | URL | https:// |
N.,Guerquin,M.,Ivison,H.,Koh,P.W.,Liu,J.,Malik, openreview.net/forum?id=SylKikSYDH.
S.,Merrill,W.,Miranda,L.J.V.,Morrison,J.,Murray,
T., Nam, C., Pyatkin, V., Rangapur, A., Schmitz, M., Rumbelow, J.andWatkins, M. Solidgoldmagikarp(plus,
Skjonsberg, S., Wadden, D., Wilhelm, C., Wilson, M., promptgeneration),2023.
Zettlemoyer,L.,Farhadi,A.,Smith,N.A.,andHajishirzi,
H. 2olmo2furious. arXivpreprintarXiv:2501.00656, Rust,P.,Lotz,J.F.,Bugliarello,E.,Salesky,E.,deLhoneux,
|     |     |     |     |     |     |     |     | M., and | Elliott, | D. Language | modelling |     | with pixels. |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | -------- | ----------- | --------- | --- | ------------ |
2025.
InTheEleventhInternationalConferenceonLearning
OpenAI. GPT-4 technical report. arXiv preprint Representations,2023. URLhttps://openreview.
net/forum?id=FkSp8VW8RjH.
arXiv:2303.08774,2023.
|     |     |     |     |     |     |     |     | Salesky,E.,Etter,D.,andPost,M. |     |     | Robustopen-vocabulary |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------ | --- | --- | --------------------- | --- | --- |
Owodunni,A.T.,Ahia,O.,andKumar,S.Flexitokens:Flex-
|                   |     |     |          |          |         |     |       | translationfromvisualtextrepresentations. |      |            |     |           | InProceed- |
| ----------------- | --- | --- | -------- | -------- | ------- | --- | ----- | ----------------------------------------- | ---- | ---------- | --- | --------- | ---------- |
| ible tokenization |     | for | evolving | language | models. |     | arXiv |                                           |      |            |     |           |            |
|                   |     |     |          |          |         |     |       | ings of the                               | 2021 | Conference | on  | Empirical | Methods in |
preprintarXiv:2507.12720,2025.
|     |     |     |     |     |     |     |     | NaturalLanguageProcessing,2021. |     |     |     | URLhttps:// |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | ----------- | --- |
aclanthology.org/2021.emnlp-main.576.
| Pagnoni, | A., Pasunuru, |     | R., | Rodriguez, | P., | Nguyen, | J., |     |     |     |     |     |     |
| -------- | ------------- | --- | --- | ---------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
Muller,B.,Li,M.,Zhou,C.,Yu,L.,Weston,J.,Zettle-
Salesky,E.,Verma,N.,Koehn,P.,andPost,M.Multilingual
| moyer,L.,etal. |     | Bytelatenttransformer: |     |     |     | Patchesscale |     |     |     |     |     |     |     |
| -------------- | --- | ---------------------- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
pixelrepresentationsfortranslationandeffectivecross-
| better   | than tokens. |     | arXiv | preprint | arXiv:2412.09871, |            |     |                                                |     |                                  |     |     |     |
| -------- | ------------ | --- | ----- | -------- | ----------------- | ---------- | --- | ---------------------------------------------- | --- | -------------------------------- | --- | --- | --- |
|          |              |     |       |          |                   |            |     | lingualtransfer.                               |     | InProceedingsofthe2023Conference |     |     |     |
| 2024.    |              |     |       |          |                   |            |     | onEmpiricalMethodsinNaturalLanguageProcessing, |     |                                  |     |     |     |
|          |              |     |       |          |                   |            |     | 2023. URLhttps://aclanthology.org/2023.        |     |                                  |     |     |     |
| Park, J. | and Johnson, |     | J.    | Rgb no   | more:             | Minimally- |     |                                                |     |                                  |     |     |     |
emnlp-main.854.
| decodedjpegvisiontransformers. |     |     |     | InProceedingsofthe |     |     |     |     |     |     |     |     |     |
| ------------------------------ | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
IEEE/CVFConferenceonComputerVisionandPattern Schmidt, C. W., Reddy, V., Zhang, H., Alameddine, A.,
Recognition(CVPR),pp.22334–22346,June2023. Uzan,O.,Pinter,Y.,andTanner,C. Tokenizationismore
|                                                       |     |     |                                 |     |     |     |     | than compression. |     | arXiv | preprint | arXiv:2402.18376, |     |
| ----------------------------------------------------- | --- | --- | ------------------------------- | --- | --- | --- | --- | ----------------- | --- | ----- | -------- | ----------------- | --- |
| Pe´rez,J.C.,Pardo,A.,Soldan,M.,Itani,H.,Leon-Alcazar, |     |     |                                 |     |     |     |     | 2024.             |     |       |          |                   |     |
| J.,andGhanem,B.                                       |     |     | Compressed-languagemodelsforun- |     |     |     |     |                   |     |       |          |                   |     |
derstandingcompressedfileformats: ajpegexploration. Schmidt,C.W.,Reddy,V.,Tanner,C.,andPinter,Y.Bound-
|     |     |     |     |     |     |     |     | less byte | pair encoding: | Breaking |     | the pre-tokenization |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | -------------- | -------- | --- | -------------------- | --- |
arXivpreprintarXiv:2405.17146,2024.
|     |     |     |     |     |     |     |     | barrier. | InSecondConferenceonLanguageModeling, |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------------------------------------- | --- | --- | --- | --- |
Petrov, A., Malfa, E. L., Torr, P., and Bibi, A. Lan- 2025. URLhttps://openreview.net/forum?
| guage | model | tokenizers | introduce |     | unfairness | between |     | id=oPAjXGV8qQ. |     |     |     |     |     |
| ----- | ----- | ---------- | --------- | --- | ---------- | ------- | --- | -------------- | --- | --- | --- | --- | --- |
13

ProxyCompressionforLanguageModeling
Schuster,M.andNakajima,K. Japaneseandkoreanvoice Vieira, T., LeBrun, B., Giulianelli, M., Gastaldi, J. L.,
search. In2012IEEEinternationalconferenceonacous- DuSell, B., Terilla, J., O’Donnell, T. J., and Cotterell,
tics,speechandsignalprocessing(ICASSP),2012. R. Fromlanguagemodelsovertokenstolanguagemod-
|                                   |     |            |      |         |               |         | els over | characters. | arXiv | preprint | arXiv:2412.03719, |     |     |
| --------------------------------- | --- | ---------- | ---- | ------- | ------------- | ------- | -------- | ----------- | ----- | -------- | ----------------- | --- | --- |
| Sennrich,R.,Haddow,B.,andBirch,A. |     |            |      |         | Neuralmachine |         | 2024.    |             |       |          |                   |     |     |
| translation                       | of  | rare words | with | subword | units.        | In Pro- |          |             |       |          |                   |     |     |
Wang,D.,Li,Y.,Jiang,J.,Ding,Z.,Jiang,G.,Liang,J.,and
| ceedings | of the | 54th | Annual | Meeting | of the | Associa- |     |     |     |     |     |     |     |
| -------- | ------ | ---- | ------ | ------- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- |
tionforComputationalLinguistics(Volume1: LongPa- Yang,D. Tokenizationmatters! degradinglargelanguage
URLhttps://aclanthology.org/ models through challenging their tokenization. arXiv
pers),2016.
preprintarXiv:2405.17067,2024a.
P16-1162.
|            |            |          |           |          |       |           | Wang, J.,  | Gangavarapu, |     | T., Yan,  | J. N., and | Rush, | A. M.  |
| ---------- | ---------- | -------- | --------- | -------- | ----- | --------- | ---------- | ------------ | --- | --------- | ---------- | ----- | ------ |
| Slagle, K. | Spacebyte: |          | Towards   | deleting |       | tokeniza- |            |              |     |           |            |       |        |
|            |            |          |           |          |       |           | Mambabyte: | Token-free   |     | selective | state      | space | model. |
| tion from  | large      | language | modeling. |          | arXiv | preprint  |            |              |     |           |            |       |        |
arXivpreprintarXiv:2401.13660,2024b.
arXiv:2404.14408,2024.
Wang,S.,Li,Z.,Qian,H.,Yang,C.,Wang,Z.,Shang,M.,
Stern,M.,Shazeer,N.,andUszkoreit,J. Blockwiseparallel Kumar, V., Tan, S., Ray, B., Bhatia, P., Nallapati, R.,
| decodingfordeepautoregressivemodels. |     |     |     |     | Advancesin |     |             |       |       |     |           |            |     |
| ------------------------------------ | --- | --- | --- | --- | ---------- | --- | ----------- | ----- | ----- | --- | --------- | ---------- | --- |
|                                      |     |     |     |     |            |     | Ramanathan, | M.K., | Roth, | D., | andXiang, | B. ReCode: |     |
NeuralInformationProcessingSystems,2018.
|     |     |     |     |     |     |     | Robustnessevaluationofcodegenerationmodels. |     |     |     |     |     | InPro- |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- | ------ |
ceedingsofthe61stAnnualMeetingoftheAssociation
Sun,L.,Hashimoto,K.,Yin,W.,Asai,A.,Li,J.,Yu,P.,and
|          |           |                                |     |     |     |     | forComputationalLinguistics(Volume1: |     |     |     |     | LongPapers), |     |
| -------- | --------- | ------------------------------ | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- | ------------ | --- |
| Xiong,C. | Adv-bert: | Bertisnotrobustonmisspellings! |     |     |     |     |                                      |     |     |     |     |              |     |
2023. URLhttps://aclanthology.org/2023.
| generating | nature | adversarial |     | samples | on bert. | arXiv |     |     |     |     |     |     |     |
| ---------- | ------ | ----------- | --- | ------- | -------- | ----- | --- | --- | --- | --- | --- | --- | --- |
acl-long.773.
preprintarXiv:2003.04985,2020.
|                                  |              |     |             |                 |               |     | Wei,H.,Sun,Y.,andLi,Y. |                                     |     | Deepseek-ocr: |     | Contextsoptical |     |
| -------------------------------- | ------------ | --- | ----------- | --------------- | ------------- | --- | ---------------------- | ----------------------------------- | --- | ------------- | --- | --------------- | --- |
| Sutskever,                       | I., Martens, | J., | and Hinton, | G.              | E. Generating |     |                        |                                     |     |               |     |                 |     |
|                                  |              |     |             |                 |               |     | compression.           | arXivpreprintarXiv:2510.18234,2025. |     |               |     |                 |     |
| textwithrecurrentneuralnetworks. |              |     |             | InProceedingsof |               |     |                        |                                     |     |               |     |                 |     |
the28thinternationalconferenceonmachinelearning Wortsman,M.,Liu,P.J.,Xiao,L.,Everett,K.,Alemi,A.,
(ICML-11),pp.1017–1024,2011. Adlam,B.,Co-Reyes,J.D.,Gur,I.,Kumar,A.,Novak,
|     |     |     |     |     |     |     | R.,etal. | Small-scaleproxiesforlarge-scaletransformer |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------------------------------------- | --- | --- | --- | --- | --- |
Tai,Y.,Liao,X.,Suglia,A.,andVergari,A. Pixar: Auto- traininginstabilities. arXivpreprintarXiv:2309.14322,
| regressive | language | modeling |     | in pixel | space. | arXiv |     |     |     |     |     |     |     |
| ---------- | -------- | -------- | --- | -------- | ------ | ----- | --- | --- | --- | --- | --- | --- | --- |
2023.
preprintarXiv:2401.03321,2024.
Wu,S.,Tan,X.,Wang,Z.,Wang,R.,Li,X.,andSun,M.
Tao,C.,Liu,Q.,Dou,L.,Muennighoff,N.,Wan,Z.,Luo, Beyondlanguagemodels: Bytemodelsaredigitalworld
P.,Lin,M.,andWong,N. Scalinglawswithvocabulary: simulators. arXivpreprintarXiv:2402.19155,2024.
| Larger | models | deserve    | larger | vocabularies.      | In  | Thirty- |         |           |           |     |        |              |     |
| ------ | ------ | ---------- | ------ | ------------------ | --- | ------- | ------- | --------- | --------- | --- | ------ | ------------ | --- |
|        |        |            |        |                    |     |         | Wu, Y., | Schuster, | M., Chen, | Z., | Le, Q. | V., Norouzi, | M., |
| eighth | Annual | Conference | on     | Neural Information |     | Pro-    |         |           |           |     |        |              |     |
URLhttps://openreview. Macherey,W.,Krikun,M.,Cao,Y.,Gao,Q.,Macherey,
cessingSystems,2024.
|     |     |     |     |     |     |     | K., et | al. Google’s | neural | machine | translation |     | system: |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------------ | ------ | ------- | ----------- | --- | ------- |
net/forum?id=sKCKPr8cRL.
Bridgingthegapbetweenhumanandmachinetranslation.
Tay, Y., Tran, V. Q., Ruder, S., Gupta, J., Chung, H. W., arXivpreprintarXiv:1609.08144,2016.
Bahri,D.,Qin,Z.,Baumgartner,S.,Yu,C.,andMetzler,
Xue,L.,Barua,A.,Constant,N.,Al-Rfou,R.,Narang,S.,
| D. Charformer: |     | Fastcharactertransformersviagradient- |     |     |     |     |       |              |     |             |     |               |     |
| -------------- | --- | ------------------------------------- | --- | --- | --- | --- | ----- | ------------ | --- | ----------- | --- | ------------- | --- |
|                |     |                                       |     |     |     |     | Kale, | M., Roberts, | A., | and Raffel, | C.  | ByT5: Towards |     |
InInternationalConference
basedsubwordtokenization. a token-free future with pre-trained byte-to-byte mod-
| on Learning | Representations, |     |     | 2022. URL | https:// |     |     |     |     |     |     |     |     |
| ----------- | ---------------- | --- | --- | --------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
els. TransactionsoftheAssociationforComputational
openreview.net/forum?id=JtBRnrlOEFN.
|     |     |     |     |     |     |     | Linguistics, | 2022. | URL | https://aclanthology. |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ----- | --- | --------------------- | --- | --- | --- |
org/2022.tacl-1.17.
| Team,T.A.L.A. |     | Nomoreretokenizationdrift: |     |     | Returning |     |     |     |     |     |     |     |     |
| ------------- | --- | -------------------------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
tokenidsviatheopenaicompatibleapimattersinagentrl,
|       |                                   |     |     |     |     |     | Xuyang,  | S., Luo,  | X., Cheng, | T.,    | Chu, Z.,  | Li, H., | Huang, |
| ----- | --------------------------------- | --- | --- | --- | --- | --- | -------- | --------- | ---------- | ------ | --------- | ------- | ------ |
| 2025. | URL https://blog.vllm.ai/2025/10/ |     |     |     |     |     |          |           |            |        |           |         |        |
|       |                                   |     |     |     |     |     | S., Zhu, | Q., Wang, | Q.,        | Zhang, | X., Zhou, | S., et  | al. Is |
22/agent-lightning.html. compressionreallylinearwithcodeintelligence? arXiv
preprintarXiv:2505.11441,2025.
| Videau, | M., Idrissi, | B.  | Y., Leite, | A., Schoenauer, |     | M., |     |     |     |     |     |     |     |
| ------- | ------------ | --- | ---------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Teytaud, O., and Lopez-Paz, D. From bytes to ideas: Yang,J. Rethinkingtokenization: Craftingbettertokeniz-
Language modeling with autoregressive u-nets. arXiv ersforlargelanguagemodels. InternationalJournalof
| preprintarXiv:2506.14761,2025. |     |     |     |     |     |     | ChineseLinguistics,2024. |     |     |     |     |     |     |
| ------------------------------ | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | --- | --- | --- | --- |
14

ProxyCompressionforLanguageModeling
Yang,J.,Wang,Z.,Lin,Y.,andZhao,Z.Problematictokens:
| Tokenizerbiasinlargelanguagemodels. |     |     |     |     | arXivpreprint |     |
| ----------------------------------- | --- | --- | --- | --- | ------------- | --- |
arXiv:2406.11214,2024.
Yu,D.,Cohen,E.,Ghazi,B.,Huang,Y.,Kamath,P.,Ku-
| mar,                    | R., Liu, | D., and | Zhang,                  | C. Scaling | embedding |     |
| ----------------------- | -------- | ------- | ----------------------- | ---------- | --------- | --- |
| layersinlanguagemodels. |          |         | InTheThirty-ninthAnnual |            |           |     |
ConferenceonNeuralInformationProcessingSystems,
2025. URLhttps://openreview.net/forum?
id=gH4BRa4ZP3.
Yu,L.,Simig,D.,Flaherty,C.,Aghajanyan,A.,Zettlemoyer,
| L.,andLewis,M. |     | MEGABYTE:Predictingmillion-byte |     |     |     |     |
| -------------- | --- | ------------------------------- | --- | --- | --- | --- |
sequenceswithmultiscaletransformers.InThirty-seventh
ConferenceonNeuralInformationProcessingSystems,
2023. URLhttps://openreview.net/forum?
id=JTmO2V9Xpz.
Zheng,B.S.,Liu,A.,Ahia,O.,Hayase,J.,Choi,Y.,and
| Smith,                                       | N. A. | Broken | tokens? | your language |     | model |
| -------------------------------------------- | ----- | ------ | ------- | ------------- | --- | ----- |
| cansecretlyhandlenon-canonicaltokenizations. |       |        |         |               |     | arXiv |
preprintarXiv:2506.19004,2025a.
| Zheng, | L., Yuan, | J., Wang,   | C.,       | and Kong, | L.           | Effi- |
| ------ | --------- | ----------- | --------- | --------- | ------------ | ----- |
| cient  | attention | via control | variates. | In        | The Eleventh |       |
InternationalConferenceonLearningRepresentations,
2023. URLhttps://openreview.net/forum?
id=G-uNfHKrj46.
Zheng,L.,Zhao,X.,Wang,G.,Wu,C.,Dong,D.,Wang,A.,
Wang,M.,Du,Y.,Bo,H.,Sharma,A.,Li,B.,Zhang,K.,
Hu,C.,Thakker,U.,andKong,L.Evabyte:Efficientbyte-
| level | language | models | at scale, | 2025b. | URL https: |     |
| ----- | -------- | ------ | --------- | ------ | ---------- | --- |
//hkunlp.github.io/blog/2025/evabyte.
| Zhu, T., | Liu, Q., | Wang,      | H., Chen,   | S., Gu, | X., Pang,        | T., |
| -------- | -------- | ---------- | ----------- | ------- | ---------------- | --- |
| and Kan, | M.-Y.    | Skyladder: | Better      | and     | faster pretrain- |     |
|          |          |            |             |         | arXiv preprint   |     |
| ing via  | context  | window     | scheduling. |         |                  |     |
arXiv:2503.15450,2025.
| Zouhar,         | V., Meister, | C.,                                 | Gastaldi, | J., Du, | L., Sachan, | M., |
| --------------- | ------------ | ----------------------------------- | --------- | ------- | ----------- | --- |
| andCotterell,R. |              | Tokenizationandthenoiselesschannel. |           |         |             |     |
InProceedingsofthe61stAnnualMeetingoftheAssoci-
| ationforComputationalLinguistics(Volume1: |     |                              |     |     | LongPa- |     |
| ----------------------------------------- | --- | ---------------------------- | --- | --- | ------- | --- |
| pers),2023.                               |     | URLhttps://aclanthology.org/ |     |     |         |     |
2023.acl-long.284/.
15

ProxyCompressionforLanguageModeling
Appendix
A.Token-levelCompressionRatiosforProxyCompression
Weimplementmixed-representationtraininginthesamplelevel. Thisindicatesthatalthoughdocumentswillbecompressed
withacertainprobabilityr, theactualratioofcompressedtokenspresentinthecontextwillbedifferentfrom. Inthis
section,weprovidearoughestimateofthetoken-levelcompressionratio.
Forsimplicity,weconsiderafixedbatchsizepertrainingstep,thatis,thetotalnumberofsymbolsisfixed,denotedby
M. Forrawbytemodels,weassumeeachbatchconsistsofN inputdocumentseachwithaveragesamplelengthL ;for
b b
compression-basedmodel,thiscomprisesN inputsampleswithaveragelengthL . Wealsodenotethecompressionrate
|     |     | t   |     |     | t   |     |
| --- | --- | --- | --- | --- | --- | --- |
Lb.
| broughtbycompressionasC | = Asaresult,wehave |     |     |     |     |     |
| ----------------------- | ------------------ | --- | --- | --- | --- | --- |
Lt
|     | M =N | t L t =N | b L b =N | b CL t →N | t =CN b , |     |
| --- | ---- | -------- | -------- | --------- | --------- | --- |
whichindicatesthatcompression-basedmodelswillapproximatelyconsumeC×moresamplesthanrawbytemodels. Now
considerourproxycompressionframework,whereweadditionallymaintainamixingratiorsuchthatwithprobability
r aninputsamplewillbecompressedwithacompressoratrateC. Denotingthetotalnumberofinputsamples(either
compressedornot)pertrainingstepasN′,wehave
|         |           |      | L           |     | (cid:104)r | (cid:105) |
| ------- | --------- | ---- | ----------- | --- | ---------- | --------- |
| M =rN′L | +(1−r)N′L | =rN′ | b +(1−r)N′L |     | = +(1−r)   | N′L ,     |
|         | t         | b    |             |     | b          | b         |
|         |           |      | C           |     | C          |           |
andbycomparingtheabove,weobtain
1
|     |     | N′  | =        | N   | ,   |     |
| --- | --- | --- | -------- | --- | --- | --- |
|     |     |     | r +(1−r) | b   |     |     |
C
which roughly estimates the number of input samples consumed in our compressed-raw mixture. For instance, for
tokenization-based proxies at a rate r = 0.9 with the OpenCoder tokenizer (Huang et al., 2024a), which delivers a
1
compressionrateC ≈3.7,theactualtoken-levelcompressionratewouldbe ≈2.91.
r+(1−r)
C
MixingwithIn-contextTranslationPairing. Whenweemploytranslationpairsintotraining(§2.1),theactualcom-
pressionrateisfurtherdecreased,asthesameinputsamplewillbeduplicatedtwice. Sinceforeachtranslationpair,it
incrementstheamountofbothcompressedandrawdata,wecalibratethemixingratetotakethisintoaccount. Inparticular,
withthemixingrater,weassumetherewillberN samplescompressed,while(1−r)N samplesincludingboththeraw
andcompressedversions. Sotheactualcompressionandrawsampleswouldber+1−r :1−r.
Ifr > 0.5,wemixtranslationpairswithcompressedsamples;conversely,ifr ≤ 0.5,wemixtranslationpairswithraw
samples,asitwouldbeimpossibletoattainacompressed-rawfractionlargerthan0.5ifwesolelymixtranslationandraw
bytes. Concretely,ifwedesireacompressedfractionr,thenthecalibratedmixingrate$r’$ofmixingtranslationpairswith
probabilityr′mustsatisfy
(cid:40) r′+(1−r′)
|     |     |           | = r | , ifr >0.5, |     |     |
| --- | --- | --------- | --- | ----------- | --- | --- |
|     |     | r′        | 1−r |             |     |     |
|     |     | r′        | r   |             |     |     |
|     |     |           | =   | , ifr ≤0.5. |     |     |
|     |     | r′+(1−r′) | 1−r |             |     |     |
Thisgives
(cid:40) 1
|     |     |     | −1, | r >0.5, |     |     |
| --- | --- | --- | --- | ------- | --- | --- |
r′ = r
r
, r ≤0.5.
1−r
Asaresult,wecansampleinputsampleswithtranslationpairsappearingwithprobabilityr′,mixedwithcompressed(resp.
raw)samples,wheretheeffectivefractionofcompressedversusrawsamplesmatchedtheintendedtargetr >0.5(resp.
r ≤0.5).
16

ProxyCompressionforLanguageModeling
We now investigate the delivered token-level compression rate with translation pairs. Assume r > 0.5 which implies
r′ = 1 −1. Thenforeachtrainingbatch,wehave
r
|            |     |         |      |            |     | L         |     | L (cid:20) 1 | (cid:21) |     |
| ---------- | --- | ------- | ---- | ---------- | --- | --------- | --- | ------------ | -------- | --- |
| =(1−r′)N′L |     | +r′N′(L |      | )=(1−r′)N′ |     | b +r′N′(L |     | b)=          | +r′      | N′L |
| M          |     | t       | b +L | t          |     |           |     | b +          |          | b . |
|            |     |         |      |            |     | C         |     | C C          |          |     |
Thisgives
1
N′
|     |     |     |     |     | =   | N ,    |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- |
|     |     |     |     |     | 1 + | 1 −1 b |     |     |     |     |
|     |     |     |     |     | C   | r      |     |     |     |     |
withtheconfigurationabove,thisyieldsanactualcompressionrateofN′ ≈2.62N ,whichisabitslowerthanthatwithout
b
translation. Asaresult,weonlyemploytranslationpairingasawarmupphaseatthebeginningoftraininganddisabledlater
tomaximizetheamountofuniquedatapertrainingstep.
In-contextTranslationPairingWarmup. Alsonoticethatwhenwarmupphasesareincorporated,weconsiderannealing
r(i) linearly from the start point a and ending rate b with T steps (in this work, a = 0.4 and b = 0.9 by default). For
r ≤0.5,wecanfollowingthesimilarreasoningaboveandderive
(cid:20) r′(i) (cid:21)
L b)=
M =(1−r′(i))N′L +r′(i)N′(L +L )=(1−r′(i))N′L +r′(i)N′(L + 1+ N′L .
|     | i b |     | i b | t   |     | i b |     | i b C |     | C i b |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | ----- |
Thisgives
|     |     |     |      | 1   |         | 1       |     |     |     |     |
| --- | --- | --- | ---- | --- | ------- | ------- | --- | --- | --- | --- |
|     |     |     | N′ = |     | N =     |         | N   | .   |     |     |
|     |     |     | i    |     | r′(i) b | r(i)    | b   |     |     |     |
|     |     |     |      | 1+  |         | 1+      | 1   |     |     |     |
|     |     |     |      |     | C       | 1−r(i)C |     |     |     |     |
Thecompressionrateforr >0.5canbecalculatedsimilarly. Weevaluatetheaveragenumberofsamplesprocessedateach
stepasN′ 1 (cid:80)T N′.
:= Thiscanbeevaluatedeitherbyenumeratingeachterminthesummation,orbyapproximating
| T i=1 | i   |     |     |     |     |     |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
withthepiecewiseintegralaverage,whichcanbeevaluatedinclosedformtogiveaquickestimate. Forinstance,inour
defaultschedule,weannealr(i)=0.4+ 0.5i toincreasefrom0.4to0.9atthefirst10000trainingstepsi. Thisgivesthe
10000
averagerateN′ ≈1.38N ,inotherwords,duringthewarmupphase,weonlyprocessonaverage1.38×asmanysamples
b
perstepasapurerawbytemodeltrainingstep.
B.ImplementationDetailsofProxyCompressors
B.1.Tokenization-basedProxyCompression
Thissectionprovidesadditionalimplementationdetailsontokenizer-basedproxycompression,includingrepresentation
formats,encodingstrategies,andpre-tokenizationschemes. Table5summarizesablationresultsacrossthesedesignchoices.
RepresentationFormats. Weconsidertwoformatsforrepresentingtokenizeroutputs:
• Tokenindices(default): EachtokenIDismappedtoadedicatedentryinthelanguagemodelvocabularyandtreatedas
asinglesymbol. Thisachievesthehighestcompressionrate(3.7×withtheOpenCodertokenizer)andyieldsthebest
downstreamperformance.
• Tokenbytes: TokenIDsareserializedasfixed-lengthbytesequences. WechoosethesmallestBsuchthat256B ≥V,
whereV isthetokenizervocabularysize. ForOpenCoder(V = 96,640),thisgivesB = 3,soeachtokenbecomes3
bytes. Underthisscheme, alength-LtokensequenceproducedbythetokenizerisconvertedintoasequenceofBL
symbols. Thisformatkeepsbothrawandcompressedrepresentationsinbytespace,whichwehypothesizedmightease
cross-representationalignment. However,itreducestheeffectivecompressionrateanddoesnotimprovetransfer(Table5).
Apracticaladvantageoftokenbytesisflexibility: sincethelanguagemodelvocabularyisdecoupledfromthetokenizer
vocabulary,arbitrarilylargetokenizers(including“superword”vocabulariesthatmergeacrosswordboundaries(Liuetal.,
2025))canbesupportedwithoutchangingthemodel’sembeddingtable. Forourtoken-byteexperiments,wetrainaBPE
tokenizerwithadefaultvocabularysizeV =65,536onourpretrainingcorpus,sothateachtokenIDcanberepresentedas
exactly2bytes.
17

ProxyCompressionforLanguageModeling
Table5.Ablationstudyondesignchoicesoftokenizerproxycompression.Allmodelsare1.5Bparameterstrainedon100Bsequence
symbolsfromthePythonsubset.Directtoken-indexrepresentationachievesthebestcompression-performancetrade-off.
Format VocabSize Pre-tokenization Encoding CompressionRate Pass@1(%)
Byte 256 Default Default 1.7 14.6
Byte 256 Default GrayCoding 1.7 15.2
Byte 256 Default HuffmanCoding 1.8 18.3
Double-byte 65536 Default Default 3.5 15.2
Byte 256 Line Default 2.3 18.3
Byte 256 SuperBPE Default 2.9 16.5
Token-index 96640 Default — 3.7 20.7
We also explore a double-byte variant that expands the language model vocabulary from 256 to 65,536. Under this
scheme, eachtokenIDmapstoasinglesymbol, ratherthanbeingserializedintomultiplebytes. AsshowninTable5,
double-byteachievesahighercompressionrate(3.5×)thansimplebytes(1.7×)butstillunderperformsdirecttoken-index
representations.
ByteEncodingStrategies. Forthetoken-bytesformat,weexploredseveralencodingstrategies:
• Default(fixed-length): EachtokenIDisconvertedtoaB-bytebig-endianrepresentation. Alltokensoccupythesame
numberofbytes,providinguniformrepresentationcomplexity. Notethatthisimplicitlyencodesfrequencyinformation,
sinceBPEtypicallyassignslowerIDstomorefrequenttokens.
• Huffmancoding: Variable-lengthbytecodesareassignedbasedontokenfrequency,withmorefrequenttokensreceiving
shortercodes. Codesarebyte-alignedandsatisfytheKraft-McMillaninequalityforprefix-freedecodability. Inpractice,
thisyieldsonlymarginalcompressionimprovementsoverfixed-lengthencoding.
• Graycoding: TokensarefirstsortedlexicographicallybytheirUTF-8surfaceformsandassignedsequentialranks. These
ranksarethenconvertedtoGraycodes,ensuringthatlexicographicallysimilartokensdifferbyonlyonebitintheirbyte
representations. Thispreserveslocalityinbytesurfacesandslightlyimprovesperformance.
As shown in Table 5, these encoding strategies yield marginal improvements in downstream performance within the
token-bytesformat,andallunderperformdirecttoken-indexrepresentations.
PretokenizationSchemes. StandardBPEpipelinesfirstsegmentrawtextinto“words”viapre-tokenization(typically
regex-based),thenapplyiterativemergestoproducesubwords. Weexperimentedwithseveralpre-tokenizationschemes:
• Default: Standardregex-basedpre-tokenization(Radfordetal.,2019;OpenAI,2023;Daganetal.,2024).
• Line-separated: Pre-tokenizationallowstokenstospanmultiplewordswithinaline(Friedetal.,2023).
• SuperBPE:Extendedpre-tokenizationthatpermitsmergesacrosswhitespaceboundaries(Liuetal.,2025).
Line-separatedandSuperBPEpre-tokenizationimprovecompressionrates(2.3×and2.9×respectively,comparedto1.7×
fordefault),butdonotmatchtheperformanceofdirecttoken-indexrepresentations.
TokenizerAlgorithms. WealsocomparedUnigram-basedtokenization(Kudo,2018)andfoundnosignificantdifference
intransferperformanceatmatchedcompressionrates,suggestingthatthechoiceoftokenizationalgorithmsislesscritical.
B.2.NeuralProxyCompression
Thissectionprovidesimplementationdetailsforneuralproxycompression,includingthecompressorarchitecture,entropy-
based segmentation algorithm, and parallelization strategies. Table 6 summarizes ablation results across key design
choices.
CompressorModel. Ourneuralproxycompressorcombinesasmallbyte-levellanguagemodelwitharithmeticcoding.
Wetrain a ∼40M-parameter byte-level Transformeron ourpretraining corpus, with thedimension size 512, 12 layers,
18

ProxyCompressionforLanguageModeling
8 attention heads. Training uses a learning rate of 1e−3 for 200k steps with batch size 64×2048 bytes. The model
operatesoverafixedalphabetofsize256,andproducesconditionaldistributionsp(b | b )foreverybyteintheinput
t <t
x =(b ,...,b ). Thesedistributionsdrivethearithmeticcodertooutputacompressedbitstream.
raw 1 T
Entropy-based Segmentation. Naively compressing training data is prohibitively slow: (1) the arithmetic coder is
inherentlysequential,and(2)theequal-informationwindowschemeinLesteretal.(2024)requiresfrequenttermination
andcontexttruncation, triggeringnewforwardpassesforthelanguagemodeltoobtainnewprobabilities. Toincrease
parallelism,wepre-segmenttrainingsamplesandcompresseachsegmentindependently.
Weimplementanentropy-basedadaptivesegmentationstrategy: foreachinputexampleinUTF-8bytes,werunthemodel
forward pass to obtain per-position logits and compute the per-byte cross-entropy h := −logp (b ) for t = 1,...,L.
t t t
Segmentboundariesareconstructedwheretheentropyprofileindicateslowpredictabilitybasedontwocriteria:
1. Absoluteentropy: positionswhereh exceedsaglobalthreshold(e.g.,95thpercentile).
t
2. Entropyjumps: positionswherethefinitedifference∆h =h −h exceedsamonotonicitythreshold,indicating
t t t−1
suddenchangesinpredictability.
Similarentropy-basedcriteriaalsoappearinBLTs(Pagnonietal.,2024)fordynamicbytepatchificationwithinthemodel
architecture; here we use them only for segmenting inputs for parallel arithmetic coding. By default, we use the 95th
percentileasthethresholdforbothcriteria.
VectorizedArithmeticCoding. Weimplementabatchedarithmeticcodertoprocessmultiplesegmentsinparallelwith
equal-informationwindows(Lesteretal.,2024). Givenapredefinedbitthresholdτ,compressionproceedsiterativelyfor
eachsegment:
1. Runaforwardpassofthecompressormodeltoobtainnext-bytedistributions(onGPU).
2. Performarithmeticcodingandcountoutputbitsintheresultingcompressedbitstream(onCPU).Ifthebitstreamforthe
currentwindowexceedsτ bits,emitthefirstτ bits,discardtheconsumedbytecontext,andreturntostep1withthe
truncatedcontext.
WedesignapipelinedimplementationtooverlapGPUforwardpasseswithCPUencodingacrossiterations.
Caching. Weexploitsubstantialrepetitioninpre-trainingcorpuswithaglobalsegmentcache: beforecompressinga
segment,wecheckwhetheritexistsinthecache. Cachehitswillretrievethepre-computedcompressedbitstream,while
cachemisseswilltriggercompressionasusual. Cachingsignificantlyreducesredundantcomputationduringarithmetic
coding.
BitstreamPacking. Aftercompressingeachsegmenttoabitstream,wepackfixed-lengthbitchunksintodiscretesymbols.
WedefineabitwidthN andpackconsecutiveN-bitchunksfromthebitstreamintosymbols. Bydefault,N =16,which
yieldsavocabularysizeV =65,536forthelanguagemodelembeddingtable;weablatethisdesignchoiceinTable6.
End-to-EndPipeline. Thecompressorrunsfullyofflineinparallelviaamulti-processpipeline. Eachworker:
1. Readsashardofthecorpus.
2. Appliesentropy-basedsegmentation(onGPUs).
3. Compressessegmentswitharithmeticcoding,equal-infowindows(Lesteretal.,2024),andcachelookup(GPU/CPU
pipelining).
4. Packstheresultingcompressedbitstreamintofixed-bitsymbols.
5. Writessegmentationmetadataandcompressedsequences.
Attrainingtime,theproxycompressorsimplyreadsthepre-computedcompresseddataandpresentsthemtothemixed-
representation training pipeline (§2.1). Our pipeline design improves efficiency significantly: we process ∼3.3TB of
pretrainingdataat0.57GB/hourperprocess,comparedto0.005GB/hourforanaivefully-sequentialimplementation.
19

ProxyCompressionforLanguageModeling
Table6. Ablationstudyondesignchoicesofneuralproxycompressionwith1.5Bmodels. CompressorCRdenotesthecompression
rateoftheproxycompressorinisolation(i.e.,withoutmixingwithrawbytes). Pre-segmentationcontrolshowdocumentsaresplit
beforearithmeticcoding; EqualInfoACBitsspecifiesthetargetinformationpercodingwindow(Lesteretal.,2024); PackingBits
determineshowmanybitsaregroupedintoeachdiscretesymbol(V istheresultingvocabularysize).Thebottomrowshowsourfinal
configuration,whichachievesaneffectivecompressionrateofapproximately2.6underthemixed-representationtrainingschemewith
r=0.9(seeAppendixA).
Pre-segmentation EqualInfoACBits PackingBits CompressorCR Pass@1(%)
Fixed-length(size=4) None 8(V =256) 1.4 8.5
Fixed-length(size=8) None 8(V =256) 2.0 3.7
Fixed-length(size=16) None 8(V =256) 2.9 6.1
Lines None 8(V =256) 5.1 9.8
Lines 16 8(V =256) 2.3 11.6
Entropy(98thpercentile) 16 8(V =256) 1.8 13.4
Entropy(98thpercentile) 16 16(V =65536) 3.5 18.9
Entropy(95thpercentile) 32 16(V =65536) 4.1 12.2
Entropy(95thpercentile) 16 16(V =65536) 3.1 18.3
WhyNeuralCompressionCannotDecode. Unliketokenization,neuralcompressionisnotinvertibleandthusdoesnot
supportdecoding. Severalfactorscontributetothis: (i)probabilitytablesarenotstoredduringcompression,(ii)ouruseof
segmentationandequal-informationwindowing(Lesteretal.,2024)producecompressedsegmentsofvaryingbytelengths,
andtheseboundariesareunknownatdecodetime,and(iii)atinferencetime,whennewcompressedsymbolsarepredicted
bythelanguagemodelinsteadofproducedbythecompressor,theunderlyingcompressorprobabilitiesthatwouldbeneeded
fordecodingarebydefinitionunavailable. Thesefactorscausethesamecompressedsequencetocorrespondtomultiple
plausiblerawbytesequences,orthe“fuzziness”discussedin§2.3.
DesignChoiceAblations. Table6ablateskeydesignchoicesinourneuralcompression: segmentationstrategy,equal-
informationbitwindowsize,andsymbolpackinggranularity. Forsegmentation,weobservefixed-lengthsegmentation
performspoorly,likelyduetoabruptchangeswithsemantic-agnosticboundaries. Line-basedsegmentation(splittingat
newlines)workswellforcode,improvesresults,butremainsunsatisfactory. Entropy-basedsegmentationisgeneraland
yieldsthebestperformancebyplacingboundariesatnaturaltransitionpoints. Whenusingequal-infowindows(Lester
etal.,2024),itimprovesperformancebutdegradescompressionrates,aswindowresetsintroduceoverheadintermsof
compression. Wefind16-bitwindowsstrikethebestbalanceandincreasingto32bitsimprovescompressionratebutgreatly
degradesperformance. Forpacking,using16-bitpersymbolsubstantiallyoutperformsthe8-bitvariant. Inaddition,the
choicebetween95thand98thpercentileforthethresholdinentropysegmentationhasminimalimpactondownstream
performance. Overall,entropy-basedsegmentationwith16-bitequal-informationwindowsand16-bitsymbolpackingyields
thebesttrade-off.
C.AdditionalArchitectural,Training,andEvaluationDetails
C.1.ModelArchitectures
Figure10comparesEvaByte(Zhengetal.,2025b)againstOpenCoder(Huangetal.,2024a),aLlama-basedtransformer
architecture (Dubey et al., 2024). We reproduce OpenCoder 1.5B and 8B under our codebase; our reproductions in a
longertrainingrunmatchorexceedthereleasedintermediatecheckpointsonHumanEvalandMBPPbenchmarks. EvaByte
consistentlyachieveslowerBPBwhilematchingOpenCoder’sdownstreamperformanceatcomparablemodelsizes,where
bothmodelsoperateontokens. Givenitsfavorableefficiency–performancetrade-off(Zhengetal.,2023;2025b),weadopt
EvaByteasthedefaultarchitecturethroughoutthisstudy.FollowingEvaByte(Zhengetal.,2025b),weemploymulti-symbol
(over either tokens or bytes) prediction (Stern et al., 2018; Gloeckle et al., 2024; Cai et al., 2024; Zheng et al., 2025b;
Grivasetal.,2025)asthetrainingobjectiveabove4Bparameters,andstandardnext-symbolpredictionotherwise(enabling
multi-symbolpredictionforsmallermodelsleadstoslightlydegradedperformance,consistentwithGloeckleetal.(2024)).
Acrossdifferentmodels,forbyte-levelpredictions,weuse8predictionheads;fortoken-levelpredictionsfrom(proxy)
compressors,weuseeitherstandardnext-tokenpredictionor2-headmulti-tokenprediction(weconductedablationstudies
andfoundvaryingthenumberoftokenpredictionheadsdoesnotimprovedownstreamperformance,includingforourproxy
20

ProxyCompressionforLanguageModeling
|       | Validation Bits per Byte (BPB) |     |              |     |     |     |     | HumanEval Pass@1 |     |              |     |
| ----- | ------------------------------ | --- | ------------ | --- | --- | --- | --- | ---------------- | --- | ------------ | --- |
| 0.225 |                                |     | EvaByte-1.5B |     |     |     |     |                  |     | EvaByte-1.5B |     |
0.26
|     |     |     | EvaByte-7B |     |     |     |     |     |     | EvaByte-7B |     |
| --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | ---------- | --- |
0.220
| )BPB( etyB rep stiB |     |     | OpenCoder-1.5B |     |     | 0.24 |     |     |     | OpenCoder-1.5B |     |
| ------------------- | --- | --- | -------------- | --- | --- | ---- | --- | --- | --- | -------------- | --- |
|                     |     |     | OpenCoder-8B   |     |     |      |     |     |     | OpenCoder-8B   |     |
0.215
0.22
1@ssaP
0.210
0.20
0.205
0.18
0.200
| 0.195 |          |                     |       |     |     | 0.16 |     |                     |     |     |     |
| ----- | -------- | ------------------- | ----- | --- | --- | ---- | --- | ------------------- | --- | --- | --- |
| 0.190 |          |                     |       |     |     | 0.14 |     |                     |     |     |     |
|       | 20 30 40 | 50 60               | 70 80 | 90  | 100 |      | 20  | 40                  | 60  | 80  | 100 |
|       |          | Training Tokens (B) |       |     |     |      |     | Training Tokens (B) |     |     |     |
Figure10.AblationonmodelarchitectureonvalidationBPB(left)andHumanEvalpass@1(right).
Table7.Architecturalhyperparameters.VocabularysizesforEvaByteareomittedhereduetovaryinginputrepresentationsinourstudy.
|     |     |     | OpenCoder |     |     |     | EvaByte |     |     |     |     |
| --- | --- | --- | --------- | --- | --- | --- | ------- | --- | --- | --- | --- |
Hyperparameter
|     |                   |     | 1.5B  | 8B     | 0.5B   | 1.5B   | 4B     |        | 7B     | 14B |     |
| --- | ----------------- | --- | ----- | ------ | ------ | ------ | ------ | ------ | ------ | --- | --- |
|     | Layers            |     | 24    | 32     | 28     | 20     | 32     |        | 32     | 40  |     |
|     | ModelDimension    |     | 2240  | 4096   | 1024   | 2048   | 3072   | 4096   | 5120   |     |     |
|     | FFNDimension      |     | 6144  | 14336  | 4096   | 8192   | 9216   | 12288  | 16384  |     |     |
|     | AttentionHeads    |     | 14    | 32     | 8      | 16     | 24     |        | 32     | 40  |     |
|     | Key/ValueHeads    |     | 14    | 8      | 8      | 16     | 24     |        | 32     | 40  |     |
|     | VocabSize         |     | 96640 | 96640  | -      | -      |        | -      | -      | -   |     |
|     | RoPEθ             |     | 10000 | 500000 | 100000 | 100000 | 100000 | 100000 | 100000 |     |     |
|     | ContextWindowSize |     | 4096  | 4096   | 16384  | 16384  | 16384  | 16384  | 16384  |     |     |
models,whichultimatelyoperateonrawbytesatinference). Specificationsonthenumberoftoken-orbyte-prediction
headsaremadetoroughlymatchpredictiongranularityacrossrepresentations,giventhatbothtokenizerandneuralproxy
compressorsachievecompressionratesabove3×,althoughwefounditdoesnotleadtoperformanceimprovementsover
otherconfigurations.
C.2.TrainingConfiguration
Table8. Learningratesfordifferentinputrepresentationsanddifferentmodelsizes. Allvaluesarepeaklearningratesofthetraining
schedule.
|     |     | Variant          |     | 0.5B   | 1.5B | 4B   | 7B   | 14B  |     |     |     |
| --- | --- | ---------------- | --- | ------ | ---- | ---- | ---- | ---- | --- | --- | --- |
|     |     | Tokenizer        |     | 1.2e−3 | 9e−4 | 7e−4 | 5e−4 | 5e−4 |     |     |     |
|     |     | Byte-level       |     | 1.2e−3 | 9e−4 | 7e−4 | 5e−4 | 3e−4 |     |     |     |
|     |     | Proxy(Neural)    |     | 1.2e−3 | 9e−4 | 3e−4 | 5e−4 | 3e−4 |     |     |     |
|     |     | Proxy(Tokenizer) |     | 1.2e−3 | 9e−4 | 7e−4 | 5e−4 | 3e−4 |     |     |     |
ModelparametersareinitializedfromatruncatedNormaldistributionwithstandarddeviation0.02,exceptforembedding
parameters (with standard deviation 1.0). Gradient norms are clipped to 1.0. We use AdamW (Kingma & Ba, 2014;
Loshchilov&Hutter,2019)withweightdecay0.1,β = 0.9,β = 0.95,andϵ = 1e−15,followingpriorpracticeson
|     |     |     |     |     | 1   | 2   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
stablelarge-scaletraining(Molybogetal.,2023;Wortsmanetal.,2023;OLMoTeametal.,2025;Zhengetal.,2025b).
Table8reportspeaklearningratesfordifferentinputrepresentationsandmodelsizes. Foreachconfiguration,weperforma
moderatelearningratesweepwhilekeepingthebatchsizefixed,startingfromcommonvaluesandadjustinguntilobserving
eithertraininginstabilityorvalidationlossdegradation.
21

ProxyCompressionforLanguageModeling
For models trained on the Python subset, we use a fixed effective batch size of 2M sequence symbols, independent of
whethertheinputsarerepresentedastokens,bytes,orothercompressedformats. Asaresult,modelswithdifferentinput
representationsconsumedifferentamountsofrawdataperbatch. Thesemodelsaretrainedfor50000stepswithacosine
learning-rateschedule,wherethelearningrateislinearlywarmedupforthefirst500stepsandthendecayeddownto10%of
itspeakvalue. FormodelstrainedonthefullGitHubcorpus(Table2),weincreasethebatchsizeto4Msequencesymbols
for80000trainingstepsanduseaconstantlearningrateschedulewith2000-steplinearwarm-up. Allothersettingsremain
unchanged.
C.3.EvaluationProtocols
Weprimarilyfocusondownstreamcodegenerationtasksforevaluationandreportpass@kratesfollowingChenetal.(2021),
whichestimatetheprobabilityofamodelgeneratingacorrectsolutionwithinkattempts. Weevaluateonwell-established
codegenerationbenchmarks,includingHumanEval(Chenetal.,2021),MBPP(Austinetal.,2021),andtheirEvalPlus
variants(Liuetal.,2023). Pass@1iscalculatedviagreedydecoding,andpass@10draws20samplesattemperature0.2
usingnucleussampling(Holtzmanetal.,2020)withtop-p=0.95. Toacceleratedecoding,wecapthemaximumnumberof
generatedtokensto512fortokenizer-basedbaselinesand2048forotherinputformats. WealsomeasureBits-Per-Byte
(BPB)forrepresentation-agnosticcomparisonofmodelingquality(Raeetal.,2020;Xueetal.,2022;Yuetal.,2023;Huang
etal.,2024b;Xuyangetal.,2025),computedon40Kheld-outsamples(∼150Mbytes)fromSwallowCode(Fujiietal.,
2025).
NoteonBPBEvaluation. WefocusondownstreamtaskperformanceratherthanvalidationBPBinthiswork. Validation
BPBisknowntobebiasedwhencomparingacrossdifferentdatarepresentations(Vieiraetal.,2024;Hwangetal.,2025),
andthisbiasisamplifiedinoursettingwheretraininginvolvestokensfromdifferentcompressors,rawbytes,andtheir
mixtures. Empirically,weobservethatmodelstrainedwithmulti-symbolpredictionobjectives(whetherovertokensor
bytes)oftenachievebetterdownstreamcodegenerationbutworseBPB,likelybecausetheirtrainingobjectivedivergesfrom
next-symbollikelihood. Similarly,proxy-trainedmodelsexhibitworseBPBwhenevaluatedoneithercompressedorraw
representationsalone,despitesuperiordownstreamperformance. Thisisexpectedasattrainingtime,themodelmustnot
onlypredictnextsymbolswithineachrepresentation,butalsoalignacrossrepresentationstoachievetransfer,whichgoes
beyondstandardnext-symbolprediction. Wethereforerelyondownstreambenchmarksasourprimarymetric,whichwe
findyieldsreliablesignalsacrossmodelsandscales.
D.AdditionalExperimentalResultsandAnlayses
D.1.FullResultsofDownstreamTransfer
WelistdownstreamperformanceforbothHumanEvalandMBPPaswellastheirEvalPlusvariantsforcompleteness,as
showninTables9and10.
D.2.AdditionalAnalysesofIn-contextTransfer
Following§3.3,weprovideadditionalexperimentaldetailsandanalysesforin-contexttransferprobingundercontrolled
supervision. Weconsiderthefollowingmixed-representationpromptforevaluation,
(cid:2) (cid:3)
⟨comp⟩◦p ◦s ◦⟨/comp⟩◦⟨raw⟩◦p .
comp comp raw
Notethatthisisonlyapplicabletotokenizer-basedproxies. Weevaluatebothtokenizer-basedandneuralcompressors
at1.5Band7Bmodels,trackingoracle-translationpass@1atintermediatetrainingsteps(10k,20k,30k,40k,and50k).
Asdescribedin§2.1,weoptionallytransformtraininginputsintoexplicittranslationpairsbyincludingbothcompressed
andrawviewsofthesamedatainthesamecontext. Tostudyhowin-contexttransferstrengthdependsonthispairing
schedule,weconsiderthreevariantsthatsharethesameoverallratior = 0.9ofcompressedsamplesanddifferonlyin
whetherthosesamplesarepaired: (1)Nopairs,wheretrainingexamplesareindependentlysampledintoeithercompressed
orrawformwithoutanypaireddata;(2)Warmup-only,wherethefirst10kstepsusetranslationpairsandlaterstepsswitch
toindependentsampling;and(3)Always-on,wheretranslationpairsarepresentthroughouttraining. Weidentifytwokey
findingsfromtheextendedin-contexttransferexperiments.
22

ProxyCompressionforLanguageModeling
Table9.Downstreampass@1performanceonHumanEval(-Plus)andMBPP(-Plus)acrossdifferentmodelsizesandinputrepresentations.
ModelSize
| Task |     | Model           | CompressionRate |     |           |           |      |
| ---- | --- | --------------- | --------------- | --- | --------- | --------- | ---- |
|      |     |                 |                 |     | 0.5B 1.5B | 4B 7B     | 14B  |
|      |     | Tokenizer-based |                 | 3.7 | 21.3 21.3 | 33.5 32.9 | 34.1 |
|      |     | Byte-level      |                 | 1.0 | 17.7 21.3 | 26.8 26.2 | 27.4 |
HumanEval
|     |     | Proxy(Neural)    |     | 2.6 | 15.2 21.3 | 26.2 30.5 | 32.9 |
| --- | --- | ---------------- | --- | --- | --------- | --------- | ---- |
|     |     | Proxy(Tokenizer) |     | 2.9 | 13.4 23.8 | 29.3 32.9 | 34.8 |
|     |     | Tokenizer-based  |     | 3.7 | 17.7 18.3 | 28.0 28.7 | 29.3 |
|     |     | Byte-level       |     | 1.0 | 15.9 18.3 | 22.0 23.8 | 24.4 |
HumanEval-Plus
|     |     | Proxy(Neural)    |     | 2.6 | 13.4 18.3 | 22.6 26.8 | 29.9 |
| --- | --- | ---------------- | --- | --- | --------- | --------- | ---- |
|     |     | Proxy(Tokenizer) |     | 2.9 | 12.2 20.7 | 24.4 26.2 | 30.5 |
|     |     | Tokenizer-based  |     | 3.7 | 37.8 47.9 | 57.1 54.8 | 59.8 |
|     |     | Byte-level       |     | 1.0 | 31.7 42.1 | 51.1 50.0 | 52.6 |
MBPP
|     |     | Proxy(Neural)    |     | 2.6 | 27.5 37.3 | 50.8 50.0 | 58.7 |
| --- | --- | ---------------- | --- | --- | --------- | --------- | ---- |
|     |     | Proxy(Tokenizer) |     | 2.9 | 30.7 46.0 | 54.2 56.3 | 58.2 |
|     |     | Tokenizer-based  |     | 3.7 | 29.4 41.0 | 46.3 45.2 | 48.1 |
|     |     | Byte-level       |     | 1.0 | 25.9 33.6 | 41.8 41.3 | 42.1 |
MBPP-Plus
|     |     | Proxy(Neural)    |     | 2.6 | 22.0 29.6 | 41.8 41.8 | 49.2 |
| --- | --- | ---------------- | --- | --- | --------- | --------- | ---- |
|     |     | Proxy(Tokenizer) |     | 2.9 | 25.4 38.4 | 44.4 45.5 | 49.5 |
Table10.Downstreampass@1performanceonHumanEval(-Plus)andMBPP(-Plus)aftertraining320BtokensonthefullRefineCode
GitHubcorpus.
#Parameters Model CompressionRate HumanEval HumanEval-Plus MBPP MBPP-Plus
|     | Tokenizer-based |     | 3.7 | 19.5 | 17.1 | 33.9 | 28.0 |
| --- | --------------- | --- | --- | ---- | ---- | ---- | ---- |
|     | Byte-level      |     | 1.0 | 11.6 | 9.1  | 31.0 | 23.3 |
1.5B
|     | Proxy(Neural)    |     | 2.6 | 15.2 | 14.0 | 29.4 | 24.1 |
| --- | ---------------- | --- | --- | ---- | ---- | ---- | ---- |
|     | Proxy(Tokenizer) |     | 2.9 | 14.6 | 12.8 | 32.8 | 25.1 |
|     | Tokenizer-based  |     | 3.7 | 25.6 | 21.3 | 42.6 | 36.0 |
|     | Byte-level       |     | 1.0 | 18.3 | 14.6 | 41.5 | 32.5 |
7B
|     | Proxy(Neural)    |     | 2.6 | 25.0 | 21.3 | 45.2 | 36.0 |
| --- | ---------------- | --- | --- | ---- | ---- | ---- | ---- |
|     | Proxy(Tokenizer) |     | 2.9 | 23.2 | 22.0 | 43.4 | 34.9 |
Structuraldifferencesinproxycompressiondrivetransferstability. AsshowninTable3,underWarmup-only,the
tokenizer proxy drops after warmup but partially recovers (1.5B: 90.9%→31.1%→45.7%), while neural proxy decays
more severely (1.5B: 90.9%→14.6%→38.4%), reflecting the structural properties of the two proxy compression types
(Figure4). Tokenizer-basedcompressionusesaglobalstaticvocabularywheretokenIDsmapconsistentlytobytepatterns
across the corpus, providing a stable anchor even without explicit supervision. Neural compression, in addition to its
structuredfuzziness(§3.4),producescontext-dependentsymbolsthatlackafixedglobalmapping,wherethesamepattern
mayyielddifferentcompressedsequencesdependingonlocalcontext. Thispotentiallyexplainswhy,underALWAYS-ON,
bothproxycompressorsreachveryhightranslationpass@1(themodelcanalwaysrelyontheexplicittranslationpairing);
whereasunderWARMUP-ONLY,onceexplicitpairsdisappear,neuralproxiesdecayfasterthantokenizer-basedcounterparts
oracle-translationpass@1.
Largermodelsdonotsubstituteforexplicitpairing. Figure11visualizesthetrainingdynamicsforneuralcompression
at1.5Band7Bmodels. UnderWarmup-only,both1.5Band7Bmodelsexhibitrapiddecayinoracle-translationaccuracy
oncetranslationpairsareremoved,despite7Bretainingslightlyhigheraccuracyatintermediatesteps(e.g.,73.8%vs.39.0%
at20k). Thissuggeststhatin-contexttranslationisfundamentallydependentonexplicitpairingsupervision: largermodels
donotinternalizethesuperficialmappingmorerobustly,theysimplystartfromamarginallybetterinitialalignment. Once
pairingisremoved,thelanguagemodelingobjectivenolongerconstrainssurface-leveltranslation,andbothscalesconverge
towardsimilardegradedperformance. Incontrast,underAlways-on,both1.5Band7Bmaintainnear-perfecttranslation
23

ProxyCompressionforLanguageModeling
1
0,8
0,6
0,4
0,2
0
10k 20k 30k 40k 50k
Trainingsteps
1@ssapnoitalsnartelcarO
1.5BALWAYS-ON
7BALWAYS-ON
1.5BWARMUP-ONLY
7BWARMUP-ONLY
Figure11.Oracletranslationpass@1onneuralproxycompression.Solidlinesrepresentcontinualtranslationpairs(ALWAYS-ON),while
dashedlinesindicateabruptremovalafter10ksteps(WARMUP-ONLY).
25000
20000
15000
10000
5000
0
0.0 0.2 0.4 0.6 0.8 1.0
LCP ratio
slobmys
desserpmoC
Figure12.DistributionoftheLCPratioacrossallcompressedsymbolsthatexhibitcollisions.Thedistributionisheavilyskewedtowards
highsimilarity(LCPratio>0.8),showingthatcollisionstypicallydifferonlyinshortsuffixes.
(>94%)throughouttraining,confirmingthatasmallfractionofexplicitpairsisbothnecessaryandsufficientforreliable
in-contexttransfer.
D.3.AdditionalResultsofNeuralProxyCompression
Weprovideadditionalanalysisofthecollisionbehaviorinducedbytheneuralcompressor,complementingthemainresults
in§3.4.
LCPRatioDistribution. Toquantifysimilarityamongcollidingchunks,wecomputethelongestcommonprefix(LCP)
ratio: thelengthofthesharedprefixdividedbyaveragechunklength. Figure12showsthatover90%ofcollisionshave
LCPratiosabove0.8,meaningcollidingchunksarenearlyidenticalexceptforshortsuffixes. Thisconfirmsthatneural
compressioninducesstructuredratherthanarbitraryambiguity.
RepresentativeCollisionCases. Table11presentsstatisticsforfourrepresentativecollisionclusters,andListing1shows
qualitativeexamples. Eveninthelargestcluster(Case1,61variants),nearlyallvariantsdifferonlybytrailingwhitespace
andindentation. Cases5–7illustratecommonpatterns: URLsuffixes,if name boilerplatewithvaryingcompletions,
24

ProxyCompressionforLanguageModeling
Table11.Statisticsoffourrepresentativecollisionclustersinducedbytheneuralcompressor.
|     |     | Case           |     | #Variants LCPRatio | Length(mean) | Std   |
| --- | --- | -------------- | --- | ------------------ | ------------ | ----- |
|     |     | 1.Maximumscale |     | 61 0.49            | 59.00        | 17.60 |
|     |     | 2.Minimumscale |     | 2 0.56             | 64.00        | 28.00 |
|     |     | 3.HighestLCP   |     | 2 0.87             | 7.50         | 0.50  |
|     |     | 4.LowestLCP    |     | 4 0.00             | 10.00        | 8.15  |
andfunctioncallswithformattingdifferences. Theseexamplesdemonstratethatneuralcompressionmergessemantically
equivalentcontentwhileabstractingawaysuperficialformattingnoise.
Listing1.Collisionexamplesfromtheneuralcompressor.
| Case 1: | Maximum scale | (61 variants, |     | 4 shown) |     |     |
| ------- | ------------- | ------------- | --- | -------- | --- | --- |
[,\n ]
| [,\n    |               |              | ]   |     |     |     |
| ------- | ------------- | ------------ | --- | --- | --- | --- |
| [,\n    |               |              |     | ]   |     |     |
| [,\n    |               |              |     |     | ]   |     |
| Case 2: | Minimum scale | (2 variants) |     |     |     |     |
[acc,\n ]
| [acc,\n   |                  |              |           | ]   |     |     |
| --------- | ---------------- | ------------ | --------- | --- | --- | --- |
| Case 3:   | Highest LCP      | ratio (2     | variants) |     |     |     |
| [True\n\n | ]                |              |           |     |     |     |
| [True\n\n | ]                |              |           |     |     |     |
| Case 4:   | Lowest LCP ratio | (4 variants) |           |     |     |     |
[ }]
| [ }\n |     | ]   |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- |
[!]
| [ }\n       | ]                    |              |                           |     |     |     |
| ----------- | -------------------- | ------------ | ------------------------- | --- | --- | --- |
| Case 5:     | URL suffixes         | (4 variants) |                           |     |     |     |
| [ = 1)\n\n# | + colab={]           |              |                           |     |     |     |
| [ = 1)\n\n# | + colab={"base_uri": |              | "https://localhost:8080/] |     |     |     |
[ = 1)\n\n# + colab={"base_uri": "https://localhost:8080/", "height": ]
| [ = 1)\n\n#    | + colab]      |             |     |           |     |     |
| -------------- | ------------- | ----------- | --- | --------- | --- | --- |
| Case 6:        | Main function | boilerplate | (11 | variants) |     |     |
| [\nif __name__ | == ’_"]       |             |     |           |     |     |
[\nif __n]
| [\nif __name__ | == ’__main]    |     |     |     |     |     |
| -------------- | -------------- | --- | --- | --- | --- | --- |
| [\nif __name__ | == ’__main__’] |     |     |     |     |     |
[\nif __]
[\nif _]
| [\nif __name__ | ]       |     |     |     |     |     |
| -------------- | ------- | --- | --- | --- | --- | --- |
| [\nif __name__ | =]      |     |     |     |     |     |
| [\nif __name__ | == ’__] |     |     |     |     |     |
[\nif __na]
[\nif __name__]
| Case 7:      | Function call | formatting | (4  | variants) |     |     |
| ------------ | ------------- | ---------- | --- | --------- | --- | --- |
| [process()\n |               | ]          |     |           |     |     |
| [process(\n  | ]             |            |     |           |     |     |
| [process()\n | ]             |            |     |           |     |     |
| [process(\n  | ]             |            |     |           |     |     |
D.4.AdditionalResultsofRobustnessEvaluationonReCode
EvaluationMetrics. WeevaluaterobustnessontheHumanEvalsplitoftheReCodebenchmark(Wangetal.,2023),
which applies naturally occurring, semantics-preserving perturbations to coding problems. Following ReCode (Wang
25

ProxyCompressionforLanguageModeling
0,33
0,3 0,29
0,2
0,2 0,15
0,1
0
Toke P n P r B i r o z o y x e x t y r y e- ( ( l T e T o v o k e k e l e n n i i z z e e r P r - ) t r o o k x e y ns ( N ) eural)
PR
0,6
0,53
0,4
0,21 0,2
0 0
−0,02
−0,09
Token P P i B r z r o o e y x x r t y e y - ( l ( T e T v o o e k k l e e n n i i z z e e r r - P ) t r o o k x e y ns ( ) Neural)
(a)RP(↑)
DR
0,55
0,53
0,5
0,45 0,44 0,43
0,4 0,4 0,39
0,35
Toke P n P r B i r o z o y x e x t y r y e- ( ( l T e T o v o k e k e l e n n i i z z e e r P r - ) t r o o k x e y ns ( N ) eural)
(b)RD(↓)
RR
(c)RR(↓)
Figure13.Formatperturbations.
et al., 2023), we consider four perturbation families: function name rewrites (Function), formatting changes (Format),
syntacticrewrites(Syntax),anddocstringparaphrases(Docstrings). Wereportthenominalpassratewherenoperturbations
areapplied. Wemeasurerobustnessbasedonthreemetrics: RobustPassRP @k,measuringworst-casepass@k under
s
svariantsofthesameproblem. Usingthestandardpass@k estimatorwithnsamples, robustpassratesaredefinedas
RP s @k =E x (cid:2) 1− (cid:0)n−r k c s(x)(cid:1) / (cid:0)n k (cid:1)(cid:3) ,wherer c s(x)countsgenerationsthatpassallsvariants(Wangetal.,2023). Intuitively,
RPmeasurestheworse-casepassrateswhereaproblemissolvedonlywhenthesolutionremainscorrectnomatterhow
thepromptisperturbed(higherisbetter). RobustDropRD @k = (pass@k−RP @k)/pass@k measurestherelative
s s
degradationfromnominaltoworse-caseperformance(lowerisbetter;negativevaluesindicategainsunderperturbations).
RobustRelative(fliprate)RR @kcapturesstability: theproportionofsampleswhosecorrectnessflipsbetweenthenominal
s
andperturbedinputs(lowerisbetter).
ForeachoriginalprobleminHumanEval(Chenetal.,2021),ReCodeprovidess=5randomlyperturbedvariantsforeach
perturbationtype. Werungreedydecodingandwithn = 1sampleandk = 1. Wethusrefertotheresultingquantities
simplyasRP,RD,andRR.
Models. Wecompareourproxy-trainedmodelsagainstthetokenizer-basedandbyte-levelbaselinesat7Bparameters,
usingthesamecheckpointsasinTable1. Tomoreextensivelyevaluatetherobustness,weadditionallyevaluatetokenizer-
proxy-trainedmodelsbyrunninginferenceontokens,denotedbyProxy(Tokenizer-tokens).
Per-Family Analysis. We visualize RP, RD, and RR for each perturbation family. Format perturbations (Figure 13)
exhibitthelargestgapbetweenrepresentations. Thetokenizerbaselinesuffersseveredegradation,whilebyte-leveland
proxymodelsremainstableorevenimprove. Thisindicatesthatpartialexposuretorawbytesduringtrainingsufficesto
improvemodelrobustnessagainstsurface-levelformattingnoise. WealsovisualizeresultsforFunctionperturbations
(Figure14),Syntaxperturbations(Figure15),andDocstringperturbations(Figure16).
D.5.AdditionalAnalysesonDataRepresentations
Whiletokenizationremainsthedominantapproachfortransformingrawinputsintodiscreteunitsforlanguagemodels,we
systematicallyinvestigateaspectrumofinputrepresentationsrangingfromBPEtokensdowntoindividualbits. Specifically,
weconsiderBPEtokens,double-bytes(16-bit),bytes(8-bit),half-bytes(4-bit),double-bits(2-bit),andbits(1-bit),training
modelswithmatchedparametercountsandtrainingFLOPsacrossallrepresentations.
Figure17revealstwocomplementarytrends. Underafixedcomputebudget,representationsthatprocessmoredataper
FLOPachievelowervalidationBPB,indicatingsuperiorcomputeefficiency. Conversely,underafixeddatabudget(right),
lower-levelrepresentationsgenerallyoutperformhigher-levelones,reflectingbetterdataefficiency,consistentwithprior
findings on byte-level models (Xue et al., 2022; Zheng et al., 2025b). However, this trend does not extrapolate to the
finestgranularities: 2-bitand1-bitmodelsconsistentlyunderperformacrossbothregimes. Thissuggeststhatexcessively
26

ProxyCompressionforLanguageModeling
0,2 0,21 0,2
0,2 0,18 0,19
0,1
0
Toke P n P r B i r o z o y x e x t y r y e- ( ( l T e T o v o k e k e l e n n i i z z e e r P r - ) t r o o k x e y ns ( N ) eural)
PR
0,44
0,4 0,38 0,35 0,34
0,23
0,2
0
Toke P n P r B i r o z o y x e x t y r y e- ( ( l T e T o v o k e k e l e n n i i z z e e r P r - ) t r o o k x e y ns ( N ) eural)
(a)RP(↑)
DR
0,3 0,27
0,23 0,24 0,21
0,2
0,11
0,1
0
Toke P n P r B i r o z o y x e x t y r y e- ( ( l T e T o v o k e k e l e n n i i z z e e r P r - ) t r o o k x e y ns ( N ) eural)
(b)RD(↓)
RR
(c)RR(↓)
Figure14.Functionperturbations.
0,14 0,14
0,13
0,13
0,12
0,12
0,11
0,1
Toke P n P r B i r o z o y x e x t y r y e- ( ( l T e T o v o k e k e l e n n i i z z e e r P r - ) t r o o k x e y ns ( N ) eural)
PR
0,65 0,63
0,6 0,58 0,58 0,59
0,55
0,53
0,5
Toke P n P r B i r o z o y x e x t y r y e- ( ( l T e T o v o k e k e l e n n i i z z e e r P r - ) t r o o k x e y ns ( N ) eural)
(a)RP(↑)
DR
0,6
0,54 0,5 0,5 0,51
0,5
0,4
0,3
0,22
0,2
Toke P n P r B i r o z o y x e x t y r y e- ( ( l T e T o v o k e k e l e n n i i z z e e r P r - ) t r o o k x e y ns ( N ) eural)
(b)RD(↓)
RR
(c)RR(↓)
Figure15.Syntaxperturbations.
fine-grainedrepresentationswastecomputegreatlyandlacksufficientabstractionforeffectivelearning,evenwhengranted
additionaltrainingstepsordata. Weobserveconsistenttrendsinlongertrainingruns(AppendixD.7). Thesefindings
motivaterepresentationsthatbalanceabstractionwithgranularity,ratherthanpursuingeitherextreme.
D.6.OnDocument-boundaryAttentionMasking
Inproxycompressiontraining,multiplesamplespotentiallyunderdifferentrepresentationsareconcatenatedandpacked
into fixed-length contexts, following standard language model training practice. This raises a natural question: does
cross-representationtransferarisefromin-contextattentionbetweensamplesofdifferentrepresentations,orfromshared
modelparameters?
Toisolatethis,wecomparetwosettings: (1)standardpacking,wheresampleswithinacontextcanattendtoeachother,and
(2)document-boundaryattentionmasking,whichrestrictsattentiontowithin-documenttokensonly. AsshowninFigure18,
weobserveperformanceimprovementswhenpreventingcross-documentattention. Thissuggeststhatcross-representation
transferstemsprimarilyfromsharedparametersratherthanin-contextinteractionsbetweenrepresentations. Following
recentworkdemonstratingbenefitsofdocument-boundarymaskingfortraining(Zhuetal.,2025),weenableitbydefaultin
allotherexperimentsunlessotherwisespecified.
D.7.AdditionalResultsonDataEfficiencyversusComputeEfficiency
Inthemaintext(§3.2),weshowedthatproxycompressioncapturesthebestofbothdataefficiencyandcomputeefficiency
for14Bmodels(Figure3). Hereweprovideextendedanalysisacrossmodelscalesandtraininghorizons.
27

ProxyCompressionforLanguageModeling
|     | 0,2 |     |     |     |     |     |     |     |     | 0,4 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0,6 0,57
|     |     |     |     |     |     |     | 0,55 |     |     |     | 0,36 |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | ---- | --- |
0,35
|     | 0,18 |     |     | 0,18 |     |     |     |      |     |     |     | 0,33 |
| --- | ---- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | ---- |
|     |      |     |     |      |     | 0,5 |     | 0,49 |     |     |     |      |
| PR  |      |     |     |      | DR  |     |     |      | RR  |     |     |      |
0,3 0,3
|     |      |      | 0,16 |     |     |     |      |      |     | 0,3 |     |     |
| --- | ---- | ---- | ---- | --- | --- | --- | ---- | ---- | --- | --- | --- | --- |
|     | 0,16 |      |      |     |     |     | 0,42 |      |     |     |     |     |
|     |      | 0,15 | 0,15 |     |     |     |      |      |     |     |     |     |
|     |      |      |      |     |     | 0,4 |      | 0,38 |     |     |     |     |
0,25
|     |     | 0,14 |     |     |     |     |     |     |     | 0,25 |     |     |
| --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
0,14
r e l r ) ns ) eural) r e l r ) ns ) eural) r e l s ) ns ) eural)
|     | i z e | e v | z e e |     |     | i z e e v | z e e |     |     | i z e | e v | y t e e |
| --- | ----- | --- | ----- | --- | --- | --------- | ----- | --- | --- | ----- | --- | ------- |
Toke n e- l e n i o k N Toke n e- l e n i o k N e n e - l - b o k N
|     | B y | t o k    | r - t (   |     |     | B y t o k | r - t     | (   |     | o k B y | t e r    | r - t (   |
| --- | --- | -------- | --------- | --- | --- | --------- | --------- | --- | --- | ------- | -------- | --------- |
|     |     | ( T      | i z e x y |     |     | ( T       | i z e x y |     | T   |         | n i z    | i z e x y |
|     |     | x y e    | n P r o   |     |     | x y       | e n P r o |     |     |         | k e e n  | P r o     |
|     | r o | o k      |           |     |     | r o o k   |           |     |     | T o     | o k      |           |
|     | P   | ( T      |           |     |     | P ( T     |           |     |     | y (     | ( T      |           |
|     | x   | y        |           |     |     | x y       |           |     | ro  | x x     | y        |           |
|     | r o |          |           |     |     | r o       |           |     | P   | r o     |          |           |
|     | P   |          |           |     |     | P         |           |     |     | P       |          |           |
|     |     | (a)RP(↑) |           |     |     | (b)RD(↓)  |           |     |     |         | (c)RR(↓) |           |
Figure16.Docstringperturbations.
)BPB( etyB-rep-stiB noitadilaV Tokenizer (BPE) )BPB( etyB-rep-stiB noitadilaV Tokenizer (BPE)
|     | 0.45 |     |                      | Double-byte (16-bit) |     |      | 0.45 |     |     |                    |     | Double-byte (16-bit) |
| --- | ---- | --- | -------------------- | -------------------- | --- | ---- | ---- | --- | --- | ------------------ | --- | -------------------- |
|     |      |     |                      | Byte (8-bit)         |     |      |      |     |     |                    |     | Byte (8-bit)         |
|     |      |     |                      | Halfbyte (4-bit)     |     |      |      |     |     |                    |     | Halfbyte (4-bit)     |
|     | 0.40 |     |                      |                      |     |      | 0.40 |     |     |                    |     |                      |
|     |      |     |                      | Double-bit (2-bit)   |     |      |      |     |     |                    |     | Double-bit (2-bit)   |
|     |      |     |                      | Bit (1-bit)          |     |      |      |     |     |                    |     | Bit (1-bit)          |
|     | 0.35 |     |                      |                      |     |      | 0.35 |     |     |                    |     |                      |
|     | 0.30 |     |                      |                      |     |      | 0.30 |     |     |                    |     |                      |
|     | 0.25 |     |                      |                      |     |      | 0.25 |     |     |                    |     |                      |
|     | 0.20 |     |                      |                      |     |      | 0.20 |     |     |                    |     |                      |
|     |      | 0.5 | 1.0                  |                      | 1.5 | 2.0  |      | 0   | 50  |                    | 100 | 150                  |
|     |      |     | Total Training FLOPs |                      |     | 1e21 |      |     |     | Training Bytes (B) |     |                      |
Figure17. ValidationBPBperformanceofdifferentdatarepresentationsspanningtokenstobits, underFLOPs-matched(left)and
data-matched(right)comparison.
Scaling Behavior. Figures 19 to 22 visualize performance under matched FLOPs (left) and matched data (right) for
modelsat0.5B,1.5B,4B,and7Bparameters. Atsmallerscales(0.5B),proxy-trainedmodelsunderperformbaselinesin
bothregimes;however,asmodelsizeincreases,proxycompressionbecomesprogressivelymorecompetitive,eventually
achievingthebestofbothregimesat14Bscale(Figure3). Thissupportsourhypothesisthatlargermodelshavegreater
capacitytolearncross-representationalignmentforeffectivetransfer.
Longer Training Horizons. We also examine whether the conventional wisdom, where byte-level models are more
data-efficient,tokenizer-basedmodelsaremorecompute-efficient,holdsunderdifferenttrainingschedules. Figures23
and24plotperformanceoverlongertrainingrunsfor1.5Band7Bmodels,respectively. Notably,byte-levelmodelsdonot
consistentlyoutperformtokenizer-basedmodelsundermatcheddatainthisregime. Thissuggeststhatthedata-efficiency
advantage of byte-level training might diminish given sufficient training data: the additional compute spent per byte
yieldsdiminishingreturns,andcompressionremainsbeneficialforlong-horizontrainingschedules. However,ourproxy
compressiontrainingstillpreservesthetrendasobservedin§3.2.
RelatedObservations. Ourfindingsalignwithpriorworkonthenuancedrelationshipbetweencompressionrateand
performance. SuperBPE(Liuetal.,2025)foundthathighercompressionratesdonotnecessarilyimproveperformance
despiteconsumingmoredataperstep,althoughthetrade-offbetweentheeffectivecontextsizeandtrainingsteps.4 Possible
explanations include: (i) higher compression produces harder tokens for the model to learn and predict; or (ii) lower
4Seehttps://superbpe.github.io/faq.html#context_adjustmentformoredetails.
28

ProxyCompressionforLanguageModeling
|     | 0.18 | Proxy (Tokenizer) w/ Doc Mask |     |     |     |     |
| --- | ---- | ----------------------------- | --- | --- | --- | --- |
Proxy (Tokenizer) w/o Doc Mask
1@ssaP sulP-lavEnamuH
0.16
Tokenizer-based w/ Doc Mask
Tokenizer-based w/o Doc Mask
0.14
0.12
0.10
0.08
0.06
0.04
|     | 20  | 40  | 60 80 | 100 |     |     |
| --- | --- | --- | ----- | --- | --- | --- |
Training Bytes (B)
Figure18.Ablationondocument-boundaryattentionmasking.
| 0.18 |     |     | 0.18 |     |     |     |
| ---- | --- | --- | ---- | --- | --- | --- |
Byte-level
| 0.16 Proxy Compressor (Neural) |     |     | 0.16 |     |     |     |
| ------------------------------ | --- | --- | ---- | --- | --- | --- |
Proxy Compressor (Tokenizer)
| 0.14 Tokenizer-based |     |     | 0.14   |     |     |     |
| -------------------- | --- | --- | ------ | --- | --- | --- |
| 0.12                 |     |     | 0.12   |     |     |     |
| 1@ssaP               |     |     | 1@ssaP |     |     |     |
| 0.10                 |     |     | 0.10   |     |     |     |
| 0.08                 |     |     | 0.08   |     |     |     |
Byte-level
| 0.06 |     |     | 0.06 |     |     |     |
| ---- | --- | --- | ---- | --- | --- | --- |
Proxy Compressor (Neural)
| 0.04 |     |     | 0.04 | Proxy Compressor (Tokenizer) |     |     |
| ---- | --- | --- | ---- | ---------------------------- | --- | --- |
Tokenizer-based
| 0.02 |     |     | 0.02   |         |         |     |
| ---- | --- | --- | ------ | ------- | ------- | --- |
| 1 2  | 3 4 | 5 6 | 50 100 | 150 200 | 250 300 | 350 |
1e20
| Total Training FLOPs |     |     |     | Training Bytes (B) |     |     |
| -------------------- | --- | --- | --- | ------------------ | --- | --- |
Figure19.Pass@1performanceonHumanEval-Plusfor0.5Bmodelsunderdifferentinputrepresentations,comparedasafunctionof
trainingFLOPs(left)andamountoftrainingdata(right).
compressionyieldsmoreoptimizationstepsandthusmorecomputeperbyte,allowingbetterfittingofthedatadistribution.
D.8.PairingStrategyAblation
Asdescribedin§2.1,weoptionallypaircompressedandrawviewsofthesamedocumentduringtrainingtoencourage
explicitcross-representationalignment. Table12ablatesthisdesignchoicealongthreeaxes: (i)pairingstrategy: whether
pairsareusedthroughouttraining(Always-on),onlyduringwarmup(Warmup-only),ornotatall(None);(ii)pairingorder:
whetherrawprecedescompressed(R→C),compressedprecedesraw(C→R),ororderisrandomized(R↔C);and(iii)rate
warmup: whetherthemixingraterisgraduallyincreasedfrom0.4to0.9overthefirst10Ksteps.
WeobservethatWarmup-onlypairingwithrandomizedorderachievesthebestdownstreamperformance(20.1%pass@1).
Thisalignswithfindingsin§3.3: whileAlways-onpairingyieldsnear-perfectin-contexttranslation,itreducestheeffective
compression rate by duplicating data as pairs. Warmup-only pairing provides sufficient signal for the model to learn
cross-representationalignmentearlyintraining,thenrevertstoindependentsamplingtomaximizedataefficiency. Pairing
orderhasamodesteffect,withC→Rslightlyunder-performingotherorderings. Ratewarmupprovidesmarginalgainson
theperformance.
29

ProxyCompressionforLanguageModeling
0.20 0.20
0.18 0.18
0.16 0.16
1@ssaP 0.14 1@ssaP 0.14
0.12 0.12
0.10 0.10
|     | Byte-level |     |     | Byte-level |     |     |
| --- | ---------- | --- | --- | ---------- | --- | --- |
0.08 Proxy Compressor (Neural) 0.08 Proxy Compressor (Neural)
|     | Proxy Compressor (Tokenizer) |     |     | Proxy Compressor (Tokenizer) |     |     |
| --- | ---------------------------- | --- | --- | ---------------------------- | --- | --- |
0.06 0.06
|     | Tokenizer-based      |      |        | Tokenizer-based    |         |     |
| --- | -------------------- | ---- | ------ | ------------------ | ------- | --- |
| 0.2 | 0.4 0.6 0.8          | 1.0  | 50 100 | 150 200            | 250 300 | 350 |
|     | Total Training FLOPs | 1e21 |        | Training Bytes (B) |         |     |
Figure20.Pass@1performanceonHumanEval-Plusfor1.5Bmodelsunderdifferentinputrepresentations,comparedasafunctionof
trainingFLOPs(left)andamountoftrainingdata(right).
0.25 0.25
1@ssaP 0.20 1@ssaP 0.20
0.15 0.15
|     | Byte-level                |     |     | Byte-level                |     |     |
| --- | ------------------------- | --- | --- | ------------------------- | --- | --- |
|     | Proxy Compressor (Neural) |     |     | Proxy Compressor (Neural) |     |     |
0.10 0.10
|     | Proxy Compressor (Tokenizer) |      |        | Proxy Compressor (Tokenizer) |         |     |
| --- | ---------------------------- | ---- | ------ | ---------------------------- | ------- | --- |
|     | Tokenizer-based              |      |        | Tokenizer-based              |         |     |
| 0.5 | 1.0 1.5 2.0                  | 2.5  | 50 100 | 150 200                      | 250 300 | 350 |
|     | Total Training FLOPs         | 1e21 |        | Training Bytes (B)           |         |     |
Figure21. Pass@1performanceonHumanEval-Plusfor4Bmodelsunderdifferentinputrepresentations,comparedasafunctionof
trainingFLOPs(left)andamountoftrainingdata(right).
D.9.TransferStrengthunderControlledRaw-ByteExposure
Toisolatetheeffectoftransferfromtheeffectofincreaseddatavolume, wecomparetwotrainingconfigurationswith
matchedraw-byteexposurebutdifferenttotaltrainingbytes. Specifically,wetrain1.5Bmodelson: (i)95%tokens+5%
rawbytesfor48Ksteps,and(ii)90%tokens+10%rawbytesfor25Ksteps. Bothconfigurationsexposethemodelto
approximately9.1Brawbytes,butthefirstseesmoretotaldataduetoadditionalcompressedbytes.
Table13showsthatundermatchedraw-byteexposure,increasingtotaltrainingbytesviacompresseddatayieldshigher
downstreamperformanceonbyte-levelinference. Thisconfirmspositivetransferfromcompressedtorawrepresentations:
themodelbenefitsfrommorecompressedtrainingdataevenwhenevaluatedpurelyonrawbytes. Thesamepatternholds
fortoken-levelinference(15.2%vs.10.4%),thoughtheabsoluteperformanceislowerthanbyte-levelinterface.
D.10.OntheEffectofFormatSentinels
Formatsentinels(§2.1)explicitlydemarcaterepresentationboundarieswithinpackedsequences. Weablatetheireffect
acrossmodelscalesusingpreliminarygzip-basedproxycompression.AsshowninFigure25,sentinelssignificantlyimprove
performance at the 1.5B scale, but their benefit becomes marginal at 7B. We hypothesize that larger models can more
readilydistinguishbetweenrepresentationswithoutexplicitmarkers. Additionally,whentrainingpurebytemodels(100%
30

ProxyCompressionforLanguageModeling
| 0.275  |     |                           |     |     |     | 0.275  |     |     |                           |     |
| ------ | --- | ------------------------- | --- | --- | --- | ------ | --- | --- | ------------------------- | --- |
| 0.250  |     |                           |     |     |     | 0.250  |     |     |                           |     |
| 0.225  |     |                           |     |     |     | 0.225  |     |     |                           |     |
| 1@ssaP |     |                           |     |     |     | 1@ssaP |     |     |                           |     |
| 0.200  |     |                           |     |     |     | 0.200  |     |     |                           |     |
| 0.175  |     |                           |     |     |     | 0.175  |     |     |                           |     |
| 0.150  |     | Byte-level                |     |     |     | 0.150  |     |     | Byte-level                |     |
|        |     | Proxy Compressor (Neural) |     |     |     |        |     |     | Proxy Compressor (Neural) |     |
0.125 Proxy Compressor (Tokenizer) 0.125 Proxy Compressor (Tokenizer)
| 0.100 |     | Tokenizer-based      |     |     |      | 0.100 |     |                    | Tokenizer-based |         |
| ----- | --- | -------------------- | --- | --- | ---- | ----- | --- | ------------------ | --------------- | ------- |
|       | 1   | 2                    | 3   | 4   | 5    |       | 50  | 100 150            | 200 250         | 300 350 |
|       |     | Total Training FLOPs |     |     | 1e21 |       |     | Training Bytes (B) |                 |         |
Figure22. Pass@1performanceonHumanEval-Plusfor7Bmodelsunderdifferentinputrepresentations,comparedasafunctionof
trainingFLOPs(left)andamountoftrainingdata(right).
Table12.Ablationofratewarmupandpairingdesignforproxycompressortraining.WereportHumanEval-Pluspass@1andpass@10
on1.5Bmodelswithtokenizer-basedproxycompressors.R↔CindicatesrandomorderingwithequalprobabilityofR→CandC→R,
whileR→CandC→Renforceafixedorder,whereR→Cmeansthattherawsequenceprecedesthecompressedsequenceintheinput.
|     |     | PairingStrategy |     | PairingOrder |     | RateWarmup | Pass@1 | Pass@10 |      |     |
| --- | --- | --------------- | --- | ------------ | --- | ---------- | ------ | ------- | ---- | --- |
|     |     | None            |     | —            |     | ✗          | 16.7   |         | 25.7 |     |
✓
|     |     | None      |     | —   |     |     | 16.0 |     | 27.6 |     |
| --- | --- | --------- | --- | --- | --- | --- | ---- | --- | ---- | --- |
|     |     | Always-on |     | R↔C |     | ✗   | 16.6 |     | 27.2 |     |
|     |     | Always-on |     | R↔C |     | ✓   | 16.1 |     | 27.5 |     |
✓
|     |     | Always-on |     | R→C |     |     | 16.5 |     | 27.0 |     |
| --- | --- | --------- | --- | --- | --- | --- | ---- | --- | ---- | --- |
|     |     | Always-on |     | C→R |     | ✓   | 16.1 |     | 25.6 |     |
✓
|     |     | Warmup-only |     | R↔C |     |     | 20.1 |     | 28.7 |     |
| --- | --- | ----------- | --- | --- | --- | --- | ---- | --- | ---- | --- |
raw-formatdata),weobservenoclearperformancedifferencesfromsentinels,whichisexpectedsincenorepresentation
boundariesexist. Basedonthesefindings,weenableformatsentinelsbydefault,astheyprovidebenefitsatsmallerscales
withnegligibleoverheadatlargerscales.
31

ProxyCompressionforLanguageModeling
| 0.250                  |     |                      |                   |      | 0.250                  |     |         |                    |                   |
| ---------------------- | --- | -------------------- | ----------------- | ---- | ---------------------- | --- | ------- | ------------------ | ----------------- |
| 01@ssaP sulP-lavEnamuH |     |                      |                   |      | 01@ssaP sulP-lavEnamuH |     |         |                    |                   |
| 0.225                  |     |                      |                   |      | 0.225                  |     |         |                    |                   |
| 0.200                  |     |                      |                   |      | 0.200                  |     |         |                    |                   |
| 0.175                  |     |                      |                   |      | 0.175                  |     |         |                    |                   |
| 0.150                  |     |                      |                   |      | 0.150                  |     |         |                    |                   |
| 0.125                  |     |                      |                   |      | 0.125                  |     |         |                    |                   |
|                        |     |                      | Byte-level        |      |                        |     |         |                    | Byte-level        |
|                        |     |                      | Proxy (Neural)    |      |                        |     |         |                    | Proxy (Neural)    |
| 0.100                  |     |                      |                   |      | 0.100                  |     |         |                    |                   |
|                        |     |                      | Proxy (Tokenizer) |      |                        |     |         |                    | Proxy (Tokenizer) |
| 0.075                  |     |                      | Tokenizer-based   |      | 0.075                  |     |         |                    | Tokenizer-based   |
|                        | 1   | 2                    | 3                 | 4    |                        | 0   | 200 400 | 600 800            | 1000 1200 1400    |
|                        |     | Total Training FLOPs |                   | 1e21 |                        |     |         | Training Bytes (B) |                   |
Figure23.HumanEval-Pluspass@10for1.5BmodelsunderextendedtrainingversustrainingFLOPs(left)anddataconsumed(right).
Wereportpass@10forstabilityacrosscheckpointsduringpretraining.
| 0.35                   |     |                      |                   |      | 0.35                   |     |     |                    |                   |
| ---------------------- | --- | -------------------- | ----------------- | ---- | ---------------------- | --- | --- | ------------------ | ----------------- |
| 01@ssaP sulP-lavEnamuH |     |                      |                   |      | 01@ssaP sulP-lavEnamuH |     |     |                    |                   |
| 0.30                   |     |                      |                   |      | 0.30                   |     |     |                    |                   |
| 0.25                   |     |                      |                   |      | 0.25                   |     |     |                    |                   |
| 0.20                   |     |                      |                   |      | 0.20                   |     |     |                    |                   |
|                        |     |                      | Byte-level        |      |                        |     |     |                    | Byte-level        |
|                        |     |                      | Proxy (Neural)    |      |                        |     |     |                    | Proxy (Neural)    |
| 0.15                   |     |                      |                   |      | 0.15                   |     |     |                    |                   |
|                        |     |                      | Proxy (Tokenizer) |      |                        |     |     |                    | Proxy (Tokenizer) |
|                        |     |                      | Tokenizer-based   |      |                        |     |     |                    | Tokenizer-based   |
| 0.10                   |     |                      |                   |      | 0.10                   |     |     |                    |                   |
|                        |     | 0.5 1.0              | 1.5               | 2.0  |                        | 0   | 200 | 400 600            | 800 1000          |
|                        |     | Total Training FLOPs |                   | 1e22 |                        |     |     | Training Bytes (B) |                   |
Figure24.HumanEval-Pluspass@10for7BmodelsunderextendedtrainingversustrainingFLOPs(left)anddataconsumed(right).We
reportpass@10forstabilityacrosscheckpointsduringpretraining.
Table 13. Effect of mixing rate under fixed raw-byte exposure for 1.5B models. Performance is measured with pass@1 rates on
HumanEval-Plus.
Pass@1(InferenceMode)
|     | MixingScheme       |     |     | TrainingSteps | RawbytesSeen |      |       |        |     |
| --- | ------------------ | --- | --- | ------------- | ------------ | ---- | ----- | ------ | --- |
|     |                    |     |     |               |              |      | Bytes | Tokens |     |
|     | 95%Tokens+5%Bytes  |     |     | 48000         |              | 9.1B | 15.9  | 15.2   |     |
|     | 90%Tokens+10%Bytes |     |     | 25000         |              | 9.1B | 12.2  | 10.4   |     |
32

ProxyCompressionforLanguageModeling
0.08
0.07
0.06
0.05
0.04
0.03
0.02
0.01
0.00
20 40 60 80 100
Training Bytes (B)
1@ssaP
sulP-lavEnamuH
Gzip:Raw = 75:25 w/ Sentinels
0.07
Gzip:Raw = 75:25 w/o Sentinels
Gzip:Raw = 90:10 w/ Sentinels 0.06
Gzip:Raw = 90:10 w/o Sentinels
0.05
0.04
0.03
0.02
0.01
20 40 60 80 100
Training Bytes (B)
1@ssaP
sulP-lavEnamuH
Gzip:Raw = 0:100 w/ Sentinels
Gzip:Raw = 0:100 w/o Sentinels
Gzip:Raw = 75:25 w/ Sentinels
Gzip:Raw = 75:25 w/o Sentinels
Figure25.Ablationonformatsentinelswithgzipproxycompressionat1.5B(left;Pythoncorpus)and7B(right;fullcorpus)scales.
33