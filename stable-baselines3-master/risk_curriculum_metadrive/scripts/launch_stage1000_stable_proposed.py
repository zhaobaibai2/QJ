#!/usr/bin/env python
"""Run a 1M-step proposed PPO experiment with stable curriculum exposure."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from racrl.config import get_variant_config
from racrl.experiment import evaluate, train


ROOT = Path("outputs/stage1000_stable_proposed_s0")
RUN_DIR = ROOT / "runs" / "proposed_ppo_s0"


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "evaluations").mkdir(exist_ok=True)
    (ROOT / "figures").mkdir(exist_ok=True)
    config = get_variant_config("proposed", "ppo", seed=0, timesteps=1_000_000)
    config.horizon = 1200
    config.n_envs = 2
    # Train reliably through medium traffic. Hard density is evaluated as stress/OOD.
    config.stage2_success = 0.95
    config.stage2_cost = 0.10
    config.allow_demote = True
    config.demote_grace_episodes = 20
    model_path = train(config, RUN_DIR, device="cuda")
    evaluate(
        config,
        model_path,
        ROOT / "evaluations" / "proposed_ppo_s0.csv",
        device="cuda",
        densities=(0.00, 0.08, 0.15),
        episodes=50,
    )
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
        ["scripts/write_run_report.py", "--experiment-root", str(ROOT), "--preset", "stage1000_stable_proposed_s0"],
    ]
    for command in commands:
        subprocess.run(["/root/autodl-tmp/envs/sb3/bin/python", *command], check=True)


if __name__ == "__main__":
    main()
