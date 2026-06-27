# Ornith-1.0-35B-heretic Results

Run completed on DGX Spark using this project directory.

```text
.
```

## Output

Merged model:

```text
output/Ornith-1.0-35B-heretic
```

Artifact size:

```text
66G
```

Model files:

```text
16 safetensors shards
31,666 indexed tensors
tokenizer/config/processor files present
```

## Heretic Run

Tooling:

```text
heretic-llm 1.4.0
transformers 5.12.1
Docker image ornith-heretic:1.4.0
base image nvcr.io/nvidia/pytorch:26.05-py3
```

Run summary:

```text
completed_trials: 200
initial_refusals: 90/100
selected_trial_index: 156
selected_trial_refusals: 53/100
selected_trial_kl_divergence: 0.0063087488524615765
```

Heretic found only this abliterable target on Ornith:

```text
attn.o_proj
```

## Verification

Structural verification passed:

```text
output_exists: true
missing_files: []
index_tensors: 31666
index_shards: 16
missing_shards: []
shard_tensors: 31666
weight_map_matches_shards: true
tokenizer_vocab: 248077
processor: Qwen3VLProcessor
```

Full CPU reload verification passed:

```text
loaded_class: Qwen3_5MoeForConditionalGeneration
parameters: 35107181936
first_param_dtype: torch.bfloat16
first_param_device: cpu
tokenizer_len: 248077
processor_class: Qwen3VLProcessor
```
