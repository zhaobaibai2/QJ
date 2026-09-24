#!/usr/bin/env python
"""Run proposed PPO for seeds 4 and 5 with 16 MetaDrive workers."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from racrl.config import get_variant_config
from racrl.experiment import evaluate, train
ROOT = Path('outputs/stage1000_true_proposed_s4s5_nenv16')
def run_seed(seed: int) -> None:
    run_dir = ROOT / 'runs' / f'proposed_ppo_s{seed}'
    config = get_variant_config('proposed', 'ppo', seed=seed, timesteps=1_000_000)
    config.horizon = 1200
    config.n_envs = 16
    config.stage2_success = 0.50
    config.stage2_cost = 0.30
    config.demote_grace_episodes = 20
    config.allow_demote = True
    model_path = train(config, run_dir, device='cuda')
    evaluate(config, model_path, ROOT / 'evaluations' / f'proposed_ppo_s{seed}.csv', device='cuda', densities=(0.00, 0.08, 0.15), episodes=50)
def main() -> None:
    (ROOT / 'evaluations').mkdir(parents=True, exist_ok=True)
    (ROOT / 'figures').mkdir(parents=True, exist_ok=True)
    for seed in (4, 5):
        run_seed(seed)
    commands = [
        ['scripts/plot_results.py', '--input-dir', str(ROOT / 'evaluations'), '--output-dir', str(ROOT / 'figures'), '--runs-dir', str(ROOT / 'runs')],
        ['scripts/plot_return_figures.py', '--runs-dir', str(ROOT / 'runs'), '--eval-dir', str(ROOT / 'evaluations'), '--output-dir', str(ROOT / 'figures')],
        ['scripts/plot_framework_diagram.py', '--output-dir', str(ROOT / 'figures')],
        ['scripts/write_run_report.py', '--experiment-root', str(ROOT), '--preset', 'stage1000_true_proposed_s4s5_nenv16'],
    ]
    for cmd in commands:
        subprocess.run(['/root/autodl-tmp/envs/sb3/bin/python', *cmd], check=True)
if __name__ == '__main__':
    main()
