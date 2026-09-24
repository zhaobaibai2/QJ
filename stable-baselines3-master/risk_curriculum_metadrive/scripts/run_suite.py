#!/usr/bin/env python
"""Run reproducible smoke or paper experiment suites as isolated processes."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def execute(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=ROOT, env=os.environ.copy())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", choices=["smoke", "pilot", "tuning", "validation", "million", "paper", "ablation"], default="paper")
    parser.add_argument("--include-sac", action="store_true")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--n-envs", type=int, default=int(os.environ.get("N_ENVS", "1")))
    args = parser.parse_args()
    if args.preset == "smoke":
        variants, seeds, timesteps, episodes, horizon = ["baseline", "proposed"], [0], 2_048, 2, 150
    elif args.preset == "pilot":
        variants, seeds, timesteps, episodes, horizon = ["proposed"], [0], 100_000, 20, 800
    elif args.preset == "tuning":
        variants, seeds, timesteps, episodes, horizon = ["proposed"], [0], 300_000, 30, 1000
    elif args.preset == "validation":
        variants, seeds, timesteps, episodes, horizon = ["baseline", "risk", "curriculum", "proposed"], [0], 500_000, 30, 1000
    elif args.preset == "million":
        variants, seeds, timesteps, episodes, horizon = ["proposed"], [0], 1_000_000, 50, 1000
    elif args.preset == "ablation":
        variants, seeds, timesteps, episodes, horizon = ["proposed", "proposed_wo_ttc", "proposed_wo_lane", "proposed_wo_smooth"], [0, 1, 2], 1_000_000, 50, 1000
    else:
        variants, seeds, timesteps, episodes, horizon = ["baseline", "risk", "curriculum", "proposed"], [0, 1, 2], 1_000_000, 50, 1000
    experiment_root = ROOT / "outputs" / args.preset
    runs_dir = experiment_root / "runs"
    evaluations_dir = experiment_root / "evaluations"
    figures_dir = experiment_root / "figures"
    algos = ["ppo"] + (["sac"] if args.include_sac else [])
    py = sys.executable
    execute([py, "scripts/check_env.py", "--require-gpu"])
    for algo in algos:
        for variant in variants:
            for seed in seeds:
                model = runs_dir / f"{variant}_{algo}_s{seed}" / "model" / "final_model.zip"
                eval_csv = evaluations_dir / f"{variant}_{algo}_s{seed}.csv"
                if args.skip_existing and model.exists() and eval_csv.exists():
                    print(f"skip_existing={variant}_{algo}_s{seed}", flush=True)
                    continue
                execute(
                    [
                        py, "scripts/train.py", "--variant", variant, "--algo", algo, "--seed", str(seed),
                        "--timesteps", str(timesteps), "--horizon", str(horizon), "--device", args.device,
                        "--output-dir", str(runs_dir), "--n-envs", str(args.n_envs),
                    ]
                )
                execute(
                    [
                        py, "scripts/evaluate.py", "--model", str(model), "--variant", variant, "--algo", algo,
                        "--seed", str(seed), "--episodes", str(episodes), "--horizon", str(horizon), "--device", args.device,
                        "--output-dir", str(evaluations_dir),
                    ]
                )
    execute(
        [
            py, "scripts/plot_results.py", "--input-dir", str(evaluations_dir),
            "--output-dir", str(figures_dir), "--runs-dir", str(runs_dir),
        ]
    )
    baseline = runs_dir / "baseline_ppo_s0" / "model" / "final_model.zip"
    proposed = runs_dir / "proposed_ppo_s0" / "model" / "final_model.zip"
    if baseline.exists() and proposed.exists():
        execute(
            [
                py, "scripts/plot_trajectories.py", "--runs-dir", str(runs_dir),
                "--output-dir", str(figures_dir), "--algo", "ppo", "--seed", "0", "--density", "0.25",
            ]
        )
    execute(
        [
            py, "scripts/write_run_report.py", "--experiment-root", str(experiment_root),
            "--preset", args.preset, *(["--include-sac"] if args.include_sac else []),
        ]
    )
    if args.preset in {"paper", "ablation"}:
        execute([py, "scripts/build_paper.py"])


if __name__ == "__main__":
    main()
