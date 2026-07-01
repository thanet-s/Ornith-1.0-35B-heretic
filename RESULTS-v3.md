# Ornith-1.0-35B-heretic v3 From-v1 Relaxed-KL Results

Status: prepared, not yet evaluated.

This branch is a third Heretic 1.4.0 experiment. Unlike v2, it starts from the
accepted v1 Heretic model instead of the original base model, and relaxes the KL
target to search for a lower refusal count.

## Run

```text
source_model: thanet-s/Ornith-1.0-35B-heretic
base_reference_model: deepreinforce-ai/Ornith-1.0-35B
output: output/Ornith-1.0-35B-heretic-v3-from-v1
heretic: 1.4.0
n_trials: 400
n_startup_trials: 100
kl_divergence_target: 0.02
orthogonalize_direction: true
row_normalization: full
full_normalization_lora_rank: 3
study_checkpoint_dir: checkpoints-v3-from-v1-relaxed-kl
```

## Baselines

```text
base_refusals: 90/100
v1_refusals: 53/100
v1_kl_divergence_vs_base: 0.0063087488524615765
v2_selected_trial: 351
v2_refusals: 59/100
v2_kl_divergence: 0.0027
```

## Acceptance Gate

Do not promote this branch unless it beats v1:

```text
required_refusals: <53/100
ideal_refusals: 20-35/100
capability_gate: coding, tool-use, vision, harmless chat
```

## Components

The active Heretic component patch exposes:

```text
attn.o_proj -> layer.self_attn.o_proj
attn.out_proj -> layer.linear_attn.out_proj
mlp.down_proj -> layer.mlp.shared_expert.down_proj
```

The packed MoE expert down projection remains excluded for this run:

```text
layer.mlp.experts.down_proj
```

Heretic 1.4.0 applies edits through LoRA-compatible modules. Ornith exposes the
packed MoE expert down projection as a tensor parameter rather than an
`nn.Module`, so it is not safely editable by the current component patch.

## Commands

Dry run:

```bash
docker compose run --rm --no-deps -e DRY_RUN=1 heretic /workspace/scripts/run-heretic-v3-from-v1.sh
```

Run:

```bash
docker compose run --name ornith-heretic-v3-from-v1-relaxed-kl heretic /workspace/scripts/run-heretic-v3-from-v1.sh
```

Evaluate the exported v3 model against the original base, if accepted:

```bash
docker compose run --rm --no-deps heretic heretic \
  --model deepreinforce-ai/Ornith-1.0-35B \
  --evaluate-model /workspace/output/Ornith-1.0-35B-heretic-v3-from-v1
```
