# r/LLMDevs Discussion Post

Draft for posting in r/LLMDevs. No Substack link, stands alone as genuine discussion. Slightly more practical framing than the r/ML version, with the test proposal front-loaded.

**Title:** A specific LLM failure mode I'm calling "the binding gap" (and how to test for it)

---

Hi everyone, I have been spending a lot of time thinking about a particular failure mode that I do not think has a good name yet. I want to run it by people who know this space better than I do, because I am still sorting out whether it is genuinely productive or just repackaging existing concepts.

Here is the core idea:

"Tell a model that Tom Smith's wife is Mary Stone. Then ask who Mary Stone's husband is. Nothing new has been added. Same entities, same relation, same world. Performance still drops."

Wang and Sun recently argued this Reversal Curse reflects actual problems in transformer representations, specifically inconsistency and entanglement in how concepts get bound together. They even showed that architectural changes aimed at better conceptual binding can reduce the failure. That moves it from a quirky benchmark effect toward a real design problem.

I think this extends well beyond the reversal case and deserves its own name. I have been calling it the binding gap. The idea is that a model preserves enough semantic material to generate a plausible answer but loses the specific attachment that makes the answer faithful. It remembers the paper but assigns the number to the wrong variable. It stays in the right semantic neighborhood while the output stops being usable.

The evidence that this is a real family of failures rather than a single benchmark artifact is starting to accumulate. Feng and Steinhardt showed that models use internal binding ID vectors and that causal interventions on those activations change pairing behavior. Dai and colleagues later identified a low-rank ordering subspace that directly steers which attribute gets bound to which entity. The mechanism is real and manipulable.

The bridge from toy cases to actual language is where it starts mattering. Denning et al looked at thematic role understanding and found that models can extract agent and patient information, but it influences overall sentence representations much more weakly than it does in humans. The role structure simply does not dominate the broader representational geometry.

Then comes the heavy load case. Tan and D'Souza tested models on evidence extraction for meta-analysis, where the task is to turn scientific prose into structured study records. Models performed moderately on single-property queries, then fell apart when the task required stable binding between variables, roles, methods, and effect sizes simultaneously. Full association tuples hit near-zero reliability. The dominant errors were role reversals, cross-analysis binding drift, and numeric misattribution. This is what the binding gap looks like under actual research pressure.

The question I am wrestling with is whether "binding gap" is doing real work or just adding vocabulary. A simple test would be to take a standard QA benchmark, add a role-reversal perturbation to half the entries, and check whether the accuracy gap between original and reversed correlates with model scale the way other capabilities do. Or to check whether existing interventions designed to improve binding, like Jamba-style architectures or MELODY-style memory, close the gap on extraction tasks more than they close it on open-ended ones. If the gap shrinks proportionally, the concept pays for itself. If it does not, I am probably just redescribing something we already have a name for.

That is what I wanted to ask here. Do people who work on mechanistic interpretability or evaluation design see this as a productive way to slice the space, or do entanglement and compositionality cover most of it already? Either answer would save me a lot of time.

## Notes

- No Substack or external links. All referenced papers link to arXiv in comments if threads go deeper.
- If someone asks in comments whether you have written more, mention the Substack organically then.
- Post from your personal account. r/ML responds better to individual accounts than to publication-branded ones.
