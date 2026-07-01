#!/usr/bin/env bash
set -euo pipefail

MODEL_ID="${MODEL_ID:-deepreinforce-ai/Ornith-1.0-35B}"
OUTPUT_DIR="${OUTPUT_DIR:-/workspace/output/Ornith-1.0-35B-heretic-v3-from-base}"
HERETIC_CONFIG="${HERETIC_CONFIG:-/workspace/config-v3.toml}"
HERETIC_RUN_DIR="${HERETIC_RUN_DIR:-/workspace/run-v3-from-base}"

mkdir -p /workspace/output /workspace/checkpoints-v3-from-base-relaxed-kl /workspace/plots "$HERETIC_RUN_DIR"

export MODEL_ID OUTPUT_DIR HERETIC_CONFIG HERETIC_RUN_DIR
exec python3 /workspace/scripts/run-heretic-v3-from-base-auto.py
