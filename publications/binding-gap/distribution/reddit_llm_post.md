# r/LLM Discussion Post

Draft for posting in r/LLM.

**Title:** Is "the binding gap" a useful way to think about LLM failures?

---

I've been tracking a failure pattern across several recent papers that I have not seen named clearly enough to be useful. Want to run it by this crowd to see if it lands or if it is just repackaging things that already have names.

Tell a model "Tom Smith's wife is Mary Stone." Then ask "who is Mary Stone's husband?" Nothing new has been added. Same entities, same relation. Performance still drops.

Wang and Sun showed this on the Reversal Curse and argued it reflects real problems in how transformers bind concepts — inconsistency, entanglement in representations. They showed architectural changes aimed at better binding can reduce the failure. That moves it from quirky benchmark effect toward a design problem.

I think this extends well beyond the reversal case. Call it the binding gap: a model preserves enough semantic material to generate a plausible answer but loses the specific attachment that makes it faithful. It remembers the paper but assigns the number to the wrong variable. The output stays in the right neighborhood while becoming unusable.

The evidence that this is its own family of failures is accumulating. Feng and Steinhardt showed models use internal binding ID vectors and that causal interventions on those activations change pairing behavior. Dai and colleagues identified a low-rank ordering subspace that directly steers which attribute gets bound to which entity. Denning et al looked at thematic role understanding and found agent/patient info influences sentence representations much more weakly than in humans. The mechanism is real and manipulable.

Then the heavy-load case. Tan and D'Souza tested on meta-analysis evidence extraction with GPT-5.2 and Qwen3-VL. Single-property queries land around 0.40-0.50 F1. Full association tuples with variables, methods, and effect sizes drop to ~0.24 and near-zero in dense result sections. Role reversals, cross-analysis binding drift, numeric misattribution. This is what the binding gap looks like under actual research pressure.

The question is whether this is a productive way to slice failures or just adding vocabulary. A simple test: take a standard QA benchmark, add a role-reversal perturbation to half the entries, and check whether the gap between original and reversed correlates with scale the way other capabilities do. Or test whether architectural interventions designed to improve binding close the gap on extraction more than on open-ended tasks.

Does this feel like a useful frame for evaluation design, or is it covered by entanglement and compositionality already? Either answer saves me time.