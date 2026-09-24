#!/usr/bin/env python
"""Create qualitative trajectory figures from trained baseline and proposed policies."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from stable_baselines3 import PPO, SAC

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from racrl.config import get_variant_config  # noqa: E402
from racrl.envs import build_env  # noqa: E402

LABELS = {
    "baseline": "PPO",
    "proposed": "Proposed",
}


def rollout(model_path: Path, variant: str, algo: str, seed: int, density: float, horizon: int) -> pd.DataFrame:
    config = get_variant_config(variant, algo, seed)
    config.horizon = horizon
    env = build_env(config, training=False, density=density)
    algorithm = PPO if algo == "ppo" else SAC
    model = algorithm.load(str(model_path), env=env, device="cuda")
    rows: list[dict] = []
    try:
        obs, _ = env.reset(seed=config.test_start_seed)
        done = False
        step = 0
        while not done and step < horizon:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            rows.append(
                {
                    "variant": variant,
                    "method": LABELS.get(variant, variant),
                    "step": step,
                    "x": info.get("vehicle_x"),
                    "y": info.get("vehicle_y"),
                    "speed_kmh": info.get("vehicle_speed_kmh"),
                    "lane_deviation": info.get("lane_deviation"),
                    "ttc_risk": info.get("ttc_risk"),
                    "out_of_road": float(bool(info.get("out_of_road"))),
                    "collision": float(bool(info.get("crash_vehicle") or info.get("crash_object"))),
                    "success": float(bool(info.get("arrive_dest"))),
                }
            )
            done = bool(terminated or truncated)
            step += 1
    finally:
        env.close()
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-dir", type=Path, default=ROOT / "outputs" / "paper" / "runs")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "paper" / "figures")
    parser.add_argument("--algo", choices=["ppo", "sac"], default="ppo")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--density", type=float, default=0.25)
    parser.add_argument("--horizon", type=int, default=1000)
    args = parser.parse_args()

    frames = []
    for variant in ("baseline", "proposed"):
        model = args.runs_dir / f"{variant}_{args.algo}_s{args.seed}" / "model" / "final_model.zip"
        if model.exists():
            frames.append(rollout(model, variant, args.algo, args.seed, args.density, args.horizon))
    if not frames:
        raise FileNotFoundError(f"No baseline/proposed models found in {args.runs_dir}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    data = pd.concat(frames, ignore_index=True)
    data.to_csv(args.output_dir / "trajectory_rollouts.csv", index=False)

    sns.set_theme(style="whitegrid", context="paper", font_scale=1.05)
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.6), constrained_layout=True)
    sns.lineplot(data=data, x="x", y="y", hue="method", ax=axes[0], linewidth=2.0)
    axes[0].set(title="Vehicle Trajectory", xlabel="World x", ylabel="World y")
    axes[0].axis("equal")
    sns.lineplot(data=data, x="step", y="lane_deviation", hue="method", ax=axes[1], linewidth=2.0)
    axes[1].set(title="Lane Deviation", xlabel="Step", ylabel="Normalized deviation")
    legend = axes[1].get_legend()
    if legend is not None:
        legend.remove()
    fig.savefig(args.output_dir / "trajectory_visualization.pdf", bbox_inches="tight")
    fig.savefig(args.output_dir / "trajectory_visualization.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"saved_trajectory={args.output_dir / 'trajectory_visualization.pdf'}")


if __name__ == "__main__":
    main()
