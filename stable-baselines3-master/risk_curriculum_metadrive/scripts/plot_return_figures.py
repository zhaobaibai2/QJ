#!/usr/bin/env python
"""Plot training return curves and evaluation return bars."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_scalars(runs_dir: Path) -> pd.DataFrame:
    from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

    rows: list[dict] = []
    tags = {"paper/base_reward": "base_return", "paper/shaped_reward": "shaped_return"}
    for event_file in runs_dir.glob("**/events.out.tfevents.*"):
        run_name = event_file.parents[2].name if len(event_file.parents) > 2 else event_file.parent.name
        accumulator = EventAccumulator(str(event_file), size_guidance={"scalars": 0})
        try:
            accumulator.Reload()
        except Exception:
            continue
        available = set(accumulator.Tags().get("scalars", []))
        for tag, metric in tags.items():
            if tag not in available:
                continue
            for scalar in accumulator.Scalars(tag):
                rows.append({"run": run_name, "step": scalar.step, "metric": metric, "return": scalar.value})
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-dir", type=Path, required=True)
    parser.add_argument("--eval-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--smooth", type=int, default=30)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="paper")

    curves = load_scalars(args.runs_dir)
    if not curves.empty:
        curves = curves.sort_values(["run", "metric", "step"])
        curves["smooth_return"] = curves.groupby(["run", "metric"])["return"].transform(
            lambda s: s.ewm(span=args.smooth, adjust=False).mean()
        )
        fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
        sns.lineplot(data=curves, x="step", y="smooth_return", hue="metric", ax=ax, errorbar=None)
        ax.set(title="Training Return", xlabel="Timesteps", ylabel="Episode return")
        fig.savefig(args.output_dir / "training_return_curve.pdf", bbox_inches="tight")
        fig.savefig(args.output_dir / "training_return_curve.png", dpi=300, bbox_inches="tight")
        plt.close(fig)

    frames = []
    for csv_path in args.eval_dir.glob("*_ppo_s*.csv"):
        frame = pd.read_csv(csv_path)
        frames.append(frame)
    if frames:
        data = pd.concat(frames, ignore_index=True)
        for metric, ylabel, name in [
            ("reward", "Base return", "test_base_return_by_density"),
            ("shaped_reward", "Shaped return", "test_shaped_return_by_density"),
            ("success", "Success rate", "test_success_by_density"),
            ("collision", "Collision rate", "test_collision_by_density"),
        ]:
            if metric not in data:
                continue
            fig, ax = plt.subplots(figsize=(6.4, 3.6), constrained_layout=True)
            sns.barplot(data=data, x="density", y=metric, hue="variant", ax=ax, errorbar="se")
            ax.set(title=name.replace("_", " ").title(), xlabel="Traffic density", ylabel=ylabel)
            fig.savefig(args.output_dir / f"{name}.pdf", bbox_inches="tight")
            fig.savefig(args.output_dir / f"{name}.png", dpi=300, bbox_inches="tight")
            plt.close(fig)


if __name__ == "__main__":
    main()
