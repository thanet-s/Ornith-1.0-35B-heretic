#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import heretic.model as heretic_model


PATCH_MARKER = "Ornith v2 MPOA component patch"


def patch_heretic_model_source() -> Path:
    """Patch Heretic 1.4.0 component discovery inside the running container."""
    path = Path(heretic_model.__file__)
    text = path.read_text()

    if PATCH_MARKER in text:
        print(f"[patch] Heretic model.py already patched: {path}", flush=True)
        return path

    old_linear_attn = (
        '            try_add("attn.o_proj", layer.linear_attn.out_proj)'
        "  # ty:ignore[possibly-missing-attribute]"
    )
    new_linear_attn = (
        '            try_add("attn.out_proj", layer.linear_attn.out_proj)'
        "  # ty:ignore[possibly-missing-attribute]"
    )
    if old_linear_attn not in text:
        raise RuntimeError("Could not find Heretic linear_attn out-projection hook.")
    text = text.replace(old_linear_attn, new_linear_attn, 1)

    dense_anchor = """        # Most dense models.
        with suppress(Exception):
            try_add("mlp.down_proj", layer.mlp.down_proj)  # ty:ignore[possibly-missing-attribute]

        # Some MoE models (e.g. Qwen3).
"""
    shared_expert_block = f"""        # Most dense models.
        with suppress(Exception):
            try_add("mlp.down_proj", layer.mlp.down_proj)  # ty:ignore[possibly-missing-attribute]

        # {PATCH_MARKER}: Ornith/Qwen3.5 MoE exposes the shared expert down
        # projection as an nn.Module. The packed experts.down_proj parameter is
        # a Tensor, so Heretic 1.4.0 LoRA patching cannot safely target it.
        with suppress(Exception):
            try_add("mlp.down_proj", layer.mlp.shared_expert.down_proj)  # ty:ignore[possibly-missing-attribute]

        # Some MoE models (e.g. Qwen3).
"""
    if dense_anchor not in text:
        raise RuntimeError("Could not find Heretic dense MLP down-projection hook.")
    text = text.replace(dense_anchor, shared_expert_block, 1)

    path.write_text(text)
    print(f"[patch] patched Heretic model.py: {path}", flush=True)
    return path


if __name__ == "__main__":
    patch_heretic_model_source()
