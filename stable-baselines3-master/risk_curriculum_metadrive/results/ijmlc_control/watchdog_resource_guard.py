#!/usr/bin/env python3
from __future__ import annotations

import os
import signal
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path('/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive')
CTL = ROOT / 'results' / 'ijmlc_control'
LOG = CTL / 'logs' / 'resource_watchdog.log'
STATUS = CTL / '05_CURRENT_STATUS.md'
PID_FILE = CTL / 'logs' / 'resource_watchdog.pid'

MIN_MEM_AVAILABLE_GIB = float(os.environ.get('IJMLC_MIN_MEM_AVAILABLE_GIB', '3.0'))
MIN_GPU_FREE_MIB = int(os.environ.get('IJMLC_MIN_GPU_FREE_MIB', '2048'))
CHECK_INTERVAL_SEC = int(os.environ.get('IJMLC_WATCHDOG_INTERVAL_SEC', '15'))
TARGET_PATTERNS = [
    'p1_density_expand_20260701_1655',
    'evaluate_ijmlc_diagnostics.py',
    'p2_external_baselines',
    'ijmlc_p2',
    'rcpo_lagrangian',
    'rss_ttc_filter',
    'p5_sensitivity',
]


def now() -> str:
    return datetime.now().isoformat(timespec='seconds')


def append(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(text)


def mem_available_gib() -> float:
    data = Path('/proc/meminfo').read_text(encoding='utf-8').splitlines()
    vals = {}
    for line in data:
        key, rest = line.split(':', 1)
        vals[key] = float(rest.strip().split()[0])
    return vals.get('MemAvailable', 0.0) / 1024.0 / 1024.0


def gpu_free_mib() -> int | None:
    try:
        out = subprocess.check_output(
            'nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits',
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=10,
        ).strip().splitlines()[0]
        return int(float(out.strip()))
    except Exception:
        return None


def matching_pids() -> list[int]:
    out = subprocess.check_output('ps -eo pid=,ppid=,cmd=', shell=True, text=True)
    pids: list[int] = []
    self_pid = os.getpid()
    for line in out.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) < 3:
            continue
        pid = int(parts[0])
        cmd = parts[2]
        if pid == self_pid or 'resource_watchdog' in cmd:
            continue
        if any(pattern in cmd for pattern in TARGET_PATTERNS):
            pids.append(pid)
    return sorted(set(pids), reverse=True)


def stop_targets(reason: str) -> None:
    pids = matching_pids()
    append(LOG, f'[{now()}] RESOURCE_GUARD_TRIGGER reason={reason} pids={pids}\n')
    for sig in (signal.SIGTERM, signal.SIGKILL):
        for pid in pids:
            try:
                os.kill(pid, sig)
            except ProcessLookupError:
                pass
            except PermissionError as exc:
                append(LOG, f'[{now()}] permission_error pid={pid} sig={sig}: {exc}\n')
        time.sleep(5 if sig == signal.SIGTERM else 1)
    append(
        STATUS,
        f"\n\n## 资源保护触发 {now()}\n\n"
        f"- watchdog 已停止 IJMLC 当前诊断队列。\n"
        f"- 原因：{reason}\n"
        f"- 阈值：MemAvailable < {MIN_MEM_AVAILABLE_GIB:.1f} GiB 或 GPU free < {MIN_GPU_FREE_MIB} MiB。\n"
        f"- 后续训练任务需要从最近 checkpoint 或未完成 seed 继续；诊断任务降低并行 shard 数，例如从 16 降到 8/10。\n",
    )


def main() -> None:
    PID_FILE.write_text(str(os.getpid()) + '\n', encoding='utf-8')
    append(LOG, f'[{now()}] watchdog_start min_mem_available_gib={MIN_MEM_AVAILABLE_GIB} min_gpu_free_mib={MIN_GPU_FREE_MIB} interval={CHECK_INTERVAL_SEC}\n')
    while True:
        mem = mem_available_gib()
        gpu = gpu_free_mib()
        append(LOG, f'[{now()}] mem_available_gib={mem:.2f} gpu_free_mib={gpu}\n')
        if mem < MIN_MEM_AVAILABLE_GIB:
            stop_targets(f'MemAvailable {mem:.2f} GiB below {MIN_MEM_AVAILABLE_GIB:.1f} GiB')
            break
        if gpu is not None and gpu < MIN_GPU_FREE_MIB:
            stop_targets(f'GPU free {gpu} MiB below {MIN_GPU_FREE_MIB} MiB')
            break
        time.sleep(CHECK_INTERVAL_SEC)


if __name__ == '__main__':
    main()
