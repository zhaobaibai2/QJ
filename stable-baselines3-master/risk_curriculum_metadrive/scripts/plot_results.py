#!/usr/bin/env python
"""Aggregate evaluation files and produce publication-oriented figures/tables."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
ORDER = ["baseline", "risk", "curriculum", "proposed"]
ABLATION_ORDER = ["proposed", "proposed_wo_ttc", "proposed_wo_lane", "proposed_wo_smooth"]
LABELS = {
    "baseline": "PPO",
    "risk": "PPO + Risk",
    "curriculum": "PPO + Curriculum",
    "proposed": "Proposed",
    "proposed_wo_ttc": "w/o TTC",
    "proposed_wo_lane": "w/o Lane",
    "proposed_wo_smooth": "w/o Smooth",
}


def _safe_legend(ax, title: str = "") -> None:
    legend = ax.get_legend()
    if legend is not None:
        legend.set_title(title)


def _mean_std(values: pd.Series) -> str:
    vals = pd.to_numeric(values, errors="coerce").dropna()
    if vals.empty:
        return "--"
    return f"{vals.mean():.3f} $\\pm$ {vals.std(ddof=0):.3f}"


def _load_tensorboard_scalars(runs_dir: Path) -> pd.DataFrame:
    try:
        from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
    except Exception:
        return pd.DataFrame()

    rows: list[dict] = []
    tags = [
        "paper/success",
        "paper/route_completion",
        "paper/episode_cost",
        "paper/shaped_reward",
        "paper/ttc_risk",
        "curriculum/stage",
    ]
    for event_file in runs_dir.glob("*_ppo_s*/tensorboard/**/events.out.tfevents.*"):
        run_name = event_file.parents[2].name
        parts = run_name.rsplit("_", 2)
        if len(parts) != 3:
            continue
        variant, algo, seed_text = parts
        if algo != "ppo":
            continue
        seed = int(seed_text.removeprefix("s"))
        accumulator = EventAccumulator(str(event_file), size_guidance={"scalars": 0})
        try:
            accumulator.Reload()
        except Exception:
            continue
        available = set(accumulator.Tags().get("scalars", []))
        for tag in tags:
            if tag not in available:
                continue
            metric = tag.split("/", 1)[1]
            for scalar in accumulator.Scalars(tag):
                rows.append(
                    {
                        "variant": variant,
                        "method": LABELS.get(variant, variant),
                        "seed": seed,
                        "step": scalar.step,
                        "metric": metric,
                        "value": scalar.value,
                    }
                )
    return pd.DataFrame(rows)


def _load_monitor_curves(runs_dir: Path) -> pd.DataFrame:
    rows = []
    for path in sorted(runs_dir.glob("*_ppo_s*/monitor.monitor.csv")):
        run_name = path.parent.name
        parts = run_name.rsplit("_", 2)
        if len(parts) != 3:
            continue
        variant, algo, seed_text = parts
        if algo != "ppo":
            continue
        frame = pd.read_csv(path, comment="#")
        if frame.empty:
            continue
        frame["variant"] = variant
        frame["method"] = frame["variant"].map(LABELS).fillna(frame["variant"])
        frame["seed"] = int(seed_text.removeprefix("s"))
        frame["episode_index"] = range(len(frame))
        for source, metric in [
            ("is_success", "success"),
            ("episode_route_completion", "route_completion"),
            ("episode_cost", "episode_cost"),
            ("episode_shaped_reward", "shaped_reward"),
            ("episode_ttc_risk", "ttc_risk"),
            ("curriculum_stage", "stage"),
        ]:
            if source in frame:
                sub = frame[["variant", "method", "seed", "episode_index", source]].copy()
                sub["metric"] = metric
                sub["value"] = sub[source]
                sub = sub.rename(columns={"episode_index": "step"})
                rows.append(sub[["variant", "method", "seed", "step", "metric", "value"]])
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def _smooth(frame: pd.DataFrame, window: int) -> pd.DataFrame:
    if frame.empty:
        return frame
    out = frame.sort_values(["variant", "seed", "metric", "step"]).copy()
    out["smooth"] = (
        out.groupby(["variant", "seed", "metric"], observed=True)["value"]
        .transform(lambda s: s.ewm(span=window, adjust=False, min_periods=1).mean())
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=ROOT / "outputs" / "evaluations")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "figures")
    parser.add_argument("--runs-dir", type=Path, default=ROOT / "outputs" / "runs")
    parser.add_argument("--smooth", type=int, default=30)
    args = parser.parse_args()
    files = sorted(path for path in args.input_dir.glob("*.csv") if path.name != "summary.csv")
    if not files:
        raise FileNotFoundError(f"No evaluation CSV files in {args.input_dir}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    data = pd.concat([pd.read_csv(path) for path in files], ignore_index=True)
    data["method"] = data["variant"].map(LABELS).fillna(data["variant"])
    summary = (
        data.groupby(["variant", "algo", "seed", "density"], as_index=False)
        .agg(
            success=("success", "mean"),
            route_completion=("route_completion", "mean"),
            collision=("collision", "mean"),
            out_of_road=("out_of_road", "mean"),
            cost=("cost", "mean"),
            reward=("reward", "mean"),
            shaped_reward=("shaped_reward", "mean"),
            episode_length=("episode_length", "mean"),
            speed=("mean_speed_kmh", "mean"),
            lane_deviation=("mean_lane_deviation", "mean"),
            steering_variation=("steering_variation", "mean"),
            accel_variation=("accel_variation", "mean"),
            ttc_risk=("ttc_risk", "mean"),
            min_ttc=("min_ttc", "mean"),
        )
    )
    summary.to_csv(args.input_dir / "summary.csv", index=False)

    sns.set_theme(style="whitegrid", context="paper", font_scale=1.12)
    palette = {LABELS[key]: color for key, color in zip(ORDER, sns.color_palette("colorblind", n_colors=4))}
    ppo = data[(data["algo"] == "ppo") & (data["variant"].isin(ORDER))].copy()
    ppo["method"] = pd.Categorical(ppo["method"], [LABELS[x] for x in ORDER], ordered=True)

    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.4), constrained_layout=True)
    sns.barplot(data=ppo, x="method", y="success", hue="density", ax=axes[0], palette="Blues", errorbar="se")
    sns.barplot(data=ppo, x="method", y="route_completion", hue="density", ax=axes[1], palette="Greens", errorbar="se")
    sns.barplot(data=ppo, x="method", y="out_of_road", hue="density", ax=axes[2], palette="Reds", errorbar="se")
    axes[0].set(title="Success", ylabel="Rate", xlabel="")
    axes[1].set(title="Route Completion", ylabel="Ratio", xlabel="")
    axes[2].set(title="Out-of-road", ylabel="Rate", xlabel="")
    _safe_legend(axes[0], "Density")
    for ax in axes[1:]:
        legend = ax.get_legend()
        if legend is not None:
            legend.remove()
    for ax in axes:
        ax.tick_params(axis="x", rotation=18)
        ax.set_ylim(0, 1)
    fig.savefig(args.output_dir / "main_unseen_metrics.pdf", bbox_inches="tight")
    fig.savefig(args.output_dir / "main_unseen_metrics.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.4), constrained_layout=True)
    sns.pointplot(data=ppo, x="density", y="cost", hue="method", ax=axes[0], palette=palette, errorbar="se")
    sns.pointplot(data=ppo, x="density", y="ttc_risk", hue="method", ax=axes[1], palette=palette, errorbar="se")
    sns.pointplot(data=ppo, x="density", y="steering_variation", hue="method", ax=axes[2], palette=palette, errorbar="se")
    axes[0].set(title="Episode Cost", xlabel="Traffic Density", ylabel="Cost")
    axes[1].set(title="TTC Risk", xlabel="Traffic Density", ylabel="Risk")
    axes[2].set(title="Steering Variation", xlabel="Traffic Density", ylabel="Mean |Delta steer|")
    _safe_legend(axes[0])
    for ax in axes[1:]:
        legend = ax.get_legend()
        if legend is not None:
            legend.remove()
    fig.savefig(args.output_dir / "robustness_control.pdf", bbox_inches="tight")
    fig.savefig(args.output_dir / "robustness_control.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    curves = _load_tensorboard_scalars(args.runs_dir)
    curve_source = "tensorboard"
    if curves.empty:
        curves = _load_monitor_curves(args.runs_dir)
        curve_source = "monitor"
    curves = curves[curves["variant"].isin(ORDER)].copy()
    curves = _smooth(curves, args.smooth)
    if not curves.empty:
        fig, axes = plt.subplots(2, 2, figsize=(10.5, 6.2), constrained_layout=True)
        metric_titles = [
            ("success", "Training Success", "Success Rate"),
            ("route_completion", "Route Completion", "Completion"),
            ("episode_cost", "Safety Cost", "Cost"),
            ("shaped_reward", "Shaped Reward", "Reward"),
        ]
        for ax, (metric, title, ylabel) in zip(axes.flat, metric_titles):
            sub = curves[curves["metric"] == metric]
            if sub.empty:
                continue
            sns.lineplot(data=sub, x="step", y="smooth", hue="method", ax=ax, palette=palette, errorbar="se")
            ax.set(title=title, xlabel="Timesteps" if curve_source == "tensorboard" else "Episode", ylabel=ylabel)
            _safe_legend(ax)
        for ax in axes.flat[1:]:
            legend = ax.get_legend()
            if legend is not None:
                legend.remove()
        fig.savefig(args.output_dir / "training_curves.pdf", bbox_inches="tight")
        fig.savefig(args.output_dir / "training_curves.png", dpi=300, bbox_inches="tight")
        plt.close(fig)

        stage = curves[curves["metric"] == "stage"]
        if not stage.empty:
            fig, ax = plt.subplots(figsize=(6.8, 3.2), constrained_layout=True)
            sns.lineplot(data=stage, x="step", y="smooth", hue="method", ax=ax, palette=palette, errorbar=None)
            ax.set(title="Curriculum Stage", xlabel="Timesteps" if curve_source == "tensorboard" else "Episode", ylabel="Stage")
            ax.set_yticks(np.arange(0, max(4, int(stage["smooth"].max()) + 1)))
            _safe_legend(ax)
            fig.savefig(args.output_dir / "curriculum_stage.pdf", bbox_inches="tight")
            fig.savefig(args.output_dir / "curriculum_stage.png", dpi=300, bbox_inches="tight")
            plt.close(fig)

    ablation = data[(data["algo"] == "ppo") & (data["variant"].isin(ABLATION_ORDER))].copy()
    if ablation["variant"].nunique() > 1:
        ablation["method"] = pd.Categorical(ablation["variant"].map(LABELS), [LABELS[x] for x in ABLATION_ORDER], ordered=True)
        fig, axes = plt.subplots(1, 3, figsize=(10.8, 3.3), constrained_layout=True)
        sns.barplot(data=ablation, x="method", y="success", ax=axes[0], color="#4C78A8", errorbar="se")
        sns.barplot(data=ablation, x="method", y="collision", ax=axes[1], color="#E45756", errorbar="se")
        sns.barplot(data=ablation, x="method", y="steering_variation", ax=axes[2], color="#72B7B2", errorbar="se")
        axes[0].set(title="Success", xlabel="", ylabel="Rate")
        axes[1].set(title="Collision", xlabel="", ylabel="Rate")
        axes[2].set(title="Steering Variation", xlabel="", ylabel="Mean |Delta steer|")
        for ax in axes:
            ax.tick_params(axis="x", rotation=18)
        fig.savefig(args.output_dir / "ablation_metrics.pdf", bbox_inches="tight")
        fig.savefig(args.output_dir / "ablation_metrics.png", dpi=300, bbox_inches="tight")
        plt.close(fig)

    main_density = float(data["density"].max())
    main = data[(data["algo"] == "ppo") & (data["variant"].isin(ORDER)) & (data["density"] == main_density)].copy()
    table = (
        main.groupby("variant")
        .agg(
            Method=("method", "first"),
            Success=("success", _mean_std),
            Route=("route_completion", _mean_std),
            Collision=("collision", _mean_std),
            OutRoad=("out_of_road", _mean_std),
            Cost=("cost", _mean_std),
            Reward=("reward", _mean_std),
        )
        .reset_index()
    )
    table["order"] = table["variant"].map({name: i for i, name in enumerate(ORDER)})
    table = table.sort_values("order")[["Method", "Success", "Route", "Collision", "OutRoad", "Cost", "Reward"]]
    table_path = ROOT / "paper" / "generated_results.tex"
    table_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_latex(table_path, index=False, escape=False, column_format="lcccccc")

    print(summary.groupby(["variant", "algo", "density"]).mean(numeric_only=True).to_string())
    print(f"curve_source={curve_source}")
    print(f"saved_summary={args.input_dir / 'summary.csv'}")
    print(f"saved_figures={args.output_dir}")


if __name__ == "__main__":
    main()
