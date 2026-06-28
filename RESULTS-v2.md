# Ornith-1.0-35B-heretic v2 MPOA-800 Results

Status: running or pending.

This branch is a second Heretic 1.4.0 run intended to lower refusals while
keeping KL low. It keeps the same base model and evaluation datasets as v1, but
expands the component search from the original single reported target to:

```text
attn.o_proj
attn.out_proj
mlp.down_proj
```

The `mlp.down_proj` target is Ornith's `mlp.shared_expert.down_proj` module.
The packed MoE `experts.down_proj` parameter is intentionally not targeted
because Heretic 1.4.0 applies the edit through LoRA-compatible modules.

## Planned Run

```text
model: deepreinforce-ai/Ornith-1.0-35B
output: output/Ornith-1.0-35B-heretic
heretic: 1.4.0
n_trials: 800
n_startup_trials: 200
kl_divergence_target: 0.01
orthogonalize_direction: true
row_normalization: full
full_normalization_lora_rank: 3
study_checkpoint_dir: checkpoints-v2-mpoa-800
```

## Baselines

```text
base_refusals: 90/100
v1_refusals: 53/100
v1_kl_divergence: 0.0063087488524615765
```

## Commands

Inspect components:

```bash
docker compose run --rm --no-deps heretic python3 /workspace/scripts/inspect-components-v2.py
```

Run:

```bash
docker compose run --name ornith-heretic-v2-mpoa-800 heretic /workspace/scripts/run-heretic-v2-mpoa-800.sh
```
