#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import time
import tomllib

import pexpect

from patch_heretic_v2 import patch_heretic_model_source


model_id = os.environ.get("MODEL_ID", "deepreinforce-ai/Ornith-1.0-35B")
output_dir = os.environ.get("OUTPUT_DIR", "/workspace/output/Ornith-1.0-35B-heretic")
config_path = os.environ.get("HERETIC_CONFIG", "/workspace/config.toml")


def assert_v2_config() -> None:
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    expected = {
        "n_trials": 800,
        "n_startup_trials": 200,
        "study_checkpoint_dir": "checkpoints-v2-mpoa-800",
        "kl_divergence_target": 0.01,
        "orthogonalize_direction": True,
        "row_normalization": "full",
        "full_normalization_lora_rank": 3,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise RuntimeError(f"{config_path} has {key}={config.get(key)!r}; expected {value!r}")


patch_heretic_model_source()
assert_v2_config()
os.makedirs(output_dir, exist_ok=True)
os.makedirs("/workspace/checkpoints-v2-mpoa-800", exist_ok=True)
os.makedirs("/workspace/plots", exist_ok=True)

cmd = [
    "heretic",
    "--model",
    model_id,
    "--export-strategy",
    "merge",
]

print(f"[runner:v2] starting: {' '.join(cmd)}", flush=True)
print(f"[runner:v2] config: {config_path}", flush=True)
print(f"[runner:v2] output_dir: {output_dir}", flush=True)
print("[runner:v2] components: attn.o_proj, attn.out_proj, mlp.down_proj", flush=True)

if os.environ.get("DRY_RUN") == "1":
    print("[runner:v2] dry run complete; not launching Heretic", flush=True)
    sys.exit(0)

child = pexpect.spawn(cmd[0], cmd[1:], encoding="utf-8", timeout=None)
child.logfile = sys.stdout

saved = False

while True:
    idx = child.expect(
        [
            r"Which trial do you want to use\?",
            r"What do you want to do with the decensored model\?",
            r"Path to the folder:",
            r"Model saved to",
            pexpect.EOF,
        ]
    )

    if idx == 0:
        print("[runner:v2] selecting first Pareto-optimal trial", flush=True)
        time.sleep(0.5)
        child.sendline("")
    elif idx == 1:
        if saved:
            print("[runner:v2] model saved; exiting Heretic", flush=True)
            child.sendcontrol("c")
        else:
            print("[runner:v2] selecting save action", flush=True)
            time.sleep(0.5)
            child.sendline("")
    elif idx == 2:
        print("[runner:v2] sending output path", flush=True)
        time.sleep(0.5)
        child.sendline(output_dir)
    elif idx == 3:
        print("[runner:v2] save completed", flush=True)
        saved = True
    elif idx == 4:
        break

sys.exit(child.exitstatus if child.exitstatus is not None else 0)
