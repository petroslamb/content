# Hardware Friction Scorecard Dataset

**A quantitative analysis of neural architecture adoption: Why do some architectures thrive in production while others remain research curiosities?**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Dataset Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/petroslamb/hardware-friction-scorecard-dataset)

---

## Overview

This dataset contains **119 neural network architectures** (2017-2025) scored against the **Hardware Friction Scorecard** — a quantitative rubric that predicts production adoption by measuring:

1. **Hardware Compatibility** (H-score): How well the architecture maps to GPU primitives
2. **Ecosystem Friction** (E-score): The infrastracture maturity and tooling investment required

Each architecture receives scores on five axes:
- **GA** (Global Access): 0-2 — Memory access patterns (GEMM-heavy = 2)
- **MAL** (Memory Access Locality): 0-2 — Cache-friendly vs scattered access
- **PAR** (Parallelism): 0-2 — Training-time parallelizability
- **STI** (Specialized Tooling Investment): 0-2 — Requires custom kernels?
- **IM** (Infrastructure Maturity): 0-2 — Upstream framework support

From these, we derive:
- **H = GA + MAL + PAR** (Hardware score, 0-6)
- **E = STI + IM** (Ecosystem score, 0-4)
- **Zone**: Production readiness (🟢 Green / 🟡 Yellow / 🟠 Orange / 🔴 Red)

---

## Key Findings

The dataset validates the **"Transformer Attractor"** thesis:

1. **100% of frontier models** (GPT-4, Claude, Llama, Gemini) use GEMM-heavy, GPU-friendly primitives (H ≥ 5)
2. **Pure SSMs hit a ceiling** at ~7B parameters (no frontier model >70B uses pure Mamba)
3. **MoE became standard** for high-end models (DeepSeek-V3, Llama 4, Mixtral)
4. **Multimodal models converged to Transformers**: DiT replaced UNets in image/video, AudioLM tokenizes audio for standard decoders
5. **Infrastructure lag is predictable**: 24-36 month gap from paper to production standard (e.g., FlashAttention: May 2022 → May 2024)

---

## Quick Start

### Load the Dataset

```python
import pandas as pd

# Load the scored dataset
df = pd.read_csv('scored_architectures.csv')

# Filter by production-ready architectures
green_zone = df[df['Zone'] == '🟢 Green']
print(f"Production-ready: {len(green_zone)} architectures")

# Show hardware scores by era
print(df.groupby('Era')['H'].mean())
```

### Explore Examples

See [`EXAMPLES.md`](EXAMPLES.md) for:
- Filtering by friction zones
- Plotting H vs E scores
- Analyzing adoption velocity
- Era-based trends

---

## Dataset Structure

### Core Files

| File | Description |
|------|-------------|
| `scored_architectures.md` | **Primary dataset** (human-readable markdown tables) |
| `scored_architectures.csv` | Machine-readable CSV (auto-generated from MD) |
| `parse_scored_architectures.py` | Sync tool (MD → CSV) |

### Supporting Materials

| Directory | Contents |
|-----------|----------|
| `essays/` | Three Substack essays explaining the theory |
| `experiments/` | Simple modeling scripts (decision trees, logistic regression) |

---

## Architecture Coverage

The dataset includes:

### Language Models (72 architectures)
- **Transformers**: Vanilla, GQA, MLA, Flash-optimized variants
- **MoE**: Mixtral, DeepSeek-V3, GShard, Switch Transformer
- **SSMs**: Mamba, S4, Hyena, RWKV
- **Hybrids**: Jamba, Samba, Hymba, RetNet
- **RNNs**: LSTM, GRU, xLSTM
- **Historical**: BERT, GPT-2/3, T5, PaLM

### Multimodal & Generative Media (19 architectures)
- **Image Generation**: UNet, DiT, MaskGIT, StyleGAN3
- **Video**: Sora (Video DiT), VideoPoet, UNet 3D
- **Audio**: AudioLM, WaveNet, Jukebox, Voicebox
- **Fusion**: CLIP, LLaVA, Chameleon, Flamingo
- **Vision**: ViT, DeiT, Vision Mamba

### Specialized Techniques (28 architectures)
- Attention variants (Reformer, Performer, Lightning, Longformer)
- Training/serving optimizations (LoRA, quantization, FlashAttention)
- Memory systems (RETRO, RAG, Titans)
- Exotic architectures (KANs, Neural ODEs, Capsule Networks)

---

## Methodology

Scores are based on the **[Hardware Friction Scorecard v2.3](../../hardware_friction_scorecard/Hardware_Friction_Scorecard_v2.md)** rubric. Each architecture is evaluated by:

1. **Analyzing the core compute primitives** (GEMM, scan, convolution, FFT)
2. **Measuring memory access patterns** (sequential, strided, random)
3. **Assessing parallelizability** (across batch, sequence, or layers)
4. **Surveying ecosystem support** (PyTorch, vLLM, TensorRT-LLM, Triton)

Scores are deliberately **conservative** — when in doubt, we penalize GA/MAL/PAR for non-GEMM kernels.

---

## Essays & Context

This dataset backs three published research essays:

1. **["What Actually Works" (2024)](essays/Substack_What_Actually_Works_2023_2025_Update.md)**  
   The original thesis: Hardware compatibility, not model capability, determines production adoption.

2. **["The Hardware Friction Map" (2025)](essays/The_Hardware_Friction_Map_Substack.md)**  
   Introduces the friction scorecard and the "Startup Heuristic" — why high friction kills resource-constrained teams.

3. **["The Transformer Attractor" (2025)](essays/The_Transformer_Attractor_Substack.md)**  
   The convergence thesis: Why every domain (text, image, video, audio) is collapsing to Transformer primitives.

---

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{lambropoulos2025hardware,
  title={Hardware Friction Scorecard Dataset: Quantitative Analysis of Neural Architecture Adoption (2017-2025)},
  author={Lambropoulos, Petros},
  year={2025},
  url={https://github.com/petroslamb/hardware-friction-scorecard-dataset},
  license={CC-BY-4.0}
}
```

Or use the structured [`CITATION.cff`](CITATION.cff) file.

---

## Contributing

We welcome contributions! To add a new architecture:

1. **Understand the rubric**: Read the [Scorecard v2.3](../../hardware_friction_scorecard/Hardware_Friction_Scorecard_v2.md)
2. **Score the architecture**: Use the 5-axis system (GA/MAL/PAR/STI/IM)
3. **Add to `scored_architectures.md`**: Follow the existing table format
4. **Regenerate CSV**: Run `python parse_scored_architectures.py`
5. **Submit a PR**: With a clear rationale for your scores

### Adoption Timeline Data Needed

We're actively collecting `First_10B_Date` (when the first >10B model using this architecture shipped) to validate the friction → adoption velocity hypothesis. If you know deployment dates, please contribute!

---

## License

This dataset is licensed under **[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)**.

You are free to share and adapt this work for any purpose, including commercial use, provided you give appropriate credit.

---

## Contact

- **Author**: Petros Lambropoulos
- **Dataset Issues**: [GitHub Issues](https://github.com/petroslamb/hardware-friction-scorecard-dataset/issues)
- **Research Questions**: [Your contact method]

---

**Last Updated**: December 2025  
**Dataset Version**: 1.0.0 (119 architectures)
