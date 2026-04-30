Draft references comment for: Why Hardware Friction Decides What Ships in AI | A Cinematic Research Brief

This brief leans most heavily on these sources:

- **Switch Transformers** — early proof that sparse expert routing could scale language models without activating the whole network on every token.
- **DeepSeek-V3 / DeepSeek-R1 technical reports** — strongest current evidence that MoE plus memory-aware attention is not just a trick but a real frontier production design.
- **Mixtral 8x7B technical report** — open-weight evidence that sparse MoE can outperform dense baselines while staying economically deployable.
- **FlashAttention / FlashAttention-2** — key evidence for the claim that the winners are often the architectures and kernels that respect GPU memory movement instead of fighting it.
- **Mamba and later hybrid SSM reports** — the boundary case used here to show that elegant alternatives still struggle when they push against parallel hardware.

Full essay + full references: https://lambpetros.substack.com/p/the-hardware-friction-map
