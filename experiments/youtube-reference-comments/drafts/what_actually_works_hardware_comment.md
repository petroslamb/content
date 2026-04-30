Draft references comment for: Why AI Architecture Progress Is Filtered by Hardware | A Cinematic Research Brief

This brief leans most heavily on these sources:

- **FlashAttention** — the cleanest evidence that a winning idea can be about memory movement and kernel design, not just a new mathematical primitive.
- **FlashAttention-2** — shows how quickly a hardware-aligned trick turns into standard practice once frameworks absorb the kernel work.
- **Switch Transformers** — the early large-scale reference point for sparse conditional execution and the starting line for the MoE story.
- **DeepSeek-V3 technical report** — current proof that MoE plus KV-compression-style design choices can win under real deployment pressure.
- **Mamba and hybrid SSM reports** — used here as the contrast case for architectures that are compelling on paper but still constrained by parallel hardware.

Full essay + full references: https://lambpetros.substack.com/p/what-actually-works-the-hardware
