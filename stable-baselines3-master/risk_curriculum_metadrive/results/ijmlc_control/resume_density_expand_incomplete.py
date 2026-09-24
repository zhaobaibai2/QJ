#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path
from datetime import datetime

ROOT = Path('/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive')
CTL = ROOT / 'results' / 'ijmlc_control'
OLD_GROUP = 'p1_density_expand_20260701_1655'
NEW_GROUP = 'p1_density_expand_resume_max8_' + datetime.now().strftime('%Y%m%d_%H%M%S')
LABELS = ['baseline', 'risk_only', 'guard_only', 'shield_only', 'gated_risk', 'no_action_guard']
SEEDS = [0, 1, 2]
MAX_JOBS = 8

def complete(label: str, seed: int) -> bool:
    path = CTL / 'run_manifests' / f'{OLD_GROUP}_{label}_s{seed}.json'
    if path.exists():
        return True
    # Also allow a resumed group to satisfy completion.
    for candidate in (CTL / 'run_manifests').glob(f'p1_density_expand_resume_*_{label}_s{seed}.json'):
        if candidate.exists():
            return True
    return False

missing = [(label, seed) for label in LABELS for seed in SEEDS if not complete(label, seed)]
script = CTL / 'logs' / f'{NEW_GROUP}_manager.sh'
pid_file = CTL / 'logs' / f'{NEW_GROUP}.pids'
lines = [
    '#!/usr/bin/env bash',
    'set -u',
    f'cd {ROOT}',
    f'RUN_GROUP={NEW_GROUP}',
    f'MAX_JOBS={MAX_JOBS}',
    f'PID_FILE={pid_file}',
    ': > "$PID_FILE"',
    'launch_one() {',
    '  local label="$1"',
    '  local seed="$2"',
    '  local run_id=${RUN_GROUP}_${label}_s${seed}',
    '  local log=results/ijmlc_control/logs/${run_id}.log',
    '  (',
    '    /home/aaa/miniconda3/bin/conda run --no-capture-output -n sb3 python -u scripts/evaluate_ijmlc_diagnostics.py --labels "$label" --seeds "$seed" --densities 0.08 0.20 0.25 --test-start-seeds 10000 20000 --episodes-per-start 20 --run-id "$run_id"',
    '    rc=$?',
    '    echo "EXIT_CODE=${rc}" >> "$log"',
    '    exit $rc',
    '  ) > "$log" 2>&1 &',
    '  echo "$! $run_id $log" >> "$PID_FILE"',
    '}',
]
for label, seed in missing:
    lines.extend([
        f'while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done',
        f'launch_one {label} {seed}',
    ])
lines.append('wait')
script.write_text('\n'.join(lines) + '\n', encoding='utf-8')
script.chmod(0o755)

plan = CTL / 'RESOURCE_GUARD_RESUME_PLAN.md'
plan.write_text(
    '# 资源保护后恢复计划\n\n'
    f'更新时间：{datetime.now().isoformat(timespec="seconds")}\n\n'
    f'- 原始 run_group: `{OLD_GROUP}`\n'
    f'- 恢复 run_group: `{NEW_GROUP}`\n'
    f'- 恢复并行上限: {MAX_JOBS}\n'
    f'- 未完成 shard 数: {len(missing)}\n'
    f'- manager script: `{script}`\n\n'
    '如果 watchdog 因 MemAvailable < 3GB 停止当前队列，后续使用这个 manager 只重跑未完成 shard。\n\n'
    '待恢复 shard:\n'
    + ''.join(f'- {label} seed{seed}\n' for label, seed in missing),
    encoding='utf-8',
)
print(plan)
print(script)
print(f'missing={len(missing)}')
for label, seed in missing:
    print(label, seed)
