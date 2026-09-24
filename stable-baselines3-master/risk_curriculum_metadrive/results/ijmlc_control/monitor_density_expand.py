#!/usr/bin/env python3
from __future__ import annotations

import csv
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path('/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive')
CTL = ROOT / 'results' / 'ijmlc_control'
RUN_GROUP = 'p1_density_expand_20260701_1655'
OUT = CTL / 'density_expand_monitor_latest.md'
LOG = CTL / 'logs' / 'density_expand_monitor.log'
PID_FILE = CTL / 'logs' / 'density_expand_monitor.pid'
INTERVAL = 60
LABELS = ['baseline', 'risk_only', 'guard_only', 'shield_only', 'gated_risk', 'no_action_guard']
SEEDS = [0, 1, 2]


def sh(cmd: str) -> str:
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT, timeout=20).strip()
    except Exception as exc:
        return f'ERROR: {exc}'


def done_rows() -> list[str]:
    lines = []
    for p in sorted((CTL / 'logs').glob(f'{RUN_GROUP}_*.log')):
        txt = p.read_text(encoding='utf-8', errors='replace')
        for line in txt.splitlines():
            if 'done label=' in line:
                lines.append(line)
    return lines


def exit_rows() -> list[str]:
    lines = []
    for p in sorted((CTL / 'logs').glob(f'{RUN_GROUP}_*.log')):
        txt = p.read_text(encoding='utf-8', errors='replace')
        for line in txt.splitlines():
            if 'EXIT_CODE=' in line:
                lines.append(f'{p.name}: {line}')
    return lines


def build_snapshot() -> str:
    done = done_rows()
    exits = exit_rows()
    done_keys = set()
    for line in done:
        # format: [1/1] done label=baseline seed=0 ...
        parts = line.replace('=', ' ').split()
        if 'label' in parts and 'seed' in parts:
            label = parts[parts.index('label') + 1]
            seed = parts[parts.index('seed') + 1]
            done_keys.add((label, int(seed)))
    missing = [(label, seed) for label in LABELS for seed in SEEDS if (label, seed) not in done_keys]
    raw_count = len(list((CTL / 'raw_csv').glob(f'{RUN_GROUP}_*_episodes.csv')))
    manifest_count = len(list((CTL / 'run_manifests').glob(f'{RUN_GROUP}_*.json')))
    manager_pid = (CTL / 'logs' / f'{RUN_GROUP}_manager.pid').read_text(encoding='utf-8').strip() if (CTL / 'logs' / f'{RUN_GROUP}_manager.pid').exists() else 'NA'
    lines = []
    lines.append('# Density Expand Monitor')
    lines.append('')
    lines.append(f'time: {datetime.now().isoformat(timespec="seconds")}')
    lines.append(f'run_group: {RUN_GROUP}')
    lines.append('')
    lines.append('## Resource')
    lines.append(sh("awk '/MemAvailable|MemFree/ {print}' /proc/meminfo"))
    lines.append(sh('nvidia-smi --query-gpu=memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits'))
    lines.append('')
    lines.append('## Watchdog')
    lines.append(sh(f'tail -5 {CTL}/logs/resource_watchdog.log'))
    lines.append('')
    lines.append('## Progress')
    lines.append(f'done_shards: {len(done_keys)} / 18')
    lines.append(f'raw_csv_files: {raw_count}')
    lines.append(f'run_manifests: {manifest_count}')
    lines.append(f'manager_pid: {manager_pid}')
    lines.append(sh(f'ps -p {manager_pid} -o pid,stat,etime,cmd || true'))
    lines.append('')
    lines.append('## Done')
    lines.extend([f'- {line}' for line in done] or ['- none'])
    lines.append('')
    lines.append('## Missing')
    lines.extend([f'- {label} seed{seed}' for label, seed in missing] or ['- none'])
    lines.append('')
    lines.append('## Exit Codes')
    lines.extend([f'- {line}' for line in exits] or ['- none'])
    return '\n'.join(lines) + '\n'


def main() -> None:
    PID_FILE.write_text(str(Path('/proc/self').resolve().name) + '\n', encoding='utf-8')
    with LOG.open('a', encoding='utf-8') as log:
        log.write(f'[{datetime.now().isoformat(timespec="seconds")}] monitor_start\n')
    while True:
        snapshot = build_snapshot()
        OUT.write_text(snapshot, encoding='utf-8')
        with LOG.open('a', encoding='utf-8') as log:
            log.write(f'[{datetime.now().isoformat(timespec="seconds")}] snapshot_written\n')
        if 'done_shards: 18 / 18' in snapshot:
            break
        if 'RESOURCE_GUARD_TRIGGER' in (CTL / 'logs' / 'resource_watchdog.log').read_text(encoding='utf-8', errors='replace'):
            break
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()
