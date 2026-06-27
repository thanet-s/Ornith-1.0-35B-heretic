#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import importlib.metadata
import os
import torch
from huggingface_hub import model_info

print("heretic-llm", importlib.metadata.version("heretic-llm"))
print("torch", torch.__version__)
print("cuda_available", torch.cuda.is_available())
if torch.cuda.is_available():
    print("gpu", torch.cuda.get_device_name(0))
    free, total = torch.cuda.mem_get_info(0)
    print("gpu_mem_free_gb", round(free / 1024**3, 2))
    print("gpu_mem_total_gb", round(total / 1024**3, 2))

info = model_info("deepreinforce-ai/Ornith-1.0-35B")
print("model", info.modelId)
print("private", info.private)
print("gated", getattr(info, "gated", None))
print("sha", info.sha)
print("hf_home", os.environ.get("HF_HOME"))
PY

heretic --help | sed -n '1,160p'
