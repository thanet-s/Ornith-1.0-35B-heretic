# Ornith-1.0-35B-heretic v2 MPOA-800 Results

Status: completed, not accepted as the release candidate.

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

## Run

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

## Outcome

```text
completed_trials: 800/800
selected_trial: 351
selected_trial_refusals: 59/100
selected_trial_kl_divergence: 0.0027
beat_v1_low_kl: false
container_exit_code: 0
saved_output: output/Ornith-1.0-35B-heretic
```

Heretic's final Pareto menu selected trial 351 as the best refusal/KL tradeoff:

```text
[Trial 351] Refusals: 59/100, KL divergence: 0.0027
```

This improves the base model's refusal count but does not beat the current v1
release, so this output should not be uploaded over the current HF model.

## Baselines

```text
base_refusals: 90/100
v1_refusals: 53/100
v1_kl_divergence: 0.0063087488524615765
```

## Notes

The lower KL score means the v2 run preserved the base model more strongly than
v1, but that also limited how much refusal behavior moved. Expanding the search
to `attn.out_proj` and `mlp.shared_expert.down_proj` did not find a better
low-KL direction than the existing v1 run. The packed MoE expert down projection
was not edited because Heretic 1.4.0 applies edits through LoRA-compatible
modules, while Ornith exposes that target as a packed tensor parameter.

For another attempt, keep v1 as the release baseline and run a separate v3
experiment instead of promoting this output.

## Commands

Inspect components:

```bash
docker compose run --rm --no-deps heretic python3 /workspace/scripts/inspect-components-v2.py
```

Run:

```bash
docker compose run --name ornith-heretic-v2-mpoa-800 heretic /workspace/scripts/run-heretic-v2-mpoa-800.sh
```
