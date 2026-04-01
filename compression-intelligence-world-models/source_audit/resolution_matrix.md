# Resolution Matrix

This matrix now reflects the rewritten article.

Disposition labels:

* `KEEP`: the claim stands as written.
* `KEEP WITH QUALIFIER`: the claim stands because the article now frames it carefully.
* `REMOVED`: the earlier weak claim has been cut from the article.
* `WATCH`: the claim is acceptable, but only if the metaphorical framing stays disciplined.

## Claim-Level Resolutions

| ID | Current Lines | Claim | Disposition | Resolution |
| --- | --- | --- | --- | --- |
| C1 | 3, 9 | Prediction and compression are tightly linked in language modeling. | KEEP | Strongly supported and central. |
| C2 | 11, 17 | Understanding as compression is a useful research frame. | KEEP WITH QUALIFIER | The article now treats it as a program, not final doctrine. |
| C3 | 15 | Better compression tracks stronger benchmark performance. | KEEP | Clean empirical claim. |
| C4 | 21 | Models learn internal structure richer than surface token frequency. | KEEP WITH QUALIFIER | Framed cautiously as inference from behavior and representation. |
| C5 | 23 | `Compression is Routing` is a promising architectural direction. | KEEP WITH QUALIFIER | Safe because the article names it as a preprint. |
| C6 | 27-29 | Hierarchical and looped models support multi-step internal organization. | KEEP WITH QUALIFIER | The old recursive-pointer overclaim is gone. |
| C7 | 33-35 | Compression implies selective loss with philosophical consequences. | WATCH | Acceptable if read as synthesis rather than proof. |
| C8 | 39-41 | Alignment works against a much larger pretraining prior. | KEEP | Strong section. |
| C9 | 45-47 | Factuality remains distinct from compression quality. | KEEP | Now anchored in the FACTS benchmark and hallucination survey. |
| C10 | 51 | Semantic communication offers a real engineering analogue to semantic compression. | KEEP | Well supported. |
| C11 | 53 | Holography offers an adjacent example of dense non-linguistic representation. | KEEP WITH QUALIFIER | Safe because the analogy is kept narrow. |
| C12 | 57-59 | Economics and deployment constraints matter for semantic compression. | KEEP | Strong and grounded. |
| C13 | 63-65 | The metaphor has explanatory value but strict limits. | WATCH | This is the article's governing discipline. |

## Removed Claims

| Old Issue | Disposition | Outcome |
| --- | --- | --- |
| `PHS` as concrete architecture | REMOVED | Entire claim family removed. |
| Deterministic guarantees paragraph | REMOVED | Removed. |
| Hallucinations as compression artifacts | REMOVED | Replaced by a more accurate multi-causal framing. |
| Tokens as recursive pointers | REMOVED | Replaced by hierarchical / looped internal-state framing. |

## Source-Level Resolutions

| Source Family | Disposition | Outcome |
| --- | --- | --- |
| `InfoQ`, `ResearchGate` wrappers, `WordPress`, `Hugging Face` search, `Reddit`, `IJIRT` | REMOVED OR REPLACED | No longer used in the article. |
| `Language Modeling Is Compression`, `Compression Represents Intelligence Linearly`, alignment ACL paper, FACTS paper, semantic communication paper, holography papers, economics paper, TinyLM review, proxy compression paper | KEEP | Current evidence base. |
| `Compression Is Routing`, `Understanding Is Compression` | KEEP WITH QUALIFIER | Still useful, but the article must preserve their provisional status. |
