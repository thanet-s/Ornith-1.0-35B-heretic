#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import sys
import time
import tomllib
from pathlib import Path

import pexpect

from patch_heretic_v2 import patch_heretic_model_source


model_id = os.environ.get("MODEL_ID", "thanet-s/Ornith-1.0-35B-heretic")
output_dir = os.environ.get(
    "OUTPUT_DIR",
    "/workspace/output/Ornith-1.0-35B-heretic-v3-from-v1",
)
config_path = Path(os.environ.get("HERETIC_CONFIG", "/workspace/config-v3.toml"))
run_dir = Path(os.environ.get("HERETIC_RUN_DIR", "/workspace/run-v3-from-v1"))


def assert_v3_config(config: dict) -> None:
    expected = {
        "n_trials": 400,
        "n_startup_trials": 100,
        "study_checkpoint_dir": "checkpoints-v3-from-v1-relaxed-kl",
        "kl_divergence_target": 0.02,
        "orthogonalize_direction": True,
        "row_normalization": "full",
        "full_normalization_lora_rank": 3,
    }
    for key, value in expected.items():
        if config.get(key) != value:
            raise RuntimeError(f"{config_path} has {key}={config.get(key)!r}; expected {value!r}")


def prepare_run_dir() -> None:
    with config_path.open("rb") as f:
        config = tomllib.load(f)
    assert_v3_config(config)

    run_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(config_path, run_dir / "config.toml")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path("/workspace/checkpoints-v3-from-v1-relaxed-kl").mkdir(parents=True, exist_ok=True)
    Path("/workspace/plots").mkdir(parents=True, exist_ok=True)


patch_heretic_model_source()
prepare_run_dir()

cmd = [
    "heretic",
    "--model",
    model_id,
    "--export-strategy",
    "merge",
]

print(f"[runner:v3] starting: {' '.join(cmd)}", flush=True)
print(f"[runner:v3] config: {config_path}", flush=True)
print(f"[runner:v3] run_dir: {run_dir}", flush=True)
print(f"[runner:v3] output_dir: {output_dir}", flush=True)
print("[runner:v3] components: attn.o_proj, attn.out_proj, mlp.down_proj", flush=True)
print("[runner:v3] source: accepted v1 HF model", flush=True)

if os.environ.get("DRY_RUN") == "1":
    print("[runner:v3] dry run complete; not launching Heretic", flush=True)
    sys.exit(0)

child = pexpect.spawn(cmd[0], cmd[1:], cwd=str(run_dir), encoding="utf-8", timeout=None)
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
        print("[runner:v3] selecting first Pareto-optimal trial", flush=True)
        time.sleep(0.5)
        child.sendline("")
    elif idx == 1:
        if saved:
            print("[runner:v3] model saved; exiting Heretic", flush=True)
            child.sendcontrol("c")
        else:
            print("[runner:v3] selecting save action", flush=True)
            time.sleep(0.5)
            child.sendline("")
    elif idx == 2:
        print("[runner:v3] sending output path", flush=True)
        time.sleep(0.5)
        child.sendline(output_dir)
    elif idx == 3:
        print("[runner:v3] save completed", flush=True)
        saved = True
    elif idx == 4:
        break

sys.exit(child.exitstatus if child.exitstatus is not None else 0)
