#!/usr/bin/env python3
"""Build IJMLC table/figure artifacts from frozen diagnostic CSV files."""
from __future__ import annotations

from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
CONTROL = ROOT / "results" / "ijmlc_control"
SUMMARY = CONTROL / "summary_tables" / "p1_all_density_core_aggregate.csv"
SEED_SUMMARY = CONTROL / "summary_tables" / "p1_all_density_core_seed_summary.csv"
RAW = CONTROL / "raw_csv" / "p1_all_density_core_episodes.csv"
OUT_TABLE = CONTROL / "manuscript"
OUT_FIG = CONTROL / "figures"
OUT_TABLE.mkdir(parents=True, exist_ok=True)
OUT_FIG.mkdir(parents=True, exist_ok=True)

METHOD_ORDER = ["baseline", "risk_only", "no_action_guard", "guard_only", "shield_only", "gated_risk"]
METHOD_LABELS = {
    "baseline": "PPO",
    "risk_only": "Risk-only",
    "no_action_guard": "No-action guard",
    "guard_only": "Guard",
    "shield_only": "Shield",
    "gated_risk": "Gated-risk",
}
COLORS = {
    "baseline": "#4C78A8",
    "risk_only": "#B279A2",
    "no_action_guard": "#F58518",
    "guard_only": "#54A24B",
    "shield_only": "#72B7B2",
    "gated_risk": "#E45756",
}
MARKERS = {"baseline": "o", "risk_only": "X", "no_action_guard": "s", "guard_only": "^", "shield_only": "D", "gated_risk": "P"}


def method_sort_key(label: str) -> int:
    return METHOD_ORDER.index(label) if label in METHOD_ORDER else len(METHOD_ORDER)


def pct(x: float) -> float:
    return float(x) * 100.0


def add_method_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["method"] = out["label"].map(METHOD_LABELS).fillna(out["label"])
    out["method_order"] = out["label"].map(lambda x: method_sort_key(str(x)))
    return out.sort_values(["density", "method_order"]).drop(columns=["method_order"])


def seed_std(seed: pd.DataFrame, density: float, metric: str) -> pd.Series:
    tmp = seed[seed["density"].round(6).eq(round(density, 6))]
    return tmp.groupby("label")[metric].std(ddof=1)


