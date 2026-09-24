#!/usr/bin/env python3
from __future__ import annotations
import csv, subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path('/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive')
CTL=ROOT/'results/ijmlc_control'
P2=CTL/'p2_external_baselines'
OUT=CTL/'p2_external_monitor_latest.md'
RUN_GROUP='ijmlc_p2_external_20260701_1733'

def sh(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT, timeout=10).strip()
    except Exception as e:
        return f'ERR: {e}'

def read_csv(path):
    if not path.exists():
        return []
    return list(csv.DictReader(path.open(newline='', encoding='utf-8')))

def main():
    lines=[f'# P2 External Baseline Monitor\n\ntime: {datetime.now().isoformat(timespec="seconds")}\nrun_group: {RUN_GROUP}\n\n']
    lines.append('## Resource\n')
    lines.append('```\n'+sh('free -h')+'\n'+sh('nvidia-smi --query-gpu=index,memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits')+'\n```\n')
    lines.append('\n## Watchdog\n```\n'+sh('tail -n 8 '+str(CTL/'logs/resource_watchdog.log'))+'\n```\n')
    lines.append('\n## Processes\n```\n'+sh("ps -eo pid,stat,etime,cmd | grep -E '[i]jmlc_p2|[r]cpo_lagrangian|[r]ss_ttc_filter|[e]valuate_ijmlc_diagnostics.py' | head -80")+'\n```\n')
    lines.append('\n## RCPO Training\n')
    rcpo=read_csv(P2/'rcpo_train_status.csv')
    if rcpo:
        for r in rcpo:
            lines.append(f"- seed {r.get('seed')}: {r.get('status')} exit={r.get('exit_code')} model={r.get('model_path')}\n")
    else:
        lines.append('- not started or status not written yet\n')
    man=P2/'p2_rcpo_lagrangian_manifest.csv'
    if man.exists():
        lines.append(f'- rcpo_manifest_rows: {max(sum(1 for _ in man.open())-1,0)}\n')
    lines.append('\n## RSS/TTC Evaluation\n')
    rss=read_csv(P2/'rss_ttc_eval_status.csv')
    if rss:
        for r in rss:
            raw=ROOT/r.get('raw_csv','') if r.get('raw_csv') else Path()
            rows='NA'
            if raw.exists():
                try: rows=str(max(sum(1 for _ in raw.open())-1,0))
                except Exception: rows='ERR'
            lines.append(f"- seed {r.get('seed')}: {r.get('status')} exit={r.get('exit_code')} rows={rows} run_id={r.get('run_id')}\n")
    else:
        lines.append('- not started or status not written yet\n')
    OUT.write_text(''.join(lines), encoding='utf-8')
    print(OUT)

if __name__=='__main__':
    main()
