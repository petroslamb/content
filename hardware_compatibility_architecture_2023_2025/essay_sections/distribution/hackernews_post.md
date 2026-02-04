# Hacker News Post: The Transformer Attractor

**Post link:** https://open.substack.com/pub/lambpetros/p/the-transformer-attractor

---

**Title:** The Transformer Attractor: Why alternative architectures converge toward GEMM patterns at scale

**URL:** https://open.substack.com/pub/lambpetros/p/the-transformer-attractor

---

**Introductory comment:**

Mamba-2 rewrote its core operation from parallel scans to block-diagonal GEMMs. RetNet was abandoned by Microsoft Research five months after publication. RWKV hit 14B through community persistence but can't break to frontier scale.

The thesis: Transformers and NVIDIA GPUs co-evolved into a stable attractor. Alternative architectures must clear two reinforcing gates (Tensor Core efficiency + major lab backing) simultaneously. At frontier scale, no one has.

Includes Tensor Core utilization numbers for different architectures and three falsifiable predictions for 2028. Also covers why alternative chip vendors face structural barriers that Google solved in 2016 but are nearly impossible to replicate now.

Interested in pushback from anyone with access to unpublished scaling experiments.
