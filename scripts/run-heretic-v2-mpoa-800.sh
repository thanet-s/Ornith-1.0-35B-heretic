#!/usr/bin/env bash
set -euo pipefail

MODEL_ID="${MODEL_ID:-deepreinforce-ai/Ornith-1.0-35B}"
OUTPUT_DIR="${OUTPUT_DIR:-/workspace/output/Ornith-1.0-35B-heretic}"

mkdir -p /workspace/output /workspace/checkpoints-v2-mpoa-800 /workspace/plots

export MODEL_ID OUTPUT_DIR
exec python3 /workspace/scripts/run-heretic-v2-mpoa-800-auto.py
