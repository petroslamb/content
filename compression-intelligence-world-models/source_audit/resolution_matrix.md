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
| C1 | 27 | Prediction and compression are tightly linked in language modeling. | KEEP | Strongly supported and central. |
| C2 | 31 | Understanding as compression is a useful research frame. | KEEP WITH QUALIFIER | The article now treats it as a program, not final doctrine. |
| C3 | 35 | Better compression tracks stronger functional structure retention. | KEEP | Clean empirical claim via Wan, Li, and Sengupta. |
| C4 | 37 | Models learn internal structure richer than surface token frequency. | KEEP WITH QUALIFIER | Framed cautiously as inference from behavior and representation. |
| C5 | 39 | `Compression is Routing` is a promising architectural direction. | KEEP WITH QUALIFIER | Now structurally verified by KV-cache limit studies (Ananthanarayanan). |
| C6 | 41 | Cache compression proves the boundary of semantic reachability. | KEEP | Highly robust KV constraint test (Ananthanarayanan). |
| C7 | 49-51 | Factuality and Hallucination behave like artifact boundaries. | KEEP | Anchored in the FACTS benchmark and hallucination survey. |
| C8 | 53 | Alignment works against a much larger pretraining prior. | KEEP | Strong section. |
| C9 | 57 | Semantic communication offers a real engineering analogue. | KEEP | Well supported. |
| C10 | 61 | Holography offers an adjacent example of dense constraint geometry. | KEEP WITH QUALIFIER | Safe because the analogy is kept narrow. |
| C11 | 65-71 | Economics, hardware limitations, and deployment constraints matter. | KEEP | Strong, grounded climax section across Kipf, Pouransari. |

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
