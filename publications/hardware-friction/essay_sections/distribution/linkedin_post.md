# LinkedIn Post: The Transformer Attractor

**Post link:** https://open.substack.com/pub/lambpetros/p/the-transformer-attractor

---

Mamba's authors rewrote their core algorithm between v1 and v2. The original used parallel scans, an elegant recurrence. The rewrite uses matrix multiplications. Their paper is explicit about why: "efficient computation via matrix multiplications on modern hardware accelerators."

The architecture changed. The hardware did not budge.

This isn't an isolated case. Microsoft Research published RetNet in July 2023 with Transformer-matching perplexity at 6.7B parameters. Five months later, the same organization shipped Phi-2, a dense Transformer. Then Phi-3. Then Phi-4. The co-authors didn't bet on their own architecture. We don't know exactly why because Microsoft never published the scaling experiments that would tell us.

I spent months analyzing what happens when alternative architectures attempt frontier scale. The pattern is consistent: they either adopt Transformer-like compute patterns or they fail to attract the institutional backing needed to validate them at 30B+ parameters. The two requirements reinforce each other. Poor hardware compatibility makes institutional bets expensive and risky. Lack of institutional backing means no one invests in the kernel optimizations that would improve hardware compatibility.

NVIDIA's roadmap through 2027 includes a "Second-Generation Transformer Engine" and promises "3x faster Transformer layer performance." What's absent: any silicon support for the primitives alternative architectures need. That's a $30B implicit bet that Transformers remain dominant. Betting against it requires simultaneously changing hardware, architecture, ecosystem, and economics. No single actor has the capital or coordination to do all four at once.

The essay includes three falsifiable predictions for 2027-2028 and practical heuristics for evaluating alternative architectures. If you're making infrastructure or investment decisions in this space, it's worth understanding the structural forces at play.

https://open.substack.com/pub/lambpetros/p/the-transformer-attractor
