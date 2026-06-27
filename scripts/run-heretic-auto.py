#!/usr/bin/env python3
import os
import sys
import time

import pexpect


model_id = os.environ.get("MODEL_ID", "deepreinforce-ai/Ornith-1.0-35B")
output_dir = os.environ.get("OUTPUT_DIR", "/workspace/output/Ornith-1.0-35B-heretic")

os.makedirs(output_dir, exist_ok=True)

cmd = [
    "heretic",
    "--model",
    model_id,
    "--export-strategy",
    "merge",
]

print(f"[runner] starting: {' '.join(cmd)}", flush=True)
print(f"[runner] output_dir: {output_dir}", flush=True)

child = pexpect.spawn(cmd[0], cmd[1:], encoding="utf-8", timeout=None)
child.logfile = sys.stdout

saved = False
last_action = 0.0

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
        print("[runner] selecting first Pareto-optimal trial", flush=True)
        time.sleep(0.5)
        child.sendline("")
        last_action = time.time()
    elif idx == 1:
        if saved:
            print("[runner] model saved; exiting Heretic", flush=True)
            child.sendcontrol("c")
        else:
            print("[runner] selecting save action", flush=True)
            time.sleep(0.5)
            child.sendline("")
        last_action = time.time()
    elif idx == 2:
        print("[runner] sending output path", flush=True)
        time.sleep(0.5)
        child.sendline(output_dir)
        last_action = time.time()
    elif idx == 3:
        print("[runner] save completed", flush=True)
        saved = True
        last_action = time.time()
    elif idx == 4:
        break

sys.exit(child.exitstatus if child.exitstatus is not None else 0)
