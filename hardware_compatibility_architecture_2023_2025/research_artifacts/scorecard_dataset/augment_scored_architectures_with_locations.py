import json
from pathlib import Path

import pandas as pd


# Manually curated model locations (Hugging Face repos or canonical paper URLs).
# Values are lists so we can capture multiple representative checkpoints.
LOCATIONS = {
    # Encoder-only / BERT family
    "BERT": [
        "https://huggingface.co/bert-base-uncased",
        "https://huggingface.co/bert-large-uncased",
    ],
    "RoBERTa": [
        "https://huggingface.co/roberta-base",
        "https://huggingface.co/roberta-large",
    ],
    "ALBERT": [
        "https://huggingface.co/albert-base-v2",
        "https://huggingface.co/albert-xxlarge-v2",
    ],
    "XLNet": [
        "https://huggingface.co/xlnet-base-cased",
        "https://huggingface.co/xlnet-large-cased",
    ],
    "ELECTRA": [
        "https://huggingface.co/google/electra-base-discriminator",
        "https://huggingface.co/google/electra-large-discriminator",
    ],
    "DeBERTa": [
        "https://huggingface.co/microsoft/deberta-base",
        "https://huggingface.co/microsoft/deberta-large",
    ],
    # Decoder / unified Transformers
    "GPT‑2": [
        "https://huggingface.co/gpt2",
        "https://huggingface.co/gpt2-medium",
        "https://huggingface.co/gpt2-large",
        "https://huggingface.co/gpt2-xl",
    ],
    "T5": [
        "https://huggingface.co/t5-small",
        "https://huggingface.co/t5-base",
        "https://huggingface.co/t5-large",
    ],
    # GPT‑3 and PaLM are closed; point to papers.
    "GPT‑3": ["https://arxiv.org/abs/2005.14165"],
    "PaLM": ["https://arxiv.org/abs/2204.02311"],
    # Llama family
    "Llama 1": [
        "https://huggingface.co/decapoda-research/llama-7b-hf",
        "https://huggingface.co/decapoda-research/llama-13b-hf",
    ],
    "Llama 2": [
        "https://huggingface.co/meta-llama/Llama-2-7b-hf",
        "https://huggingface.co/meta-llama/Llama-2-13b-hf",
        "https://huggingface.co/meta-llama/Llama-2-70b-hf",
    ],
    "Llama 3 / 3.1": [
        "https://huggingface.co/meta-llama/Meta-Llama-3-8B",
        "https://huggingface.co/meta-llama/Meta-Llama-3-70B",
    ],
    # Modern open LLMs
    "Qwen2.5": [
        "https://huggingface.co/Qwen/Qwen2.5-7B",
        "https://huggingface.co/Qwen/Qwen2.5-32B",
        "https://huggingface.co/Qwen/Qwen2.5-72B",
    ],
    "Gemma / Gemma 2 / Gemma 3": [
        "https://huggingface.co/google/gemma-2b",
        "https://huggingface.co/google/gemma-7b",
    ],
    "Phi‑3": [
        "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct",
        "https://huggingface.co/microsoft/Phi-3-medium-4k-instruct",
    ],
    # MoE models
    "Mixtral‑8×7B (MoE)": [
        "https://huggingface.co/mistralai/Mixtral-8x7B-v0.1",
        "https://huggingface.co/mistralai/Mixtral-8x22B-v0.1",
    ],
    "DeepSeek‑V3 (MoE + MLA/DSA)": [
        "https://huggingface.co/deepseek-ai/DeepSeek-V3",
    ],
    "Switch Transformer": [
        "https://arxiv.org/abs/2101.03961",
    ],
    # Mamba / SSM
    "Pure Mamba / SSM (Falcon Mamba 7B)": [
        "https://huggingface.co/TiiUAQ/falcon-mamba-7b",
    ],
    # Hybrids
    "Jamba (Mamba + Attention + MoE)": [
        "https://huggingface.co/ai21labs/Jamba-v0.1",
    ],
    "Samba (Sliding‑Window Attention + Mamba)": [
        "https://arxiv.org/abs/2406.07522",
    ],
    "Hymba (Fusion + Striped Hybrids)": [
        "https://arxiv.org/abs/2411.13676",
    ],
    # Modern production decoders/encoders
    "ModernBERT": [
        "https://huggingface.co/answerdotai/ModernBERT-large",
        "https://huggingface.co/answerdotai/ModernBERT-base",
    ],
    "Mixtral‑8×7B (MoE)": [
        "https://huggingface.co/mistralai/Mixtral-8x7B-v0.1",
    ],
    # Misc
    "Transformer + FlashAttention (reference)": [
        "https://huggingface.co/meta-llama/Meta-Llama-3-8B",
    ],
}


def locations_for_arch(name: str) -> str:
    name = str(name)
    if name in LOCATIONS:
        return json.dumps(LOCATIONS[name])
    # Fallback: prefix/substring match for families
    for key, urls in LOCATIONS.items():
        if name.startswith(key) or key in name:
            return json.dumps(urls)
    return json.dumps([])


def main() -> None:
    root = Path(__file__).resolve().parent
    csv_path = root / "scored_architectures.csv"
    df = pd.read_csv(csv_path)

    df["Model_Locations"] = df["Architecture"].apply(locations_for_arch)
    df.to_csv(csv_path, index=False)
    print(f"Updated {csv_path} with Model_Locations column")


if __name__ == "__main__":
    main()

