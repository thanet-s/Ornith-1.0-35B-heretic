# Ornith-1.0-35B-heretic v3 From-base Relaxed-KL Results

Status: running on DGX Spark.

This branch is a third Heretic 1.4.0 experiment. It starts from the original
Ornith base model and relaxes the KL target to search for a lower refusal count.

## Run

```text
source_model: deepreinforce-ai/Ornith-1.0-35B
base_reference_model: deepreinforce-ai/Ornith-1.0-35B
output: output/Ornith-1.0-35B-heretic-v3-from-base
heretic: 1.4.0
n_trials: 400
n_startup_trials: 100
kl_divergence_target: 0.02
orthogonalize_direction: true
row_normalization: full
full_normalization_lora_rank: 3
study_checkpoint_dir: checkpoints-v3-from-base-relaxed-kl
runtime_checkpoint_journal: run-v3-from-base/checkpoints-v3-from-base-relaxed-kl/deepreinforce-ai--Ornith-1--0-35B.jsonl
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

## Current Progress

Last checked: 2026-07-01 18:02:08 +07:00.

```text
container: ornith-heretic-v3-from-base-relaxed-kl
source_model_verified: deepreinforce-ai/Ornith-1.0-35B
bad_source_seen: false
initial_refusals: 90/100
completed_trials: 2/400
best_trial_so_far: trial 2
best_refusals_so_far: 81/100
best_kl_so_far: 0.0005
beats_v1: false
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
docker compose run --rm --no-deps -e DRY_RUN=1 heretic /workspace/scripts/run-heretic-v3-from-base.sh
```

Run:

```bash
docker compose run --name ornith-heretic-v3-from-base-relaxed-kl heretic /workspace/scripts/run-heretic-v3-from-base.sh
```

Evaluate the exported v3 model against the original base, if accepted:

```bash
docker compose run --rm --no-deps heretic heretic \
  --model deepreinforce-ai/Ornith-1.0-35B \
  --evaluate-model /workspace/output/Ornith-1.0-35B-heretic-v3-from-base
```
