#!/usr/bin/env python3
from __future__ import annotations

import os
from collections import Counter
from contextlib import suppress

import torch
from accelerate import init_empty_weights
from torch import Tensor
from torch.nn import Module
from transformers import AutoConfig, AutoModelForImageTextToText

from patch_heretic_v2 import patch_heretic_model_source


def get_attr_path(obj, path: str):
    cur = obj
    for part in path.split("."):
        cur = getattr(cur, part)
    return cur


def find_layers(model):
    for path in (
        "model.language_model.layers",
        "language_model.model.layers",
        "model.model.layers",
        "model.layers",
    ):
        with suppress(Exception):
            layers = get_attr_path(model, path)
            if layers:
                return path, layers
    raise RuntimeError("Could not find transformer layers.")


def main() -> None:
    patch_heretic_model_source()

    model_id = os.environ.get("MODEL_ID", "deepreinforce-ai/Ornith-1.0-35B")
    config = AutoConfig.from_pretrained(model_id)

    with init_empty_weights():
        model = AutoModelForImageTextToText.from_config(config)

    layer_path, layers = find_layers(model)
    component_counts: Counter[str] = Counter()
    suffix_counts: Counter[str] = Counter()
    packed_expert_shapes: Counter[str] = Counter()

    def try_add(component: str, module) -> None:
        if isinstance(module, Module):
            component_counts[component] += 1
            suffix_counts[module.__class__.__name__] += 1
        elif isinstance(module, Tensor):
            packed_expert_shapes[f"{component}: {tuple(module.shape)}"] += 1

    for layer in layers:
        with suppress(Exception):
            try_add("attn.o_proj", layer.self_attn.o_proj)
        with suppress(Exception):
            try_add("attn.out_proj", layer.linear_attn.out_proj)
        with suppress(Exception):
            try_add("mlp.down_proj", layer.mlp.down_proj)
        with suppress(Exception):
            try_add("mlp.down_proj", layer.mlp.shared_expert.down_proj)
        with suppress(Exception):
            for expert in layer.mlp.experts:
                try_add("mlp.down_proj", expert.down_proj)
        with suppress(Exception):
            try_add("packed_experts.down_proj", layer.mlp.experts.down_proj)

    print(f"model_id: {model_id}")
    print(f"config_class: {config.__class__.__name__}")
    print(f"model_type: {config.model_type}")
    print(f"layers_path: {layer_path}")
    print(f"layers: {len(layers)}")
    print("components:")
    for component, count in sorted(component_counts.items()):
        print(f"  {component}: {count}")
    print("module_classes:")
    for name, count in sorted(suffix_counts.items()):
        print(f"  {name}: {count}")
    print("non_lora_packed_tensors:")
    for name, count in sorted(packed_expert_shapes.items()):
        print(f"  {name}: {count}")


if __name__ == "__main__":
    main()
