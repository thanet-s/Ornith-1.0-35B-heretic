FROM nvcr.io/nvidia/pytorch:26.05-py3

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/root/.cache/huggingface \
    HUGGINGFACE_HUB_CACHE=/root/.cache/huggingface/hub \
    TRANSFORMERS_CACHE=/root/.cache/huggingface/hub \
    PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

WORKDIR /workspace

RUN python3 -m pip install --no-cache-dir "uv==0.9.19" \
    && uv pip install --system --break-system-packages --no-cache \
      "heretic-llm==1.4.0" \
      "huggingface_hub[hf_transfer]" \
      "hf_transfer" \
      "pexpect"

COPY scripts/ /workspace/scripts/
RUN chmod +x /workspace/scripts/*.sh

CMD ["/bin/bash"]
