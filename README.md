# Ornith-1.0-35B-heretic

Docker-contained Heretic 1.4.0 project for creating a local heretic/abliterated
artifact from `deepreinforce-ai/Ornith-1.0-35B` on the DGX Spark.

This directory intentionally produces the first-stage unquantized artifact only:

- source model: `deepreinforce-ai/Ornith-1.0-35B`
- output model: `output/Ornith-1.0-35B-heretic`
- Heretic version: `1.4.0`
- quantization while running Heretic: `none`
- Docker base: `nvcr.io/nvidia/pytorch:26.05-py3`
- HF cache: `${HOME}/.cache/huggingface` on the DGX, mounted to
  `/root/.cache/huggingface` in the container

The GB10 `NVFP4-FP8Dense` quantization should be done as a separate second
phase after this output reloads and evaluates correctly.

## Commands

Build:

```bash
docker compose build heretic
```

Smoke check:

```bash
docker compose run --rm heretic /workspace/scripts/smoke-check.sh
```

Optional pre-download:

```bash
docker compose run --rm heretic /workspace/scripts/download-model.sh
```

Run Heretic:

```bash
docker compose run --name ornith-heretic-run heretic /workspace/scripts/run-heretic.sh
```

The runner chooses the first Pareto-optimal trial when optimization completes,
selects "Save the model to a local folder", and exports a merged model to:

```text
output/Ornith-1.0-35B-heretic
```

Follow logs:

```bash
docker logs -f ornith-heretic-run
```

Resume after interruption:

```bash
docker compose run --name ornith-heretic-run heretic /workspace/scripts/run-heretic.sh
```

## HF token

If Hugging Face access needs a token, do not put it in this repo. Login inside a
throwaway Docker run or pass it via the shell environment:

```bash
docker compose run --rm -e HF_TOKEN heretic hf auth whoami
```
