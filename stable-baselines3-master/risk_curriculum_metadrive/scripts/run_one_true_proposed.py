#!/usr/bin/env python
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from racrl.config import get_variant_config
from racrl.experiment import evaluate, train

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--n-envs', type=int, default=24)
    parser.add_argument('--timesteps', type=int, default=1_000_000)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    args.root.mkdir(parents=True, exist_ok=True)
    (args.root / 'evaluations').mkdir(exist_ok=True)
    (args.root / 'figures').mkdir(exist_ok=True)
    run_dir = args.root / 'runs' / f'proposed_ppo_s{args.seed}'
    config = get_variant_config('proposed', 'ppo', seed=args.seed, timesteps=args.timesteps)
    config.horizon = 1200
    config.n_envs = args.n_envs
    config.stage2_success = 0.50
    config.stage2_cost = 0.30
    config.demote_grace_episodes = 20
    config.allow_demote = True
    model_path = train(config, run_dir, device='cuda')
    evaluate(config, model_path, args.root / 'evaluations' / f'proposed_ppo_s{args.seed}.csv', device='cuda', densities=(0.00, 0.08, 0.15), episodes=50)
    for cmd in [
        ['scripts/plot_results.py', '--input-dir', str(args.root / 'evaluations'), '--output-dir', str(args.root / 'figures'), '--runs-dir', str(args.root / 'runs')],
        ['scripts/plot_return_figures.py', '--runs-dir', str(args.root / 'runs'), '--eval-dir', str(args.root / 'evaluations'), '--output-dir', str(args.root / 'figures')],
        ['scripts/plot_framework_diagram.py', '--output-dir', str(args.root / 'figures')],
        ['scripts/write_run_report.py', '--experiment-root', str(args.root), '--preset', args.root.name],
    ]:
        subprocess.run(['/root/autodl-tmp/envs/sb3/bin/python', *cmd], check=True)
if __name__ == '__main__':
    main()
