#!/usr/bin/env python
from __future__ import annotations
import multiprocessing as mp
import subprocess
import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from racrl.config import get_variant_config
from racrl.experiment import evaluate, train
ROOT = Path('outputs/stage1000_true_proposed_s6s7_parallel_nenv24')
def run_seed(seed: int) -> None:
    run_dir = ROOT / 'runs' / f'proposed_ppo_s{seed}'
    config = get_variant_config('proposed', 'ppo', seed=seed, timesteps=1_000_000)
    config.horizon = 1200
    config.n_envs = 24
    config.stage2_success = 0.50
    config.stage2_cost = 0.30
    config.demote_grace_episodes = 20
    config.allow_demote = True
    model_path = train(config, run_dir, device='cuda')
    evaluate(config, model_path, ROOT / 'evaluations' / f'proposed_ppo_s{seed}.csv', device='cuda', densities=(0.00, 0.08, 0.15), episodes=50)
def main() -> None:
    (ROOT / 'evaluations').mkdir(parents=True, exist_ok=True)
    (ROOT / 'figures').mkdir(parents=True, exist_ok=True)
    procs = [mp.Process(target=run_seed, args=(seed,)) for seed in (6, 7)]
    for p in procs: p.start()
    for p in procs: p.join()
    failed = [p.exitcode for p in procs if p.exitcode != 0]
    if failed:
        raise SystemExit(f'failed_exitcodes={failed}')
    commands = [
        ['scripts/plot_results.py', '--input-dir', str(ROOT / 'evaluations'), '--output-dir', str(ROOT / 'figures'), '--runs-dir', str(ROOT / 'runs')],
        ['scripts/plot_return_figures.py', '--runs-dir', str(ROOT / 'runs'), '--eval-dir', str(ROOT / 'evaluations'), '--output-dir', str(ROOT / 'figures')],
        ['scripts/plot_framework_diagram.py', '--output-dir', str(ROOT / 'figures')],
        ['scripts/write_run_report.py', '--experiment-root', str(ROOT), '--preset', 'stage1000_true_proposed_s6s7_parallel_nenv24'],
    ]
    for cmd in commands:
        subprocess.run(['/root/autodl-tmp/envs/sb3/bin/python', *cmd], check=True)
if __name__ == '__main__':
    main()