def build_tables(agg: pd.DataFrame, seed: pd.DataFrame, raw: pd.DataFrame) -> dict[str, Path]:
    outputs: dict[str, Path] = {}
    agg = add_method_columns(agg)

    d015 = agg[np.isclose(agg["density"], 0.15)].copy()
    for metric in ["success", "cost", "route_completion", "low_progress", "stop_ratio", "ttc_dangerous_fraction"]:
        d015[f"{metric}_seed_std"] = d015["label"].map(seed_std(seed, 0.15, metric))
    table3 = pd.DataFrame({
        "method": d015["method"],
        "episodes": d015["episodes"],
        "train_seeds": d015["train_seeds"],
        "success_pct": d015["success"].map(pct),
        "success_seed_std_pct": d015["success_seed_std"].map(pct),
        "cost_pct": d015["cost"].map(pct),
        "cost_seed_std_pct": d015["cost_seed_std"].map(pct),
        "route_completion_pct": d015["route_completion"].map(pct),
        "route_seed_std_pct": d015["route_completion_seed_std"].map(pct),
        "low_progress_pct": d015["low_progress"].map(pct),
        "stop_ratio_pct": d015["stop_ratio"].map(pct),
        "mean_speed_kmh": d015["mean_speed_kmh"],
        "ttc_dangerous_pct": d015["ttc_dangerous_fraction"].map(pct),
        "interventions_per_100_steps": d015["intervention_rate_per_100_steps"],
        "control_loop_p95_ms": d015["control_loop_wall_ms_p95"],
    }).round(3)
    p = OUT_TABLE / "table3_core_d015_main_diagnostics.csv"
    table3.to_csv(p, index=False)
    outputs["table3_csv"] = p
    ptex = OUT_TABLE / "table3_core_d015_main_diagnostics.tex"
    table3.to_latex(ptex, index=False, escape=True, float_format="%.3f")
    outputs["table3_tex"] = ptex

    density_table = pd.DataFrame({
        "density": agg["density"],
        "method": agg["method"],
        "episodes": agg["episodes"],
        "success_pct": agg["success"].map(pct),
        "cost_pct": agg["cost"].map(pct),
        "route_completion_pct": agg["route_completion"].map(pct),
        "collision_pct": agg["collision"].map(pct),
        "out_of_road_pct": agg["out_of_road"].map(pct),
        "low_progress_pct": agg["low_progress"].map(pct),
        "mean_speed_kmh": agg["mean_speed_kmh"],
        "ttc_dangerous_pct": agg["ttc_dangerous_fraction"].map(pct),
        "interventions_per_100_steps": agg["intervention_rate_per_100_steps"],
    }).round(3)
    p = OUT_TABLE / "table6_density_stress_summary.csv"
    density_table.to_csv(p, index=False)
    outputs["table6_csv"] = p
    ptex = OUT_TABLE / "table6_density_stress_summary.tex"
    density_table.to_latex(ptex, index=False, escape=True, float_format="%.3f")
    outputs["table6_tex"] = ptex

    runtime = agg[[
        "label", "method", "density", "episodes", "policy_inference_ms_mean", "policy_inference_ms_p95",
        "control_loop_wall_ms_mean", "control_loop_wall_ms_p95", "intervention_rate_per_100_steps",
        "intervention_rate_per_km"
    ]].copy()
    base = runtime[runtime["label"].eq("baseline")].set_index("density")
    runtime["delta_policy_mean_vs_ppo_ms"] = runtime.apply(lambda r: r["policy_inference_ms_mean"] - base.loc[r["density"], "policy_inference_ms_mean"], axis=1)
    runtime["delta_control_p95_vs_ppo_ms"] = runtime.apply(lambda r: r["control_loop_wall_ms_p95"] - base.loc[r["density"], "control_loop_wall_ms_p95"], axis=1)
    runtime = runtime.drop(columns=["label"]).round(3)
    p = OUT_TABLE / "table7_runtime_overhead.csv"
    runtime.to_csv(p, index=False)
    outputs["table7_csv"] = p
    ptex = OUT_TABLE / "table7_runtime_overhead.tex"
    runtime.to_latex(ptex, index=False, escape=True, float_format="%.3f")
    outputs["table7_tex"] = ptex

    non_motion = agg[[
        "density", "label", "method", "episodes", "success", "cost", "route_completion", "mean_speed_kmh",
        "median_speed_kmh", "stop_ratio", "low_progress", "ttc_dangerous_fraction"
    ]].copy()
    for col in ["success", "cost", "route_completion", "stop_ratio", "low_progress", "ttc_dangerous_fraction"]:
        non_motion[col + "_pct"] = non_motion[col].map(pct)
    p = OUT_TABLE / "table_supp_non_motion_artifact.csv"
    non_motion.round(4).to_csv(p, index=False)
    outputs["non_motion_csv"] = p

    fig2_data = non_motion[np.isclose(non_motion["density"], 0.15)].copy()
    p = OUT_TABLE / "figure2_non_motion_artifact_data.csv"
    fig2_data.round(4).to_csv(p, index=False)
    outputs["fig2_data"] = p

    fig3_data = agg[np.isclose(agg["density"], 0.15)][[
        "label", "method", "density", "episodes", "success", "cost", "route_completion", "low_progress",
        "ttc_dangerous_fraction", "intervention_rate_per_100_steps", "control_loop_wall_ms_p95"
    ]].copy()
    p = OUT_TABLE / "figure3_progress_safety_frontier_data.csv"
    fig3_data.round(5).to_csv(p, index=False)
    outputs["fig3_data"] = p

    fig5_data = agg[["label", "method", "density", "episodes", "success", "cost", "route_completion", "low_progress"]].copy()
    p = OUT_TABLE / "figure5_density_stress_data.csv"
    fig5_data.round(5).to_csv(p, index=False)
    outputs["fig5_data"] = p

    latency_seed = raw.groupby(["label", "train_seed", "density"], as_index=False).agg(
        episodes=("episode", "count"),
        policy_inference_ms_mean=("policy_inference_ms_mean", "mean"),
        policy_inference_ms_p95=("policy_inference_ms_p95", "mean"),
        control_loop_wall_ms_mean=("control_loop_wall_ms_mean", "mean"),
        control_loop_wall_ms_p95=("control_loop_wall_ms_p95", "mean"),
        total_action_latency_ms_mean=("total_action_latency_ms_mean", "mean"),
        total_action_latency_ms_p95=("total_action_latency_ms_p95", "mean"),
    )
    latency_seed = add_method_columns(latency_seed)
    p = OUT_TABLE / "table_supp_runtime_by_seed.csv"
    latency_seed.round(4).to_csv(p, index=False)
    outputs["runtime_seed_csv"] = p
    return outputs


