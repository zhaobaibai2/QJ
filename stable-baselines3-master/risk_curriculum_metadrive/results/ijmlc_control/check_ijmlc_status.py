#!/usr/bin/env python3
from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path('/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive')
CTL = ROOT / 'results' / 'ijmlc_control'

def run(cmd: str) -> str:
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT, timeout=20).strip()
    except Exception as exc:
        return f'ERROR: {exc}'

def count(path: Path, pattern: str) -> int:
    return len(list(path.glob(pattern))) if path.exists() else 0

queue = CTL / '03_RUN_QUEUE.csv'
queue_rows = []
if queue.exists():
    with queue.open(newline='', encoding='utf-8') as f:
        queue_rows = list(csv.DictReader(f))

lines: list[str] = []
lines.append('# IJMLC Supervision Snapshot')
lines.append('')
lines.append(f'time: {datetime.now().isoformat(timespec="seconds")}')
lines.append(f'root: {ROOT}')
lines.append('')
lines.append('## GPU')
lines.append(run('nvidia-smi --query-gpu=index,name,memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits'))
lines.append('')
lines.append('## Active MetaDrive/Python Jobs')
procs = run("ps -eo pid,ppid,stat,etime,pcpu,pmem,cmd | grep -E 'python|train|evaluate|metadrive|risk_curriculum' | grep -v grep | grep -v check_ijmlc_status | head -80")
lines.append(procs if procs else 'none')
lines.append('')
lines.append('## IJMLC Files')
lines.append(f'raw_csv: {count(CTL / "raw_csv", "*.csv")}')
lines.append(f'summary_tables: {count(CTL / "summary_tables", "*.csv")}')
lines.append(f'run_manifests: {count(CTL / "run_manifests", "*.json")}')
lines.append('')
lines.append('## Queue')
for row in queue_rows:
    lines.append(f'- {row.get("priority")}: {row.get("run_group")} / {row.get("method")} / {row.get("status_now")} / next={row.get("next_action")}')

out = CTL / 'supervision_snapshot_latest.md'
out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(out)
