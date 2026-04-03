# Reddit Post: The Transformer Attractor

**Post link:** https://open.substack.com/pub/lambpetros/p/the-transformer-attractor

**Recommended Subreddit:** r/MachineLearning (https://www.reddit.com/r/MachineLearning/)

---

**Title:** [D] Why Mamba rewrote its core algorithm and Microsoft abandoned RetNet: The Hardware Attractor Thesis

---

**Post Body:**

Mamba-2 restructured its recurrence from parallel scans (10-20% Tensor Core utilization) to block-diagonal GEMMs (60-70%). The architecture bent to fit the silicon.

RetNet was published by Microsoft Research in July 2023 with promising results at 6.7B. Five months later, the same organization shipped Phi-2, a dense Transformer. Then Phi-3. Then Phi-4. The co-authors didn't bet on their own architecture.

I wrote an analysis of why this pattern keeps repeating. The short version: Transformers and NVIDIA GPUs co-evolved into a stable attractor. Breaking out requires clearing two reinforcing gates at once, hardware compatibility and institutional backing, and the gates make each other harder to pass. At frontier scale, no pure alternative has done it.

Essay has Tensor Core utilization numbers, analysis of alternative chip vendors, and three falsifiable predictions for 2028.