def save_fig(fig: plt.Figure, stem: str) -> list[Path]:
    paths = []
    for ext in ["pdf", "png"]:
        p = OUT_FIG / f"{stem}.{ext}"
        fig.savefig(p, dpi=300, bbox_inches="tight")
        paths.append(p)
    plt.close(fig)
    return paths


def style_axes(ax):
    ax.grid(True, color="#E5E5E5", linewidth=0.8, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def build_figures(agg: pd.DataFrame) -> dict[str, list[Path]]:
    outputs: dict[str, list[Path]] = {}
    agg = add_method_columns(agg)
    d015 = agg[np.isclose(agg["density"], 0.15)].copy()

    labels = d015["label"].tolist()
    x = np.arange(len(labels))
    names = [METHOD_LABELS[l] for l in labels]
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.8))
    panels = [
        ("route_completion", "Route completion", 100),
        ("cost", "Cost / unsafe episode", 100),
        ("stop_ratio", "Stop ratio", 100),
        ("low_progress", "Low-progress episode", 100),
    ]
    for ax, (metric, ylabel, scale) in zip(axes.flat, panels):
        vals = d015[metric].to_numpy() * scale
        ax.bar(x, vals, color=[COLORS[l] for l in labels], width=0.74, zorder=2)
        ax.set_ylabel(ylabel + " (%)")
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=28, ha="right")
        ax.set_ylim(0, max(100, vals.max() * 1.12))
        style_axes(ax)
    fig.suptitle("Frozen-policy diagnostics at traffic density 0.15", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    outputs["fig2"] = save_fig(fig, "fig2_non_motion_artifact")

    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    for _, r in d015.iterrows():
        label = r["label"]
        size = 60 + min(float(r["intervention_rate_per_100_steps"]), 100) * 4.0
        ax.scatter(r["cost"] * 100, r["route_completion"] * 100, s=size, color=COLORS[label], marker=MARKERS[label], edgecolor="black", linewidth=0.6, alpha=0.92, zorder=3)
        ax.annotate(METHOD_LABELS[label], (r["cost"] * 100, r["route_completion"] * 100), xytext=(5, 5), textcoords="offset points", fontsize=8)
    ax.set_xlabel("Cost / unsafe episode (%)")
    ax.set_ylabel("Route completion (%)")
    ax.set_xlim(-3, 105)
    ax.set_ylim(0, 100)
    style_axes(ax)
    ax.set_title("Progress-safety frontier at traffic density 0.15", fontsize=12)
    outputs["fig3"] = save_fig(fig, "fig3_progress_safety_frontier")

    fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.9), sharex=True)
    metrics = [("success", "Success (%)"), ("cost", "Cost (%)"), ("route_completion", "Route completion (%)")]
    for ax, (metric, ylabel) in zip(axes, metrics):
        for label in METHOD_ORDER:
            sub = agg[agg["label"].eq(label)].sort_values("density")
            ax.plot(sub["density"], sub[metric] * 100, marker=MARKERS[label], color=COLORS[label], linewidth=1.8, markersize=5, label=METHOD_LABELS[label])
        ax.set_xlabel("Traffic density")
        ax.set_ylabel(ylabel)
        ax.set_ylim(-3, 103)
        style_axes(ax)
    axes[0].legend(loc="best", fontsize=8, frameon=False)
    fig.suptitle("Density stress evaluation with frozen policies", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    outputs["fig5"] = save_fig(fig, "fig5_density_stress")

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    for label in METHOD_ORDER:
        sub = agg[agg["label"].eq(label)].sort_values("density")
        ax.plot(sub["density"], sub["control_loop_wall_ms_p95"], marker=MARKERS[label], color=COLORS[label], linewidth=1.8, markersize=5, label=METHOD_LABELS[label])
    ax.set_xlabel("Traffic density")
    ax.set_ylabel("Control-loop wall time p95 (ms)")
    style_axes(ax)
    ax.legend(loc="best", fontsize=8, frameon=False, ncol=2)
    ax.set_title("Runtime overhead from diagnostic rollouts", fontsize=12)
    outputs["fig7"] = save_fig(fig, "fig7_runtime_overhead")
    return outputs


def build_report(table_outputs: dict[str, Path], figure_outputs: dict[str, list[Path]], agg: pd.DataFrame, raw: pd.DataFrame) -> Path:
    lines = []
    lines.append("# IJMLC Table/Figure Package\n\n")
    lines.append(f"generated_at: {datetime.now().isoformat(timespec='seconds')}\n\n")
    lines.append("## Data Basis\n")
    lines.append(f"- aggregate: `{SUMMARY}`\n")
    lines.append(f"- seed_summary: `{SEED_SUMMARY}`\n")
    lines.append(f"- raw_episodes: `{RAW}`\n")
    lines.append(f"- aggregate_rows: {len(agg)}\n")
    lines.append(f"- raw_episodes: {len(raw)}\n")
    lines.append(f"- methods: {', '.join(METHOD_LABELS[m] for m in METHOD_ORDER)}\n")
    lines.append(f"- densities: {', '.join(str(x) for x in sorted(agg['density'].unique()))}\n")
    lines.append("\n## Generated Tables\n")
    for k, p in table_outputs.items():
        lines.append(f"- {k}: `{p}`\n")
    lines.append("\n## Generated Figures\n")
    for k, ps in figure_outputs.items():
        lines.append(f"- {k}: " + ", ".join(f"`{p}`" for p in ps) + "\n")
    lines.append("\n## Claim Boundaries\n")
    lines.append("- These artifacts summarize frozen-policy diagnostics and density stress tests. They do not claim newly trained external safe-RL baselines.\n")
    lines.append("- `Risk-only` is treated as a non-motion artifact/negative diagnostic because it has near-zero route completion and stop_ratio=1.0 across densities.\n")
    lines.append("- Runtime overhead is measured as policy/control-loop wall time during diagnostic rollouts; isolated internal guard computation latency is not separately instrumented yet.\n")
    lines.append("- Each density-method aggregate uses 120 episodes from 3 training seeds unless the table states otherwise.\n")
    p = CONTROL / "IJMLC_TABLE_FIGURE_PACKAGE.md"
    p.write_text("".join(lines), encoding="utf-8")
    return p


def main() -> None:
    missing = [p for p in [SUMMARY, SEED_SUMMARY, RAW] if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing required input(s): " + ", ".join(str(p) for p in missing))
    agg = pd.read_csv(SUMMARY)
    seed = pd.read_csv(SEED_SUMMARY)
    raw = pd.read_csv(RAW)
    agg["method_order"] = agg["label"].map(lambda x: method_sort_key(str(x)))
    agg = agg.sort_values(["density", "method_order"]).drop(columns=["method_order"])
    table_outputs = build_tables(agg, seed, raw)
    figure_outputs = build_figures(agg)
    report = build_report(table_outputs, figure_outputs, agg, raw)
    print("generated_report", report)
    for p in table_outputs.values():
        print("table", p)
    for ps in figure_outputs.values():
        for p in ps:
            print("figure", p)


if __name__ == "__main__":
    main()
