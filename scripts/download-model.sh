#!/usr/bin/env bash
set -euo pipefail

hf download deepreinforce-ai/Ornith-1.0-35B \
  --local-dir /workspace/cache/models/Ornith-1.0-35B \
  --max-workers "${HF_DOWNLOAD_WORKERS:-8}"
