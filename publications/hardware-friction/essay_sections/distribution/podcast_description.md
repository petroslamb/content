# Podcast Description: The Transformer Attractor

**Post link:** https://open.substack.com/pub/lambpetros/p/the-transformer-attractor

---

## Episode Title

The Transformer Attractor

---

## Short Description

Why Mamba rewrote its core algorithm. Why Microsoft abandoned RetNet. Why no alternative architecture has shipped as a frontier model. The hardware economics that explain all three.

---

## Full Episode Description

Between 2023 and 2024, Mamba's authors rewrote their core algorithm. The original used parallel scans, an elegant recurrence that propagated state efficiently over long sequences. The rewrite uses matrix multiplications. Their paper is explicit about why: efficient computation on modern hardware accelerators. The architecture changed to fit the silicon. The silicon did not budge.

This is the Transformer Attractor in action. Transformers and NVIDIA GPUs co-evolved over the past decade into a stable equilibrium. Now alternative architectures face a trap: they must achieve high Tensor Core utilization AND secure major lab backing simultaneously. Poor hardware compatibility makes institutional bets expensive. Lack of institutional backing means no investment in the kernel optimizations that would improve hardware compatibility. The gates reinforce each other.

This episode covers the evidence: Mamba-2's convergence toward GEMM patterns, Microsoft Research's abandonment of RetNet, RWKV's ceiling at 14B parameters despite years of community effort. It also covers why alternative chip vendors face structural barriers that Google solved in 2016 but are nearly impossible to replicate in 2025.

Three falsifiable predictions for 2028. Practical heuristics for researchers, engineering leaders, and investors evaluating alternative architectures.

**Read the full essay:** https://open.substack.com/pub/lambpetros/p/the-transformer-attractor

---

## Keywords

Transformers, Mamba, RetNet, RWKV, SSM, state space models, NVIDIA, Tensor Cores, AI hardware, GPU computing, AI infrastructure
