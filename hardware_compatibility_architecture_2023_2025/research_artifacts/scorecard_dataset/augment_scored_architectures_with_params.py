import json
from pathlib import Path

import pandas as pd

try:
    from huggingface_hub import HfApi  # noqa: F401
except Exception:
    HfApi = None  # type: ignore[assignment]


# Manually curated parameter counts (billions) for representative sizes.
PARAMS_BILLIONS = {
    # Encoder-only / BERT family
    "BERT": [0.11, 0.34],
    "RoBERTa": [0.125, 0.355],
    "ALBERT": [0.012, 0.018, 0.223],
    "XLNet": [0.11, 0.34],
    "ELECTRA": [0.014, 0.110, 0.335],
    "DeBERTa": [0.140, 0.400],
    # Decoder / unified LMs
    "GPT-2": [0.117, 0.345, 0.762, 1.5],
    "GPT‑2": [0.117, 0.345, 0.762, 1.5],
    "GPT-3": [175.0],
    "PaLM": [8.0, 62.0, 540.0],
    # Llama family
    "Llama 1": [7.0, 13.0, 33.0, 65.0],
    "Llama 2": [7.0, 13.0, 70.0],
    "Llama 3 / 3.1": [8.0, 70.0, 405.0],
    # Modern open LLMs
    "Qwen2.5": [0.5, 7.0, 14.0, 32.0, 72.0],
    "Gemma / Gemma 2 / Gemma 3": [2.0, 7.0, 27.0],
    "Phi‑3": [3.8, 7.0, 14.0],
    # MoE
    "Mixtral‑8×7B (MoE)": [47.0, 12.9],
    "Mixtral-8×7B (MoE)": [47.0, 12.9],
    "DeepSeek‑V3 (MoE + MLA/DSA)": [671.0, 37.0],
    "Switch Transformer": [1600.0],
    # Classic architectures (one representative size)
    "LSTM / GRU (LLM‑scale)": [0.65],
    "Vanilla RNN": [0.02],
    "Seq2Seq RNN (Encoder‑Decoder)": [0.06],
    # Mamba / SSM
    "Pure Mamba / SSM (Falcon Mamba 7B)": [7.0],
    # Hybrids – illustrative sizes
    "Jamba (Mamba + Attention + MoE)": [52.0, 12.0],
    "Samba (Sliding‑Window Attention + Mamba)": [3.0],
    "Hymba (Fusion + Striped Hybrids)": [7.0],
}


def main() -> None:
    root = Path(__file__).resolve().parent
    csv_path = root / "scored_architectures.csv"
    df = pd.read_csv(csv_path)

    def param_array_for_name(name: str) -> str:
        name = str(name)
        if name in PARAMS_BILLIONS:
            return json.dumps(PARAMS_BILLIONS[name])
        # Fallback: try prefix matches for families
        for key, arr in PARAMS_BILLIONS.items():
            if name.startswith(key):
                return json.dumps(arr)
        return json.dumps([])

    df["Param_Billions"] = df.get("Architecture", "").apply(param_array_for_name)
    df.to_csv(csv_path, index=False)
    print(f"Updated {csv_path} with Param_Billions column")


if __name__ == "__main__":
    main()

