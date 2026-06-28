# Ornith-1.0-35B-heretic

Docker-contained Heretic 1.4.0 project for creating a local heretic/abliterated
artifact from `deepreinforce-ai/Ornith-1.0-35B` on the DGX Spark.

This branch is the v2 MPOA-style 800-trial run. It keeps the v1 low-KL
settings but patches Heretic component discovery inside Docker so Ornith exposes
`attn.o_proj`, `attn.out_proj`, and `mlp.down_proj`.

## Prebuilt model

If you do not want to run Heretic yourself, the exported model is available on
Hugging Face:
[thanet-s/Ornith-1.0-35B-heretic](https://huggingface.co/thanet-s/Ornith-1.0-35B-heretic).

This directory produces an unquantized Heretic artifact:

- source model: `deepreinforce-ai/Ornith-1.0-35B`
- output model: `output/Ornith-1.0-35B-heretic`
- Heretic version: `1.4.0`
- quantization: `none`
- Docker base: `nvcr.io/nvidia/pytorch:26.05-py3`
- HF cache: `${HOME}/.cache/huggingface` on the DGX, mounted to
  `/root/.cache/huggingface` in the container

## Commands

Build:

```bash
docker compose build heretic
```

Smoke check:

```bash
docker compose run --rm heretic /workspace/scripts/smoke-check.sh
```

Inspect v2 components:

```bash
docker compose run --rm --no-deps heretic python3 /workspace/scripts/inspect-components-v2.py
```

Optional pre-download:

```bash
docker compose run --rm heretic /workspace/scripts/download-model.sh
```

Run Heretic:

```bash
docker compose run --name ornith-heretic-v2-mpoa-800 heretic /workspace/scripts/run-heretic-v2-mpoa-800.sh
```

The runner chooses the first Pareto-optimal trial when optimization completes,
selects "Save the model to a local folder", and exports a merged model to:

```text
output/Ornith-1.0-35B-heretic
```

Follow logs:

```bash
docker logs -f ornith-heretic-v2-mpoa-800
```

Resume after interruption:

```bash
docker compose run --name ornith-heretic-v2-mpoa-800 heretic /workspace/scripts/run-heretic-v2-mpoa-800.sh
```

## HF token

If Hugging Face access needs a token, do not put it in this repo. Login inside a
throwaway Docker run or pass it via the shell environment:

```bash
docker compose run --rm -e HF_TOKEN heretic hf auth whoami
```
