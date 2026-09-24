#!/usr/bin/env python
"""Run stable 1M-step proposed PPO for seeds 1 and 2."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from racrl.config import get_variant_config
from racrl.experiment import evaluate, train


ROOT = Path("outputs/stage1000_stable_proposed_multiseed")


def run_seed(seed: int) -> None:
    run_dir = ROOT / "runs" / f"proposed_ppo_s{seed}"
    config = get_variant_config("proposed", "ppo", seed=seed, timesteps=1_000_000)
    config.horizon = 1200
    config.n_envs = 4
    config.stage2_success = 0.95
    config.stage2_cost = 0.10
    config.allow_demote = True
    config.demote_grace_episodes = 20
    model_path = train(config, run_dir, device="cuda")
    evaluate(
        config,
        model_path,
        ROOT / "evaluations" / f"proposed_ppo_s{seed}.csv",
        device="cuda",
        densities=(0.00, 0.08, 0.15),
        episodes=50,
    )


def main() -> None:
    (ROOT / "evaluations").mkdir(parents=True, exist_ok=True)
    (ROOT / "figures").mkdir(parents=True, exist_ok=True)
    for seed in (1, 2):
        run_seed(seed)
    commands = [
        [
            "scripts/plot_results.py",
            "--input-dir",
            str(ROOT / "evaluations"),
            "--output-dir",
            str(ROOT / "figures"),
            "--runs-dir",
            str(ROOT / "runs"),
        ],
        [
            "scripts/plot_return_figures.py",
            "--runs-dir",
            str(ROOT / "runs"),
            "--eval-dir",
            str(ROOT / "evaluations"),
            "--output-dir",
            str(ROOT / "figures"),
        ],
        ["scripts/plot_framework_diagram.py", "--output-dir", str(ROOT / "figures")],
        ["scripts/write_run_report.py", "--experiment-root", str(ROOT), "--preset", "stage1000_stable_proposed_multiseed"],
    ]
    for command in commands:
        subprocess.run(["/root/autodl-tmp/envs/sb3/bin/python", *command], check=True)


if __name__ == "__main__":
    main()
