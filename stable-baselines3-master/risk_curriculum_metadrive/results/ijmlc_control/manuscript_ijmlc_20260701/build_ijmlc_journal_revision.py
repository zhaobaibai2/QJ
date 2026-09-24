#!/usr/bin/env python3
"""IJMLC journalization pass for the GuardShield-Runtime manuscript."""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

import build_publication_tables_figures as base


ROOT = Path(__file__).resolve().parents[3]
CONTROL = ROOT / "results" / "ijmlc_control"
DATA = CONTROL / "manuscript"
FIG_DIR = CONTROL / "figures_publication"
TAB_DIR = CONTROL / "tables_publication"
PKG = CONTROL / "manuscript_ijmlc_20260701"

COLORS = base.COLORS
METHOD_ORDER = base.METHOD_ORDER
RUNTIME_METHODS = ["Guard", "Shield", "Gated-risk"]

MAIN_TEXT_TABLE_FILES = [
    "table_runtime_signals_pub.tex",
    "table_compared_methods_pub.tex",
    "table_core_mechanism_pub.tex",
    "table_external_baseline_pub.tex",
    "table_density_summary_pub.tex",
    "table_claim_evidence_pub.tex",
]

APPENDIX_TABLE_FILES = [
    "table_manifest_pub.tex",
    "table_parameter_defaults_pub.tex",
    "table_result_block_provenance_pub.tex",
    "table_ci_binary_pub.tex",
    "table_seed_range_pub.tex",
    "table_density_operating_envelope_pub.tex",
    "table_sensitivity_summary_pub.tex",
    "table_runtime_summary_pub.tex",
]


def configure() -> None:
    base.configure_matplotlib()
    mpl.rcParams.update(
        {
            "font.size": 7.4,
            "axes.titlesize": 7.4,
            "axes.labelsize": 7.2,
            "xtick.labelsize": 6.6,
            "ytick.labelsize": 6.6,
            "legend.fontsize": 6.6,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def save(fig: plt.Figure, name: str) -> list[Path]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    for ext, dpi in [("pdf", 600), ("svg", 600), ("tiff", 600), ("png", 300)]:
        out = FIG_DIR / f"{name}.{ext}"
        fig.savefig(out, dpi=dpi, bbox_inches="tight", pad_inches=0.03, facecolor="white")
        paths.append(out)
    plt.close(fig)
    return paths


def clean(ax: plt.Axes, grid: bool = False) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(width=0.65, length=2.5)
    if grid:
        ax.grid(axis="y", color="#DADDE3", linewidth=0.4, alpha=0.75)
        ax.set_axisbelow(True)


def panel(ax: plt.Axes, letter: str) -> None:
    ax.text(-0.13, 1.07, letter, transform=ax.transAxes, fontsize=8.2, fontweight="bold")


def draw_fig1_feedback_architecture() -> list[Path]:
    fig = plt.figure(figsize=(7.2, 3.05))
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    panels = [
        (0.035, 0.18, 0.260, 0.66, "Policy\nproposes", "PPO backbone\ncandidate action", "#E8EEF7", "#4E5D7A"),
        (0.370, 0.18, 0.260, 0.66, "Runtime feedback\nintervenes", "TTC / speed monitor\nbounded action", "#F8E5DF", "#C65764"),
        (0.705, 0.18, 0.260, 0.66, "Diagnostics\naudit", "episode-level\nprogress-safety", "#ECE8F2", "#6C4A7E"),
    ]
    for x, y, w, h, title, subtitle, fill, accent in panels:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.014,rounding_size=0.016",
                facecolor=fill,
                edgecolor="#2F333A",
                linewidth=0.86,
            )
        )
        ax.add_patch(plt.Rectangle((x + 0.020, y + h - 0.090), 0.045, 0.010, facecolor=accent, edgecolor="none"))
        ax.text(x + 0.020, y + h - 0.175, title, ha="left", va="center", fontsize=9.5, fontweight="bold", color="#20242B", linespacing=1.05)
        ax.text(x + 0.020, y + 0.308, subtitle, ha="left", va="center", fontsize=7.6, color="#303741", linespacing=1.25)

    inner_cards = [
        (0.068, 0.265, 0.190, 0.110, "observation", "action proposal"),
        (0.403, 0.265, 0.190, 0.110, "risk state", "hard / soft / clear"),
    ]
    for x, y, w, h, top, bottom in inner_cards:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.008,rounding_size=0.012",
                facecolor="#FFFFFF",
                edgecolor="#8C939D",
                linewidth=0.55,
            )
        )
        ax.text(x + w / 2, y + h * 0.62, top, ha="center", va="center", fontsize=7.2, fontweight="bold", color="#29313B")
        ax.text(x + w / 2, y + h * 0.35, bottom, ha="center", va="center", fontsize=6.8, color="#555D68")

    dashboard = [("Success", "Cost"), ("Route", "Low-prog."), ("TTC", "Int./100"), ("Loop", "p95")]
    dx, dy = 0.731, 0.250
    card_w, card_h = 0.091, 0.074
    for i, (top, bottom) in enumerate(dashboard):
        x = dx + (i % 2) * 0.103
        y = dy + (1 - i // 2) * 0.098
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                card_w,
                card_h,
                boxstyle="round,pad=0.006,rounding_size=0.010",
                facecolor="#FFFFFF",
                edgecolor="#8C939D",
                linewidth=0.50,
            )
        )
        ax.text(x + card_w / 2, y + card_h * 0.64, top, ha="center", va="center", fontsize=6.3, fontweight="bold")
        ax.text(x + card_w / 2, y + card_h * 0.34, bottom, ha="center", va="center", fontsize=5.9, color="#58616D")

    for start, end in [((0.292, 0.50), (0.370, 0.50)), ((0.629, 0.50), (0.706, 0.50))]:
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=10.5,
                linewidth=0.95,
                color="#33363F",
            )
        )

    ax.add_patch(
        FancyArrowPatch(
            (0.824, 0.178),
            (0.163, 0.178),
            connectionstyle="arc3,rad=-0.16",
            arrowstyle="-|>",
            mutation_scale=9.5,
            linewidth=0.78,
            color="#6D737C",
        )
    )
    ax.text(0.492, 0.064, "closed-loop feedback", ha="center", va="center", fontsize=7.5, color="#4F5661")
    return save(fig, "fig1_cybernetic_feedback_architecture")


def draw_fig2_core_evidence(tables: dict[str, pd.DataFrame]) -> list[Path]:
    core = base.ordered(tables["table3_core_d015_main_diagnostics"])
    methods = core["method"].tolist()
    x = np.arange(len(methods))
    fig = plt.figure(figsize=(7.2, 4.65))
    gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.38, hspace=0.44)

    ax = fig.add_subplot(gs[0, 0])
    ax.bar(x - 0.18, core["cost_pct"], 0.36, color=[COLORS[m] for m in methods], alpha=0.88, label="Cost")
    ax.bar(x + 0.18, core["route_completion_pct"], 0.36, facecolor="white", edgecolor=[COLORS[m] for m in methods], linewidth=1.0, label="Route")
    ax.set_ylim(0, 105)
    ax.set_ylabel("Percent")
    ax.set_xticks(x)
    ax.set_xticklabels(methods, rotation=42, ha="right")
    ax.legend(frameon=False, loc="upper right")
    clean(ax, True)
    panel(ax, "a")

    ax = fig.add_subplot(gs[0, 1])
    ax.scatter(core["cost_pct"], core["route_completion_pct"], s=np.clip(core["success_pct"] + 18, 24, 95), c=[COLORS[m] for m in methods], edgecolor="#20232A", linewidth=0.45)
    offsets = {"PPO": (-38, -18), "Risk-only": (6, 7), "No-action guard": (-82, 18), "Guard": (8, 12), "Shield": (8, -12), "Gated-risk": (8, 24)}
    for _, r in core.iterrows():
        dx, dy = offsets.get(r["method"], (4, 4))
        ax.annotate(r["method"], (r["cost_pct"], r["route_completion_pct"]), xytext=(dx, dy), textcoords="offset points", fontsize=6.2, arrowprops=dict(arrowstyle="-", color="#A8ADB5", lw=0.4))
    ax.set_xlabel("Cost (%)")
    ax.set_ylabel("Route completion (%)")
    ax.set_xlim(-4, 105)
    ax.set_ylim(-4, 100)
    clean(ax, True)
    panel(ax, "b")

    ax = fig.add_subplot(gs[1, 0])
    vals = core["low_progress_pct"].to_numpy()
    ax.barh(np.arange(len(methods)), vals, color=[COLORS[m] for m in methods], alpha=0.88)
    ax.set_yticks(np.arange(len(methods)))
    ax.set_yticklabels(methods)
    ax.set_xlim(0, 105)
    ax.set_xlabel("Low-progress episodes (%)")
    for yy, vv in enumerate(vals):
        ax.text(vv + 1, yy, f"{vv:.1f}", va="center", fontsize=6.1)
    ax.invert_yaxis()
    clean(ax, True)
    panel(ax, "c")

    ax = fig.add_subplot(gs[1, 1])
    width = 0.36
    ax.bar(x - width / 2, core["ttc_dangerous_pct"], width, color=[COLORS[m] for m in methods], alpha=0.88, label="TTC danger (%)")
    ax.bar(x + width / 2, core["interventions_per_100_steps"], width, facecolor="white", edgecolor=[COLORS[m] for m in methods], linewidth=1.0, label="Int./100")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Step-level diagnostic value")
    ax.set_xticks(x)
    ax.set_xticklabels(methods, rotation=42, ha="right")
    ax.legend(frameon=False, loc="upper left")
    clean(ax, True)
    panel(ax, "d")
    return save(fig, "fig2_core_artifact_evidence")


def draw_fig5_ttc_sensitivity(tables: dict[str, pd.DataFrame]) -> list[Path]:
    sens = tables["table_supp_sensitivity"]
    sub = sens[sens["sensitivity_axis"] == "ttc_threshold"].copy()
    metrics = [("success_pct", "Success (%)", "Blues"), ("cost_pct", "Cost (%)", "Oranges"), ("route_completion_pct", "Route (%)", "Purples")]
    methods = RUNTIME_METHODS
    values = sorted(sub["sensitivity_value"].unique())
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.55), constrained_layout=True)
    for idx, (ax, (metric, label, cmap)) in enumerate(zip(axes, metrics)):
        mat = np.full((len(methods), len(values)), np.nan)
        for i, m in enumerate(methods):
            for j, v in enumerate(values):
                row = sub[(sub["method"] == m) & (sub["sensitivity_value"] == v)]
                if not row.empty:
                    mat[i, j] = row.iloc[0][metric]
        vmin, vmax = np.nanmin(mat), np.nanmax(mat)
        im = ax.imshow(mat, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_xticks(range(len(values)))
        ax.set_xticklabels([f"{v:g}" for v in values])
        ax.set_yticks(range(len(methods)))
        ax.set_yticklabels(methods if idx == 0 else [])
        ax.set_xlabel("TTC threshold")
        ax.set_title(label, fontsize=7.2)
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                norm = 0.0 if vmax == vmin else (mat[i, j] - vmin) / (vmax - vmin)
                txt_color = "white" if norm > 0.68 else "#20232A"
                ax.text(j, i, f"{mat[i, j]:.1f}", ha="center", va="center", fontsize=6.2, color=txt_color)
        for spine in ax.spines.values():
            spine.set_linewidth(0.45)
            spine.set_color("#AEB4BD")
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02)
        cbar.ax.tick_params(labelsize=6.0, length=2)
        panel(ax, chr(ord("a") + idx))
    return save(fig, "fig5_ttc_threshold_sensitivity")


def draw_fig_s1_target_speed(tables: dict[str, pd.DataFrame]) -> list[Path]:
    sens = tables["table_supp_sensitivity"]
    sub = sens[sens["sensitivity_axis"] == "target_speed_kmh"].copy()
    metrics = [("success_pct", "Success (%)", "Blues"), ("cost_pct", "Cost (%)", "Oranges"), ("route_completion_pct", "Route (%)", "Purples")]
    methods = RUNTIME_METHODS
    values = sorted(sub["sensitivity_value"].unique())
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.55), constrained_layout=True)
    for idx, (ax, (metric, label, cmap)) in enumerate(zip(axes, metrics)):
        mat = np.full((len(methods), len(values)), np.nan)
        for i, m in enumerate(methods):
            for j, v in enumerate(values):
                row = sub[(sub["method"] == m) & (sub["sensitivity_value"] == v)]
                if not row.empty:
                    mat[i, j] = row.iloc[0][metric]
        vmin, vmax = np.nanmin(mat), np.nanmax(mat)
        im = ax.imshow(mat, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_xticks(range(len(values)))
        ax.set_xticklabels([f"{v:g}" for v in values])
        ax.set_yticks(range(len(methods)))
        ax.set_yticklabels(methods if idx == 0 else [])
        ax.set_xlabel("Target speed (km/h)")
        ax.set_title(label, fontsize=7.2)
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                norm = 0.0 if vmax == vmin else (mat[i, j] - vmin) / (vmax - vmin)
                txt_color = "white" if norm > 0.68 else "#20232A"
                ax.text(j, i, f"{mat[i, j]:.1f}", ha="center", va="center", fontsize=6.2, color=txt_color)
        for spine in ax.spines.values():
            spine.set_linewidth(0.45)
            spine.set_color("#AEB4BD")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02)
        panel(ax, chr(ord("a") + idx))
    return save(fig, "figS1_target_speed_sensitivity")


def draw_fig6_runtime(tables: dict[str, pd.DataFrame]) -> list[Path]:
    runtime = base.ordered(tables["table7_runtime_overhead"], "density")
    methods = ["PPO", "Guard", "Shield", "Gated-risk"]
    density_ticks = [0.08, 0.15, 0.20, 0.25]
    specs = [
        ("policy_inference_ms_p95", "Policy p95 (ms)"),
        ("control_loop_wall_ms_p95", "Loop p95 (ms)"),
        ("intervention_rate_per_100_steps", "Interventions / 100 steps"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.55), constrained_layout=True)
    for idx, (ax, (col, ylabel)) in enumerate(zip(axes, specs)):
        for m in methods:
            df = runtime[runtime["method"] == m].sort_values("density")
            ax.plot(df["density"], df[col], marker=base.MARKERS[m], color=COLORS[m], linewidth=1.2, markersize=3.9, label=m)
        ax.set_xlabel("Traffic density")
        ax.set_ylabel(ylabel)
        ax.set_xticks(density_ticks)
        ax.set_xticklabels([f"{v:.2f}" for v in density_ticks])
        clean(ax, True)
        panel(ax, chr(ord("a") + idx))
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.08))
    return save(fig, "fig6_simulation_loop_overhead")


def table_block(label: str, caption: str, note: str, tabular: str, font: str = r"\scriptsize", placement: str = "t", tabcolsep: str = "3.4pt") -> str:
    return rf"""
\begin{{table}}[{placement}]
\centering
\caption{{{caption}}}
\label{{{label}}}
{font}
\setlength{{\tabcolsep}}{{{tabcolsep}}}
\renewcommand{{\arraystretch}}{{1.08}}
{tabular}
\begin{{tablenotes}}
\item {note}
\end{{tablenotes}}
\end{{table}}
"""


def display_method(method: object) -> str:
    name = str(method)
    if name == "PPO":
        return "PPO backbone"
    if name == "RCPO-Lagrangian":
        return "PPO-Lagrangian"
    return name


def write_main_tables(tables: dict[str, pd.DataFrame]) -> list[Path]:
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    signal_rows = [
        ["Runtime signal", "Speed", "$v_t$", "speed guard; stop ratio"],
        ["Runtime signal", "Route progress", "$\\Delta p_t$", "low-progress and Gated-risk motion gate"],
        ["Runtime signal", "Forward TTC", "$\\mathrm{TTC}_t$", "hard/soft risk state; TTC-danger"],
        ["Runtime signal", "Intervention event", "$\\mathbf{1}[a_t^{exec}\\ne a_t^\\pi]$", "Int./100 steps"],
        ["Core parameter", "Episode horizon", "1500 steps", "evaluation limit"],
        ["Core parameter", "Target speed", "18 km/h", "runtime variants"],
        ["Core parameter", "Core TTC threshold", "12.0", "stored formal configuration"],
        ["Core parameter", "TTC-danger threshold", "5.0", "diagnostic danger counter"],
        ["Core parameter", "Stop threshold", "$v_t<1.0$ km/h", "stop ratio"],
        ["Core parameter", "Low-progress threshold", "route $<0.20$", "non-motion artifact flag"],
    ]
    tab = base.tabular(
        [[base.latex_escape(c) if "$" not in c else c for c in row] for row in signal_rows],
        r"@{}>{\raggedright\arraybackslash}p{0.17\textwidth}>{\raggedright\arraybackslash}p{0.22\textwidth}>{\raggedright\arraybackslash}p{0.19\textwidth}>{\raggedright\arraybackslash}p{0.34\textwidth}@{}",
        ["Group", "Item", "Value or symbol", "Role"],
    )
    p = TAB_DIR / "table_runtime_signals_pub.tex"
    p.write_text(
        table_block(
            "tab_runtime_signals",
            "Runtime signals and core diagnostic parameters.",
            "Detailed action caps, speed-guard thresholds, and result-block provenance are reported in Appendix~\\ref{app_manifest}.",
            tab,
            font=r"\scriptsize",
            placement="!htbp",
        ),
        encoding="utf-8",
    )
    written.append(p)

    method_rows = [
        ["PPO backbone", "No risk reward", "None", "Fixed policy backbone and lower-bound comparator"],
        ["Risk-only", "Risk reward", "None", "Tests whether low cost is stationary avoidance"],
        ["No-action guard", "Risk reward", "Disabled", "Clean reward-only versus runtime-intervention control"],
        ["RSS/TTC filter", "No risk reward", "External TTC/RSS rule", "Classical runtime-filter comparator"],
        ["PPO-Lagrangian", "Lagrangian penalty", "None", "Training-time constrained baseline under this protocol"],
        ["Guard", "Curriculum PPO, no risk reward", "TTC hard/soft cap + speed guard", "Runtime deployment variant with action intervention"],
        ["Shield", "No-curriculum PPO, no risk reward", "Same TTC hard/soft cap + speed guard", "Runtime deployment variant isolating the execution-side operator"],
        ["Gated-risk", "Curriculum PPO with gated risk", "Same TTC hard/soft cap + speed guard", "Adds motion/risk-gated reward to reduce stationary exploitation"],
    ]
    tab = base.tabular(
        [[base.latex_escape(c) for c in row] for row in method_rows],
        r"@{}>{\raggedright\arraybackslash}p{0.16\textwidth}>{\raggedright\arraybackslash}p{0.20\textwidth}>{\raggedright\arraybackslash}p{0.25\textwidth}>{\raggedright\arraybackslash}p{0.30\textwidth}@{}",
        ["Method", "Training or reward", "Runtime operator", "Role in protocol"],
    )
    p = TAB_DIR / "table_compared_methods_pub.tex"
    p.write_text(
        table_block(
            "tab_compared_methods",
            "Compared methods and runtime deployment variants.",
            "Guard and Shield share the same execution-side operator but differ in training context; they are deployment variants rather than a clean single-factor ablation. The clean same-checkpoint runtime-operator contrast is reported separately in Table~\\ref{tab_clean_runtime_ablation}.",
            tab,
            font=r"\scriptsize",
            placement="!htbp",
        ),
        encoding="utf-8",
    )
    written.append(p)

    component_rows = [
        ["Training context", "Curriculum PPO", "No-curriculum PPO", "Curriculum PPO"],
        ["Execution operator", "TTC hard/soft cap + speed guard", "Same TTC hard/soft cap + speed guard", "Same TTC hard/soft cap + speed guard"],
        ["Risk reward", "No", "No", "Motion-gated risk reward"],
        ["Motion/risk gate", "No reward gate", "No reward gate", "$v_t\\geq3$ km/h or $\\Delta p_t>10^{-4}$; risk if TTC-risk $\\geq0.01$ or lane deviation $\\geq0.25$"],
        ["Intended role", "Runtime action regularizer", "Pure execution-shield baseline", "Anti-stationary risk shaping plus runtime feedback"],
    ]
    tab = base.tabular(
        [[base.latex_escape(c) if "$" not in c else c for c in row] for row in component_rows],
        r"@{}>{\raggedright\arraybackslash}p{0.18\textwidth}>{\raggedright\arraybackslash}p{0.20\textwidth}>{\raggedright\arraybackslash}p{0.20\textwidth}>{\raggedright\arraybackslash}p{0.31\textwidth}@{}",
        ["Component", "Guard", "Shield", "Gated-risk"],
    )
    p = TAB_DIR / "table_runtime_variant_components_pub.tex"
    p.write_text(
        table_block(
            "tab_runtime_variant_components",
            "Code-level distinction among runtime variants.",
            "Guard and Shield intentionally share the same execution-side operator; they are separated to isolate the effect of curriculum/training context from the effect of runtime action intervention. Gated-risk adds a motion/risk-gated training reward on top of the same execution operator.",
            tab,
            font=r"\scriptsize",
        ),
        encoding="utf-8",
    )
    # Generated for supplementary audit if needed; not copied into the final manuscript package.

    protocol_rows = [
        ["Claim 1", "Cost-only safe RL can create non-motion artifacts", "P1 artifact controls", "Risk-only, stop ratio, low progress, route completion"],
        ["Claim 2", "Execution-side feedback is the active ingredient", "P1 mechanism ablation", "No-action guard versus Guard/Shield/Gated-risk"],
        ["Claim 3", "Runtime feedback improves over external baselines", "P2 external comparison", "RSS/TTC filter and PPO-Lagrangian"],
        ["Claim 4", "The benefit has an operating envelope", "P4 density stress", "densities 0.08, 0.15, 0.20, 0.25"],
        ["Claim 5", "The loop is measurable and not a hidden bottleneck", "runtime diagnostics", "policy inference p95, control-loop p95, intervention rate"],
    ]
    tab = base.tabular(
        [[base.latex_escape(c) for c in row] for row in protocol_rows],
        r"@{}>{\raggedright\arraybackslash}p{0.11\textwidth}>{\raggedright\arraybackslash}p{0.31\textwidth}>{\raggedright\arraybackslash}p{0.18\textwidth}>{\raggedright\arraybackslash}p{0.30\textwidth}@{}",
        ["Claim", "Question", "Experiment block", "Primary evidence"],
    )
    p = TAB_DIR / "table_protocol_claim_map_pub.tex"
    p.write_text(
        table_block(
            "tab_protocol_claim_map",
            "Evaluation protocol mapped to manuscript claims.",
            "The protocol is organized by claim rather than by file name, so readers can see which evidence supports each conclusion.",
            tab,
            font=r"\footnotesize",
        ),
        encoding="utf-8",
    )
    # Generated for supplementary audit if needed; not copied into the final manuscript package.

    parameter_rows = [
        ["Episode horizon", "1500 simulator steps", "evaluation"],
        ["Training vectorization", "16 parallel SB3 environments", "training"],
        ["PPO policy network", "MlpPolicy, Tanh, [256, 256]", "policy backbone"],
        ["PPO optimizer settings", "lr $3\\times10^{-4}$; $\\gamma=0.99$; GAE $\\lambda=0.95$; clip 0.2", "training"],
        ["PPO batch settings", "1024 steps; batch 256; 10 epochs", "training"],
        ["Base TTC threshold ($\\tau$)", "12.0 s", "stored formal configuration"],
        ["Hard TTC threshold ($\\tau_{\\mathrm{hard}}$)", "$\\max(3.5,0.60\\tau)=7.2$ s", "hard braking region"],
        ["Soft TTC threshold ($\\tau_{\\mathrm{soft}}$)", "$\\max(6.0,\\tau)=12.0$ s", "soft acceleration cap"],
        ["Hard acceleration cap ($u_{\\mathrm{hard}}$)", "$-1.0$", "acceleration bound"],
        ["Soft acceleration cap ($u_{\\mathrm{soft}}$)", "$-0.6$", "acceleration bound"],
        ["Speed guard", "$v_t>v^*+5$: $u_t\\leq-0.35$; $v_t>v^*$: $u_t\\leq0.0$", "speed guard"],
        ["Stop threshold", "$v_t<1.0$ km/h", "stop ratio"],
        ["Low-progress threshold", "route completion $<0.20$", "non-motion flag"],
        ["TTC-danger threshold", "5.0 s", "danger counter"],
        ["TTC closing-speed gate", "$\\epsilon=10^{-3}$", "monitor definition"],
        ["Gated-risk motion gate", "$v_{\\min}=3.0$ km/h; $p_{\\min}=10^{-4}$", "risk reward gate"],
        ["PPO-Lagrangian update", "$\\lambda_0=20$; lr 5; max 200; window 20; cost limit 0.25", "constrained baseline"],
        ["RSS/TTC comparator", "soft 6.0 s; hard 3.5 s; target 20 km/h", "external runtime filter"],
    ]
    tab = base.tabular(
        [[base.latex_escape(c) if "$" not in c else c for c in row] for row in parameter_rows],
        r"@{}>{\raggedright\arraybackslash}p{0.30\textwidth}>{\raggedright\arraybackslash}p{0.35\textwidth}>{\raggedright\arraybackslash}p{0.24\textwidth}@{}",
        ["Parameter", "Value", "Used for"],
    )
    p = TAB_DIR / "table_parameter_defaults_pub.tex"
    p.write_text(
        table_block(
            "tab_parameter_defaults",
            "Default training, intervention, and diagnostic parameters.",
            "The table separates TTC thresholds from executed acceleration bounds. Lane deviation is used for risk gating and logging, not for direct acceleration capping. TTC-threshold sweeps in Fig.~\\ref{fig_ttc_sensitivity} are independent reruns and should not be numerically matched to the core rows.",
            tab,
            font=r"\scriptsize",
            placement="!htbp",
        ),
        encoding="utf-8",
    )
    written.append(p)

    provenance_rows = [
        ["Table~\\ref{tab_core_mechanism} / Fig.~\\ref{fig_core_evidence}", "0.15", "18 km/h; TTC 12.0", "core diagnostic episodes", "main mechanism result"],
        ["Fig.~\\ref{fig_ttc_sensitivity}", "0.15", "stored speed; TTC 6/8/10/12", "independent sensitivity rerun", "trend evidence only"],
        ["Fig.~\\ref{fig_target_speed_sensitivity}", "0.15", "speed 15/18/22; TTC 12.0", "independent sensitivity rerun", "secondary trend evidence"],
        ["Table~\\ref{tab_density_summary} / Fig.~\\ref{fig_density}", "0.08--0.25", "stored configs", "density-stress diagnostics", "operating-envelope evidence"],
    ]
    tab = base.tabular(
        [[c if "\\ref" in c or "--" in c else base.latex_escape(c) for c in row] for row in provenance_rows],
        r"@{}>{\raggedright\arraybackslash}p{0.25\textwidth}>{\centering\arraybackslash}p{0.09\textwidth}>{\raggedright\arraybackslash}p{0.23\textwidth}>{\raggedright\arraybackslash}p{0.19\textwidth}>{\raggedright\arraybackslash}p{0.14\textwidth}@{}",
        ["Block", "Density", "Parameters", "Source", "Use"],
    )
    p = TAB_DIR / "table_result_block_provenance_pub.tex"
    p.write_text(
        table_block(
            "tab_result_block_provenance",
            "Result-block provenance and parameter scope.",
            "Rows with the same nominal TTC threshold can differ because sensitivity plots are independent diagnostic reruns, not duplicate evaluations of the core Table~\\ref{tab_core_mechanism} rows.",
            tab,
            font=r"\scriptsize",
            placement="!htbp",
            tabcolsep="2.0pt",
        ),
        encoding="utf-8",
    )
    written.append(p)

    core = base.ordered(tables["table3_core_d015_main_diagnostics"])
    rows = []
    for _, r in core.iterrows():
        rows.append([
            base.latex_escape(display_method(r["method"])),
            base.pct(r["success_pct"]),
            base.pct(r["cost_pct"]),
            base.pct(r["route_completion_pct"]),
            base.pct(r["low_progress_pct"]),
            base.pct(r["stop_ratio_pct"]),
            base.pct(r["ttc_dangerous_pct"]),
            base.pct(r["interventions_per_100_steps"]),
        ])
    tab = base.tabular(rows, r"@{}lrrrrrrr@{}", ["Method", "Success", "Cost", "Route", "Low-prog.", "Stop", "TTC-danger", "Int./100 steps"])
    p = TAB_DIR / "table_core_mechanism_pub.tex"
    p.write_text(
        table_block(
            "tab_core_mechanism",
            "Core mechanism result at density 0.15.",
            "Values are percentages except Int./100 steps. Higher success and route are preferred; lower cost, low-progress, stop, and TTC-danger are preferred. Full seed scatter and loop timings are in Appendix Tables.",
            tab,
        ),
        encoding="utf-8",
    )
    written.append(p)

    mechanism_rows = [
        ["Low cost is sufficient?", "Risk-only", "Fail if safety is stationary avoidance", "0.0 cost, 0.9 route, 100.0 stop", "Supported"],
        ["Reward shaping is enough?", "No-action guard", "Unsafe without execution intervention", "100.0 cost, 21.7 route", "Supported"],
        ["Runtime intervention matters?", "Guard / Shield / Gated-risk", "Lower cost with route progress", "18.3--20.8 cost, 85.7--86.9 route", "Supported"],
        ["Classical filter is enough?", "RSS/TTC filter", "Improves PPO backbone but trails runtime variants", "44.2 cost versus 18.3--20.8", "Supported"],
        ["Dense traffic is solved?", "Density sweep", "Degrades under stress if claim is bounded", "cost rises at density 0.25", "Bounded"],
    ]
    tab = base.tabular(
        [[base.latex_escape(c) for c in row] for row in mechanism_rows],
        r"@{}>{\raggedright\arraybackslash}p{0.14\textwidth}>{\raggedright\arraybackslash}p{0.13\textwidth}>{\raggedright\arraybackslash}p{0.22\textwidth}>{\raggedright\arraybackslash}p{0.18\textwidth}>{\raggedright\arraybackslash}p{0.10\textwidth}@{}",
        ["Question", "Variant", "Expected evidence", "Observed evidence", "Status"],
    )
    p = TAB_DIR / "table_mechanism_decomposition_pub.tex"
    p.write_text(
        table_block(
            "tab_mechanism_decomposition",
            "Mechanism decomposition linking ablations to the main claim.",
            "This table is a reviewer-facing navigation aid. Status distinguishes supported claims from bounded operating-envelope claims.",
            tab,
            font=r"\footnotesize",
        ),
        encoding="utf-8",
    )
    # Generated for supplementary audit if needed; not copied into the final manuscript package.

    ext = base.ordered(tables["table4_external_baselines_d015"])
    rows = []
    for _, r in ext.iterrows():
        rows.append([
            base.latex_escape(display_method(r["method"])),
            base.pct(r["success_pct"]),
            base.pct(r["cost_pct"]),
            base.pct(r["route_completion_pct"]),
            base.pct(r["collision_pct"]),
            base.pct(r["out_of_road_pct"]),
            base.pct(r["ttc_dangerous_pct"]),
            base.pct(r["interventions_per_100_steps"]),
        ])
    tab = base.tabular(rows, r"@{}lrrrrrrr@{}", ["Method", "Success", "Cost", "Route", "Collision", "Out-road", "TTC-danger", "Int./100 steps"])
    p = TAB_DIR / "table_external_baseline_pub.tex"
    p.write_text(
        table_block(
            "tab_external_baseline",
            "External baseline comparison at density 0.15.",
            "Values are percentages except Int./100 steps. RSS/TTC is an interpretable runtime-filter comparator; intervention frequency is diagnostic rather than an objective by itself.",
            tab,
        ),
        encoding="utf-8",
    )
    written.append(p)

    den = tables["table6_density_stress_summary"].copy()
    rows = []
    for density, group in den.groupby("density"):
        ppo = group[group["method"] == "PPO"].iloc[0]
        runtime = group[group["method"].isin(RUNTIME_METHODS)].sort_values(["cost_pct", "route_completion_pct"], ascending=[True, False]).iloc[0]
        rows.append([
            f"{density:.2f}",
            base.pct(ppo["cost_pct"]),
            base.pct(ppo["route_completion_pct"]),
            base.latex_escape(display_method(runtime["method"])),
            base.pct(runtime["cost_pct"]),
            base.pct(runtime["route_completion_pct"]),
            base.pct(ppo["cost_pct"] - runtime["cost_pct"]),
            base.pct(runtime["route_completion_pct"] - ppo["route_completion_pct"]),
        ])
    tab = base.tabular(rows, r"@{}lrrlrrrr@{}", ["Dens.", "PPO C", "PPO R", "Best runtime variant by cost", "C", "R", "Cost red.", "Route gain"])
    p = TAB_DIR / "table_density_summary_pub.tex"
    p.write_text(
        table_block(
            "tab_density_summary",
            "Density-stress summary: post-hoc lowest-cost runtime row at each density.",
            "C and R denote cost and route completion in percent. This is a compact lowest-cost runtime summary at each density, not a claim that one fixed variant dominates across densities. Fig.~\\ref{fig_density} and Appendix~\\ref{app_density} show the fixed-variant trends and operating-envelope table.",
            tab,
            font=r"\scriptsize",
        ),
        encoding="utf-8",
    )
    written.append(p)

    evidence_rows = [
        ["Cost-only safety is ambiguous", "Risk-only obtains 0.0 cost but 100.0 stop and 0.9 route", "Table~\\ref{tab_core_mechanism}, Fig.~\\ref{fig_core_evidence}", "Supported"],
        ["Execution-side intervention matters", "No-action guard remains at 100.0 cost; runtime variants reduce cost and preserve route", "Table~\\ref{tab_core_mechanism}; Sec.~\\ref{sec_mechanism}", "Supported"],
        ["Classical filtering is not enough", "RSS/TTC improves PPO backbone but remains at 44.2 cost", "Table~\\ref{tab_external_baseline}, Fig.~\\ref{fig_external}", "Supported"],
        ["Benefit has an operating envelope", "Cost rises and success drops at density 0.25", "Table~\\ref{tab_density_summary}, Fig.~\\ref{fig_density}", "Bounded"],
        ["Timing claim is simulation-loop only", "Loop p95 is measured in the Python simulation loop", "Fig.~\\ref{fig_runtime_overhead}, App.~\\ref{app_sensitivity_runtime}", "Bounded"],
    ]
    tab = base.tabular(
        [[c if "\\ref" in c else base.latex_escape(c) for c in row] for row in evidence_rows],
        r"@{}>{\raggedright\arraybackslash}p{0.18\textwidth}>{\raggedright\arraybackslash}p{0.30\textwidth}>{\raggedright\arraybackslash}p{0.22\textwidth}>{\raggedright\arraybackslash}p{0.10\textwidth}@{}",
        ["Claim", "Evidence", "Location", "Status"],
    )
    p = TAB_DIR / "table_claim_evidence_pub.tex"
    p.write_text(
        rf"""
\begin{{center}}
\refstepcounter{{table}}\label{{tab_claim_evidence}}
\footnotesize
\textbf{{Table~\thetable}}\quad Claim-to-evidence summary.\par
\vspace{{3pt}}
\setlength{{\tabcolsep}}{{3.4pt}}
\renewcommand{{\arraystretch}}{{1.08}}
{tab}
\par\vspace{{2pt}}
\begin{{minipage}}{{0.86\textwidth}}
\footnotesize The table records supported and bounded claims under the reported simulator protocol.
\end{{minipage}}
\end{{center}}
""",
        encoding="utf-8",
    )
    written.append(p)
    return written


def ensure_bibliography() -> None:
    bib = PKG / "references.bib"
    text = bib.read_text(encoding="utf-8")
    extra = r"""

@book{astrom2008feedback,
  title={Feedback Systems: An Introduction for Scientists and Engineers},
  author={{\AA}str{\"o}m, Karl J. and Murray, Richard M.},
  publisher={Princeton University Press},
  address={Princeton, NJ},
  year={2008},
  url={https://fbsbook.org/}
}

@book{sutton2018reinforcement,
  title={Reinforcement Learning: An Introduction},
  author={Sutton, Richard S. and Barto, Andrew G.},
  edition={2},
  publisher={MIT Press},
  address={Cambridge, MA},
  year={2018},
  url={http://incompleteideas.net/book/the-book-2nd.html}
}

@article{amodei2016concrete,
  title={Concrete Problems in AI Safety},
  author={Amodei, Dario and Olah, Chris and Steinhardt, Jacob and Christiano, Paul and Schulman, John and Man{\'e}, Dan},
  journal={arXiv preprint arXiv:1606.06565},
  year={2016},
  eprint={1606.06565},
  archivePrefix={arXiv}
}

@inproceedings{pan2022reward,
  title={The Effects of Reward Misspecification: Mapping and Mitigating Misaligned Models},
  author={Pan, Alexander and Bhatia, Kush and Steinhardt, Jacob},
  booktitle={International Conference on Learning Representations},
  year={2022}
}

@inproceedings{skalse2022defining,
  title={Defining and Characterizing Reward Hacking},
  author={Skalse, Joar and Howe, Nikolaus H. R. and Krasheninnikov, Dmitrii and Krueger, David},
  booktitle={Advances in Neural Information Processing Systems},
  volume={35},
  pages={9460--9471},
  year={2022}
}

@inproceedings{berkenkamp2017safe,
  title={Safe Model-based Reinforcement Learning with Stability Guarantees},
  author={Berkenkamp, Felix and Turchetta, Matteo and Schoellig, Angela P. and Krause, Andreas},
  booktitle={Advances in Neural Information Processing Systems},
  volume={30},
  year={2017}
}

@inproceedings{chow2018lyapunov,
  title={A Lyapunov-based Approach to Safe Reinforcement Learning},
  author={Chow, Yinlam and Nachum, Ofir and Duenez-Guzman, Edgar and Ghavamzadeh, Mohammad},
  booktitle={Advances in Neural Information Processing Systems},
  volume={31},
  year={2018}
}

@article{dalal2018safe,
  title={Safe Exploration in Continuous Action Spaces},
  author={Dalal, Gal and Dvijotham, Krishnamurthy and Vecerik, Matej and Hester, Todd and Paduraru, Cosmin and Tassa, Yuval},
  journal={arXiv preprint arXiv:1801.08757},
  year={2018},
  eprint={1801.08757},
  archivePrefix={arXiv}
}

@inproceedings{saunders2018trial,
  title={Trial without Error: Towards Safe Reinforcement Learning via Human Intervention},
  author={Saunders, William and Sastry, Girish and Stuhlm{\"u}ller, Andreas and Evans, Owain},
  booktitle={Proceedings of the 17th International Conference on Autonomous Agents and MultiAgent Systems},
  pages={2067--2069},
  year={2018}
}

@inproceedings{seto1998simplex,
  title={The Simplex Architecture for Safe Online Control System Upgrades},
  author={Seto, Danbing and Krogh, Bruce and Sha, Lui and Chutinan, Alongkrit},
  booktitle={Proceedings of the 1998 American Control Conference},
  volume={6},
  pages={3504--3508},
  year={1998},
  doi={10.1109/ACC.1998.703255}
}

@inproceedings{fisac2019bridging,
  title={Bridging Hamilton-Jacobi Safety Analysis and Reinforcement Learning},
  author={Fisac, Jaime F. and Akametalu, Anayo K. and Zeilinger, Melanie N. and Kaynama, Shahab and Gillula, Jeremy and Tomlin, Claire J.},
  booktitle={2019 International Conference on Robotics and Automation},
  pages={8550--8556},
  year={2019},
  doi={10.1109/ICRA.2019.8794107}
}

@article{paden2016survey,
  title={A Survey of Motion Planning and Control Techniques for Self-driving Urban Vehicles},
  author={Paden, Brian and {\v{C}}{\'a}p, Michal and Yong, Sze Zheng and Yershov, Dmitry and Frazzoli, Emilio},
  journal={IEEE Transactions on Intelligent Vehicles},
  volume={1},
  number={1},
  pages={33--55},
  year={2016},
  doi={10.1109/TIV.2016.2578706}
}

@article{kuutti2021survey,
  title={A Survey of Deep Learning Applications to Autonomous Vehicle Control},
  author={Kuutti, Sampo and Bowden, Richard and Jin, Yaochu and Barber, Phil and Fallah, Saber},
  journal={IEEE Transactions on Intelligent Transportation Systems},
  volume={22},
  number={2},
  pages={712--733},
  year={2021},
  doi={10.1109/TITS.2019.2962338}
}

@inproceedings{dosovitskiy2017carla,
  title={CARLA: An Open Urban Driving Simulator},
  author={Dosovitskiy, Alexey and Ros, German and Codevilla, Felipe and Lopez, Antonio and Koltun, Vladlen},
  booktitle={Proceedings of the 1st Annual Conference on Robot Learning},
  series={Proceedings of Machine Learning Research},
  volume={78},
  pages={1--16},
  publisher={PMLR},
  address={Cambridge, MA},
  year={2017}
}

@inproceedings{kendall2019learning,
  title={Learning to Drive in a Day},
  author={Kendall, Alex and Hawke, Jeffrey and Janz, David and Mazur, Przemyslaw and Reda, Daniele and Allen, John-Mark and Lam, Vinh-Dieu and Bewley, Alex and Shah, Amar},
  booktitle={2019 International Conference on Robotics and Automation},
  pages={8248--8254},
  year={2019},
  doi={10.1109/ICRA.2019.8793742}
}

@article{kiran2021deep,
  title={Deep Reinforcement Learning for Autonomous Driving: A Survey},
  author={Kiran, B. Ravi and Sobh, Ibrahim and Talpaert, Victor and Mannion, Patrick and Al Sallab, Ahmad A. and Yogamani, Senthil and P{\'e}rez, Patrick},
  journal={IEEE Transactions on Intelligent Transportation Systems},
  volume={23},
  number={6},
  pages={4909--4926},
  year={2021},
  doi={10.1109/TITS.2021.3054625}
}

@inproceedings{mnih2015human,
  title={Human-level Control through Deep Reinforcement Learning},
  author={Mnih, Volodymyr and Kavukcuoglu, Koray and Silver, David and Rusu, Andrei A. and Veness, Joel and Bellemare, Marc G. and Graves, Alex and Riedmiller, Martin and Fidjeland, Andreas K. and Ostrovski, Georg and others},
  journal={Nature},
  volume={518},
  pages={529--533},
  year={2015},
  doi={10.1038/nature14236}
}

@inproceedings{fujimoto2018addressing,
  title={Addressing Function Approximation Error in Actor-Critic Methods},
  author={Fujimoto, Scott and van Hoof, Herke and Meger, David},
  booktitle={Proceedings of the 35th International Conference on Machine Learning},
  series={Proceedings of Machine Learning Research},
  volume={80},
  pages={1587--1596},
  publisher={PMLR},
  address={Cambridge, MA},
  year={2018}
}

@inproceedings{henderson2018deep,
  title={Deep Reinforcement Learning That Matters},
  author={Henderson, Peter and Islam, Riashat and Bachman, Philip and Pineau, Joelle and Precup, Doina and Meger, David},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={32},
  number={1},
  year={2018}
}

@book{altman1999constrained,
  title={Constrained Markov Decision Processes},
  author={Altman, Eitan},
  publisher={CRC Press},
  address={Boca Raton, FL},
  year={1999}
}

@inproceedings{schulman2015trust,
  title={Trust Region Policy Optimization},
  author={Schulman, John and Levine, Sergey and Abbeel, Pieter and Jordan, Michael and Moritz, Philipp},
  booktitle={Proceedings of the 32nd International Conference on Machine Learning},
  series={Proceedings of Machine Learning Research},
  volume={37},
  pages={1889--1897},
  publisher={PMLR},
  address={Cambridge, MA},
  year={2015}
}

@article{lillicrap2015continuous,
  title={Continuous Control with Deep Reinforcement Learning},
  author={Lillicrap, Timothy P. and Hunt, Jonathan J. and Pritzel, Alexander and Heess, Nicolas and Erez, Tom and Tassa, Yuval and Silver, David and Wierstra, Daan},
  journal={arXiv preprint arXiv:1509.02971},
  year={2015},
  eprint={1509.02971},
  archivePrefix={arXiv}
}

@article{leike2017ai,
  title={AI Safety Gridworlds},
  author={Leike, Jan and Martic, Miljan and Krakovna, Victoria and Ortega, Pedro A. and Everitt, Tom and Lefrancq, Andrew and Orseau, Laurent and Legg, Shane},
  journal={arXiv preprint arXiv:1711.09883},
  year={2017},
  eprint={1711.09883},
  archivePrefix={arXiv}
}

@inproceedings{todorov2012mujoco,
  title={MuJoCo: A Physics Engine for Model-based Control},
  author={Todorov, Emanuel and Erez, Tom and Tassa, Yuval},
  booktitle={2012 IEEE/RSJ International Conference on Intelligent Robots and Systems},
  pages={5026--5033},
  year={2012},
  doi={10.1109/IROS.2012.6386109}
}

@article{sallab2017deep,
  title={Deep Reinforcement Learning Framework for Autonomous Driving},
  author={Sallab, Ahmad El and Abdou, Mohammed and Perot, Etienne and Yogamani, Senthil},
  journal={Electronic Imaging},
  volume={2017},
  number={19},
  pages={70--76},
  year={2017},
  doi={10.2352/ISSN.2470-1173.2017.19.AVM-023}
}

@article{grigorescu2020survey,
  title={A Survey of Deep Learning Techniques for Autonomous Driving},
  author={Grigorescu, Sorin and Trasnea, Bogdan and Cocias, Tiberiu and Macesanu, Gigel},
  journal={Journal of Field Robotics},
  volume={37},
  number={3},
  pages={362--386},
  year={2020},
  doi={10.1002/rob.21918}
}

@article{koopman2017autonomous,
  title={Autonomous Vehicle Safety: An Interdisciplinary Challenge},
  author={Koopman, Philip and Wagner, Michael},
  journal={IEEE Intelligent Transportation Systems Magazine},
  volume={9},
  number={1},
  pages={90--96},
  year={2017},
  doi={10.1109/MITS.2016.2583491}
}

@inproceedings{xu2022safebench,
  title={SafeBench: A Benchmarking Platform for Safety Evaluation of Autonomous Vehicles},
  author={Xu, Chejian and Ding, Wenhao and Lyu, Weijie and Liu, Zuxin and Wang, Shuai and He, Yihan and Hu, Hanjiang and Zhao, Ding and Li, Bo},
  booktitle={Advances in Neural Information Processing Systems},
  volume={35},
  pages={25667--25682},
  year={2022}
}

@inproceedings{ji2023safetygymnasium,
  title={Safety-Gymnasium: A Unified Safe Reinforcement Learning Benchmark},
  author={Ji, Jiaming and Zhang, Borong and Zhou, Jiayi and Pan, Xuehai and Huang, Weidong and Sun, Ruiyang and Geng, Yiran and Zhong, Yifan and Dai, Juntao and Yang, Yaodong},
  booktitle={Advances in Neural Information Processing Systems},
  volume={36},
  year={2023}
}
"""
    needed_keys = [
        "astrom2008feedback",
        "sutton2018reinforcement",
        "amodei2016concrete",
        "pan2022reward",
        "skalse2022defining",
        "berkenkamp2017safe",
        "chow2018lyapunov",
        "dalal2018safe",
        "saunders2018trial",
        "seto1998simplex",
        "fisac2019bridging",
        "paden2016survey",
        "kuutti2021survey",
        "dosovitskiy2017carla",
        "kendall2019learning",
        "kiran2021deep",
        "mnih2015human",
        "fujimoto2018addressing",
        "henderson2018deep",
        "altman1999constrained",
        "schulman2015trust",
        "lillicrap2015continuous",
        "leike2017ai",
        "todorov2012mujoco",
        "sallab2017deep",
        "grigorescu2020survey",
        "koopman2017autonomous",
        "xu2022safebench",
        "ji2023safetygymnasium",
    ]
    if any(f"{{{key}," not in text for key in needed_keys):
        text += extra

    text = normalize_bib_addresses(text)
    entries = re.split(r"\n(?=@\w+\{)", text.strip())
    seen: set[str] = set()
    deduped: list[str] = []
    for entry in entries:
        match = re.match(r"@\w+\{([^,\s]+),", entry.strip())
        if not match:
            deduped.append(entry.strip())
            continue
        key = match.group(1)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(entry.strip())
    text = "\n\n".join(deduped) + "\n"
    bib.write_text(text, encoding="utf-8")


def normalize_bib_addresses(text: str) -> str:
    publisher_addresses = {
        "MIT Press": "Cambridge, MA",
        "PMLR": "Cambridge, MA",
        "Princeton University Press": "Princeton, NJ",
        "CRC Press": "Boca Raton, FL",
    }

    def fix_entry(match: re.Match[str]) -> str:
        entry = match.group(0)
        if "address={" in entry:
            return entry
        for publisher, address in publisher_addresses.items():
            needle = f"publisher={{{publisher}}},"
            if needle in entry:
                return entry.replace(needle, f"{needle}\n  address={{{address}}},", 1)
        return entry

    return re.sub(r"@\w+\{[^@]*?\n\}", fix_entry, text, flags=re.S)


def write_main_tex() -> Path:
    main = r"""% IJMLC journalized manuscript source.
\documentclass[pdflatex,sn-mathphys-ay]{sn-jnl}

\usepackage{graphicx}
\usepackage{multirow}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage{longtable}
\usepackage{float}
\usepackage[section]{placeins}
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage{url}
\usepackage{xcolor}
\providecommand{\blocation}[1]{}
\hypersetup{hypertexnames=false}

\raggedbottom

\begin{document}

\title[GuardShield-Runtime]{GuardShield-Runtime: A Cybernetic Feedback Framework for Progress-Preserving Safe Reinforcement Learning in Dense Traffic}

\author*[1]{\fnm{Anonymous} \sur{Author}}\email{anonymous@example.com}
\affil*[1]{\orgdiv{Department}, \orgname{Institution}, \orgaddress{\city{City}, \country{Country}}}

\abstract{Safe reinforcement learning in dense traffic can reduce measured cost by suppressing motion, producing a misleading safety signal rather than a useful driving policy. We formulate this failure as a cybernetic feedback problem in which a learned policy, environment response, runtime risk monitor, bounded action intervention, and progress-safety diagnostics form a closed loop. We introduce GuardShield-Runtime, a simulator-level framework that monitors TTC, speed, route progress, and lane-related diagnostic signals, then bounds monitor-flagged longitudinal commands before environment execution. Across MetaDrive closed-loop simulations with four traffic densities, three independently trained seeds, artifact controls, external baselines, sensitivity sweeps, confidence intervals, seed-level summaries, and runtime diagnostics, Risk-only obtains 0.0\% cost by stopping almost completely, with 100.0\% stop ratio and 0.9\% route completion at density 0.15. In contrast, Guard, Shield, and Gated-risk preserve 85.7--86.9\% route completion with 18.3--20.8\% cost. A TTC/RSS-style runtime filter improves the PPO backbone but retains higher cost than the proposed runtime variants under the same diagnostic protocol, and the tested PPO-Lagrangian implementation does not recover a progress-preserving low-cost behavior under this protocol. The contribution is therefore not formal safety certification or real-world validation; it is an artifact-aware diagnostic and runtime feedback framework showing that progress-safety evidence in dense simulated traffic should be evaluated as closed-loop feedback regulation rather than cost-only reward optimization.}

\keywords{safe reinforcement learning, cybernetic feedback, runtime intervention, autonomous driving simulation, MetaDrive, artifact-aware evaluation}

\maketitle

\section{Introduction}\label{sec_introduction}

Dense autonomous-driving control is a system--environment interaction problem. A policy chooses an action, surrounding traffic responds, the observation changes, and the next action is selected under new local risk. This feedback structure is central to cybernetics and control theory \citep{wiener1948cybernetics,astrom2008feedback}; it is also where reinforcement-learning policies can produce misleading safety evidence. In dense simulated traffic, low measured cost can arise either because the ego vehicle drives safely or because it stops and avoids interaction altogether.

This distinction matters for safe reinforcement learning. Standard deep RL optimizes long-horizon return \citep{sutton2018reinforcement,mnih2015human,schulman2015trust,schulman2017ppo,lillicrap2015continuous,fujimoto2018addressing,haarnoja2018soft}, and safe-RL methods add cost constraints, penalties, or risk objectives \citep{altman1999constrained,garcia2015safe,achiam2017constrained,tessler2018reward,chow2018lyapunov}. However, when a risk penalty is evaluated only through cost, a policy can exploit the objective by suppressing motion. In driving, this behavior is not safe driving; it is task avoidance. Progress, stop ratio, low-progress rate, time-to-collision (TTC) danger, and intervention frequency must therefore be measured alongside collision-oriented cost.

Runtime feedback intervention provides a complementary route. Rather than placing all safety regulation in the training reward, a runtime monitor can observe local risk before action execution and apply a bounded intervention to the proposed action. This turns the learned policy and driving environment into a monitored closed loop: the policy proposes actions, the environment generates feedback, the monitor estimates risk, and the intervention operator modifies monitor-flagged longitudinal commands. The resulting loop can be audited through progress-safety diagnostics.

We study this idea through GuardShield-Runtime. The framework separates three variants: Guard, which applies action-side intervention without continuous risk reward; Shield, which isolates the same execution-side operator as a no-risk-reward shield baseline; and Gated-risk, which activates risk shaping only when motion or route progress indicates an active control state. Artifact controls include Risk-only and No-action guard, and external baselines include PPO-Lagrangian and a TTC/RSS-style filter. The claim is deliberately bounded: GuardShield-Runtime is a simulator-level runtime feedback and diagnostic framework, not a proof-producing safety shield or vehicle-grade real-time controller.

The paper contributes four elements. First, it formulates progress-preserving safe RL as a cybernetic runtime feedback problem rather than a cost-only optimization problem. Second, it defines a bounded action-intervention framework with separable Guard, Shield-only, and Gated-risk variants. Third, it introduces artifact-aware diagnostics that explicitly separate low cost from immobility through route completion, stop ratio, low-progress rate, TTC danger, intervention frequency, and loop latency. Fourth, it evaluates the framework across density stress, external baselines, sensitivity sweeps, confidence intervals, seed scatter, and runtime overhead.

\section{Related Work}\label{sec_related_work}

\subsection{Safe reinforcement learning and constrained policy optimization}
Safe reinforcement learning seeks to optimize task reward while limiting unsafe outcomes \citep{garcia2015safe,amodei2016concrete,leike2017ai}. Constrained Markov decision processes, Constrained Policy Optimization, and related Lagrangian approaches formalize this idea by treating safety cost as a constraint or penalty during learning \citep{altman1999constrained,achiam2017constrained,tessler2018reward}. Other approaches use Lyapunov arguments, model-based stability conditions, or safety critics to restrict exploration \citep{berkenkamp2017safe,chow2018lyapunov,dalal2018safe}. These methods are important, but simulator evidence can be ambiguous when low cost is achieved by not moving. The non-motion artifact is related to reward hacking and specification gaming, where optimizing a proxy objective yields behavior that satisfies the measured signal without satisfying the intended task \citep{amodei2016concrete,pan2022reward,skalse2022defining}. Our study therefore treats cost as one diagnostic signal rather than the sole definition of safe driving.

\subsection{Runtime shielding, safety filters, and vehicle rules}
Runtime shielding modifies actions online when a monitored condition is violated \citep{alshiekh2018shielding,saunders2018trial}. This idea is also related to runtime-assurance and Simplex-style architectures, where an advanced controller is supervised by a simpler safety channel \citep{seto1998simplex}. In driving, rule-based safety models such as RSS provide interpretable distance or TTC-style constraints \citep{shalev2017rss}, while control barrier functions and reachability methods offer formal languages for safety filtering \citep{ames2019control,fisac2019bridging}. GuardShield-Runtime is related to this runtime family, but its evidence boundary is different. We do not claim a formal invariant set or certified safe controller. The focus is measurable runtime feedback intervention and artifact-aware evaluation in a closed-loop simulator.

\subsection{Cybernetic feedback and system--environment interaction}
Cybernetics emphasizes regulation through sensing, feedback, and action \citep{wiener1948cybernetics,astrom2008feedback}. Reinforcement learning also operates through an action--environment--observation loop, but the learned objective need not align with the desired closed-loop behavior. In our setting, the runtime monitor acts as a feedback sensor, the intervention operator acts as a bounded actuator, and progress-safety metrics act as diagnostic outputs. This framing is useful because it makes the central failure observable: a policy may reduce cost by changing the closed-loop interaction from driving to stationary avoidance.

\subsection{Closed-loop autonomous-driving simulation}
Driving simulators support repeatable evaluation of policy learning, planning, and control \citep{todorov2012mujoco,dosovitskiy2017carla,li2022metadrive}. Deep RL has been explored for autonomous-driving control and decision making \citep{sallab2017deep,kendall2019learning,grigorescu2020survey,kiran2021deep,kuutti2021survey}, but evaluation remains sensitive to scenario design, reward scale, baseline choice, random seed, and safety-case interpretation \citep{koopman2017autonomous,henderson2018deep,ray2019benchmarking}. Recent benchmark suites such as Safety-Gymnasium and SafeBench further show the need for standardized safety tasks, scenario coverage, and diagnostic metrics \citep{ji2023safetygymnasium,xu2022safebench}. MetaDrive is useful here because it provides compositional traffic scenarios and route-completion diagnostics \citep{li2022metadrive}. We use it not to claim real-world safety, but to expose whether runtime intervention preserves progress under dense closed-loop interaction.

\subsection{Positioning of this work}
GuardShield-Runtime sits between training-time safe RL and formal runtime certification. Unlike reward-only risk shaping, it modifies the action before execution and logs each intervention. Unlike RSS or CBF-style formal filters, it is not presented as a proof of safety. Its role is to demonstrate, through diagnostics, that runtime feedback intervention can mitigate a non-motion artifact that cost-only safe-RL evaluation would otherwise hide. The closest prior mechanisms are therefore TTC/RSS-style runtime filters, shielding/RTA architectures, and reward-misspecification analyses; the present distinction is the combined focus on action-side feedback, motion-gated risk shaping, and artifact-aware progress diagnostics under the same simulator protocol.

\section{GuardShield-Runtime Framework}\label{sec_method}

\begin{figure}[t]
\centering
\includegraphics[width=0.98\textwidth]{fig1_cybernetic_feedback_architecture.pdf}
\caption{Three-column architecture of GuardShield-Runtime. The learned PPO backbone proposes an action, the runtime feedback intervention converts local risk signals into a bounded executed action, and artifact-aware diagnostics determine whether safety improvements preserve motion and route progress.}
\label{fig_architecture}
\end{figure}

\subsection{Problem setting and runtime signals}\label{sec_problem_signals}
Let $o_t$ denote the simulator observation and let the learned policy propose a continuous action $a_t^\pi=(\delta_t,u_t)$, where $\delta_t$ is steering and $u_t$ is acceleration or braking. GuardShield-Runtime inserts an intervention operator $\mathcal{I}_\theta$ between policy output and environment execution:
\begin{equation}
a_t^{\mathrm{exec}}=\mathcal{I}_\theta(o_t,a_t^\pi),
\end{equation}
\begin{equation}
o_{t+1}\sim P(\cdot\mid o_t,a_t^{\mathrm{exec}}).
\end{equation}
The controller uses wrapper-level feedback signals available during closed-loop simulation: speed $v_t$, lane deviation $d_t^{\mathrm{lane}}$, route-progress increment $\Delta p_t$, a forward TTC estimate, intervention events, and wall-clock loop timing. Table~\ref{tab_runtime_signals} defines how these signals enter the monitor and how they are logged. This keeps the intervention observable and auditable rather than dependent on route identifiers or hidden simulator truth.

\input{table_runtime_signals_pub.tex}

\subsection{Failure mode: non-motion artifact}\label{sec_nonmotion_method}
The key failure mode is stationary safety. If a risk penalty or cost objective rewards the absence of collision without requiring route progress, the learned policy can reduce measured cost by slowing or stopping. This is not merely a reporting inconvenience: it changes the interpretation of a safe-RL result. A method with low cost, near-zero route completion, and high stop ratio should not be described as safe driving. For that reason, every main result reports cost together with success, route completion, low-progress rate, stop ratio, TTC-danger fraction, and intervention rate.

\subsection{Runtime monitor}\label{sec_ttc_monitor}
The runtime monitor estimates a conservative forward TTC signal from nearby traffic. For a forward vehicle $i$ with distance $d_i(t)$ and relative closing speed $v_{\mathrm{ego}}(t)-v_i(t)$, the monitored TTC is
\begin{equation}
\mathrm{TTC}_t=\min_i \frac{d_i(t)}{\max(\epsilon, v_{\mathrm{ego}}(t)-v_i(t))},
\end{equation}
with a small $\epsilon$ preventing division by zero. If no forward vehicle is available, or if the relative velocity does not indicate closing, the monitor assigns a non-dangerous default TTC state rather than inventing a collision risk. Hard, soft, and clear states are determined by thresholds $\tau_{\mathrm{hard}}$ and $\tau_{\mathrm{soft}}$; the sensitivity experiment later varies the TTC threshold independently from the core run. A dangerous step is counted when the monitored TTC is below the dangerous threshold used by the diagnostic logger.

\subsection{Intervention operator}\label{sec_guard_operator}
The intervention operator preserves steering unless the wrapper already limits it, and it bounds the acceleration command according to TTC and speed feedback:
\begin{equation}
u_t^{\mathrm{guard}}=
\begin{cases}
u_{\mathrm{hard}}, & \mathrm{TTC}_t<\tau_{\mathrm{hard}},\\
\min(u_t^\pi,u_{\mathrm{soft}}), & \tau_{\mathrm{hard}}\leq \mathrm{TTC}_t<\tau_{\mathrm{soft}},\\
u_t^\pi, & \mathrm{otherwise}.
\end{cases}
\end{equation}
A speed guard then limits acceleration when the ego speed is above the target-speed band:
\begin{equation}
u_t^{\mathrm{exec}}=\min\{u_t^{\mathrm{guard}}, u_{\mathrm{speed}}(v_t)\}.
\end{equation}
The operator is per-step and memoryless in the reported implementation. It does not optimize a trajectory or certify future safety; it enforces a bounded action before the simulator step and logs whether the action was changed. Intervention frequency is therefore reported as Int./100 control steps. A high value is not automatically better or worse: it indicates how often the runtime controller had to override the proposed action.

\subsection{Relation to TTC/RSS filtering and diagnostic scope}\label{sec_not_only_ttc}
GuardShield-Runtime is close to TTC/RSS-style runtime filtering in the sense that both act before environment execution. The distinction is diagnostic and architectural rather than formal-certification based. The external RSS/TTC comparator is a single rule-based runtime filter driven by distance or TTC thresholds. GuardShield-Runtime instead treats the intervention as one component of a closed-loop evidence system: TTC danger, stop ratio, low-progress episodes, route completion, intervention frequency, and loop timing are reported together so that a lower cost cannot be mistaken for useful driving when progress collapses.

The Gated-risk variant also addresses a reward-side failure mode that a pure execution filter does not target. Its risk reward is active only when speed or route progress indicates an active control state, which is intended to reduce stationary exploitation of a risk objective. The novelty claim is therefore not that the TTC cap is a certified safety rule. It is that runtime action intervention and artifact-aware diagnostics jointly expose whether dense-traffic safe-RL evidence reflects progress-preserving feedback regulation or conservative execution filtering alone.

\subsection{Variant definitions}\label{sec_variants}
Table~\ref{tab_compared_methods} separates the policy backbone, risk reward, action-side runtime intervention, speed guard, and progress gate. \textbf{Risk-only} uses risk reward without action intervention and is included to test the non-motion artifact. \textbf{No-action guard} disables execution-side action modification while retaining the risk-oriented objective, testing whether reward shaping alone can recover safety. \textbf{Guard} applies the action-side intervention without continuous risk reward. \textbf{Shield} isolates execution-side intervention as a non-risk-reward control. \textbf{Gated-risk} combines action intervention with risk reward that is active only when the ego vehicle is moving or making route progress:
\begin{equation}
g_t=\mathbf{1}\left[(v_t>v_{\min}\ \lor\ \Delta p_t>p_{\min})\land \mathrm{risk}_t=1\right],
\end{equation}
\begin{equation}
r_t=r_t^{\mathrm{task}}-\lambda g_t c_t^{\mathrm{risk}}.
\end{equation}
This gate is designed to reduce stationary exploitation of a continuous risk penalty. If the agent stops, the risk penalty is no longer allowed to masquerade as progress-preserving behavior.

\input{table_compared_methods_pub.tex}

\subsection{Algorithmic summary}\label{sec_algorithm}
\begin{algorithm}[t]
\footnotesize
\caption{GuardShield-Runtime closed-loop execution}
\label{alg_runtime}
\begin{algorithmic}[1]
\Require Learned policy $\pi_\phi$, monitor thresholds $\theta$, MetaDrive environment
\For{each control step $t$ until termination}
\State Observe $o_t$ and wrapper signals $v_t$, $\Delta p_t$, lane state, and nearby traffic.
\State Query the learned policy for $a_t^\pi=(\delta_t,u_t)$.
\State Estimate $\mathrm{TTC}_t$ and classify the risk state as hard, soft, or clear.
\State Apply $\mathcal{I}_\theta(o_t,a_t^\pi)$ to obtain $a_t^{\mathrm{exec}}$.
\State Execute $a_t^{\mathrm{exec}}$ in the simulator.
\State Log cost, route, stop, low-progress, TTC-danger, intervention, and loop-time diagnostics.
\EndFor
\State Aggregate diagnostics by episode, training seed, traffic density, and sensitivity setting.
\end{algorithmic}
\end{algorithm}

\section{Experimental Protocol}\label{sec_experimental_protocol}

\subsection{Environment and task}\label{sec_environment_task}
All experiments use MetaDrive dense-traffic closed-loop driving simulation. The agent receives continuous control commands and is evaluated by route progress, task success, collision or off-road cost, stop ratio, low-progress rate, speed, TTC-danger fraction, intervention frequency, and wall-clock simulation-loop timing. Success is the simulator episode-success flag for completing the driving task without terminal failure. Cost is reported as the percentage of episodes with a nonzero safety-cost event, dominated by collision or out-of-road termination in this protocol. Traffic density is the MetaDrive \texttt{traffic\_density} setting controlling background-traffic generation; the main density is 0.15, and density stress additionally evaluates 0.08, 0.20, and 0.25. Formal diagnostic episodes terminate on simulator success, simulator failure, or the fixed 1500-step horizon used by the reported checkpoints.

\subsection{Compared methods}\label{sec_compared_methods}
The compared rows are listed in Table~\ref{tab_compared_methods}. The unshielded PPO row is reported as \emph{PPO backbone} because it is the policy backbone and lower-bound comparator for runtime intervention. The PPO-Lagrangian row is a tested training-time constrained baseline under the same environment family and seed protocol; its zero-success result is reported as a protocol outcome, not as a universal claim about all constrained RL implementations. The RSS/TTC filter is a meaningful external runtime comparator because it also modifies behavior through an interpretable distance or TTC rule.

\subsection{Training protocol and checkpoint selection}\label{sec_training_protocol}
Training and ordinary evaluation use 16 parallel environments. The formal rows in the model manifest use one million training timesteps per seed, horizon 1500, and \texttt{ent\_coef}=0.01 for the reported PPO-family checkpoints. Each density-0.15 table aggregates three independently trained seeds. The default target speed for the proposed runtime variants is 18 km/h, and the stored reward/action-guard TTC threshold for the formal configuration is 12.0. The external RSS/TTC comparator is parameterized separately with soft and hard TTC thresholds of 6.0 s and 3.5 s and a 20 km/h target speed. The checkpoint selection is fixed before diagnostic evaluation so that post-hoc filtering is not used to select favourable episodes. Full PPO, PPO-Lagrangian, RSS/TTC, and runtime-variant hyperparameters are listed in Appendix~\ref{app_manifest}, with run-level configuration files retained in the supplementary package.

\subsection{Diagnostic evaluation protocol}\label{sec_eval_protocol}
The IJMLC diagnostic evaluations are launched as per-seed shards so that episode-level TTC, speed, stop, intervention, route, and latency statistics remain traceable. Each formal density-0.15 aggregate row uses 120 diagnostic episodes across three training seeds. Density stress applies the same diagnostic logic across four traffic densities. Sensitivity sweeps are independent diagnostic reruns and therefore should be interpreted as trend evidence rather than an exact reproduction of the core default row. Appendix~\ref{app_manifest} reports the detailed parameter and result-block provenance tables.

\subsection{Statistical reporting}\label{sec_stats_protocol}
Main tables report one decimal place for percent metrics. Appendix B reports Wilson intervals for binary outcomes and a seed-level mean/range summary for the density-0.15 comparison; the full bootstrap and per-seed CSVs remain in the supplementary package. These intervals are intended to document uncertainty in the simulator diagnostic protocol; they do not replace broader policy-family or real-world validation.

\subsection{Supplementary artifacts}\label{sec_evidence_package}
The supplementary package includes anonymized episode-level results, aggregate tables, plotting scripts, table-generation scripts, and configuration files required to reproduce the reported figures and tables.

\section{Results}\label{sec_results}

\subsection{Non-motion artifact: low cost without driving}\label{sec_artifact}
Low measured cost does not necessarily indicate progress-preserving safe behavior. Figure~\ref{fig_core_evidence} and Table~\ref{tab_core_mechanism} show that Risk-only obtains 0.0\% cost at density 0.15, but this apparent safety is accompanied by 0.9\% route completion, 100.0\% stop ratio, and 100.0\% low-progress episodes. The PPO backbone shows the opposite failure mode: it continues to move, but it reaches 100.0\% cost with only 20.7\% route completion. The artifact is therefore a substantive evaluation failure rather than a reporting detail. It becomes visible only when motion and progress diagnostics are reported next to collision-oriented cost.

\begin{figure}[t]
\centering
\includegraphics[width=0.98\textwidth]{fig2_core_artifact_evidence.pdf}
\caption{Core artifact-aware evidence at density 0.15. (a) Cost and route completion separate stationary cost reduction from progress-preserving behavior. (b) The progress-safety frontier separates PPO backbone, Risk-only, reward-only control, and runtime intervention. (c) Low-progress rate exposes the non-motion artifact. (d) TTC danger and intervention frequency show how runtime variants regulate the closed loop.}
\label{fig_core_evidence}
\end{figure}

\input{table_core_mechanism_pub.tex}

The PPO backbone is not selected as an artificially weakened baseline. It is the fixed learned policy used by the runtime-filter rows and is reported as a lower-bound/backbone comparator. Its zero-success result reflects the dense diagnostic success criterion: the policy still moves, with 20.7\% route completion and 41.1 km/h mean speed at density 0.15, but frequent collision or out-of-road cost prevents successful completion. The same sanity check applies to the PPO-Lagrangian row. It has 22.1\% route completion and 39.4 km/h mean speed, but collision and out-road rates of 69.2\% and 30.8\% prevent progress-preserving success. Risk-only is different: it has no collision or out-road cost because it almost does not move.

\begin{table}[!htbp]
\centering
\caption{Baseline sanity check at density 0.15. This table distinguishes failed-but-moving learned baselines from the stationary Risk-only artifact. PPO and PPO-Lagrangian have nontrivial speed and route progress but fail due to collision or out-road events, whereas Risk-only avoids cost by suppressing motion.}
\label{tab_baseline_sanity}
\footnotesize
\setlength{\tabcolsep}{4.0pt}
\begin{tabular}{@{}lrrrrl@{}}
\toprule
Baseline & Route & Speed & Collision & Out-road & Interpretation \\
\midrule
PPO backbone & 20.7 & 41.1 & 63.3 & 36.7 & moves but terminates with cost events \\
PPO-Lagrangian & 22.1 & 39.4 & 69.2 & 30.8 & moves but terminates with cost events \\
Risk-only & 0.9 & 0.0 & 0.0 & 0.0 & avoids cost through motion suppression \\
\bottomrule
\end{tabular}
\end{table}

Table~\ref{tab_baseline_sanity} is why the external RSS/TTC filter is included as a stronger runtime-filter comparator rather than relying only on PPO-family training baselines.

\subsection{Mechanism: execution-side runtime intervention}\label{sec_mechanism}
The second question is whether reward shaping alone explains the improvement. No-action guard retains the risk-oriented objective but disables execution-side action intervention; it remains at 100.0\% cost. Guard, Shield, and Gated-risk instead reduce cost to 18.3--20.8\% while preserving 85.7--86.9\% route completion. This comparison suggests that reward shaping alone is insufficient to explain the improvement. Under this comparison, the key difference is whether the proposed longitudinal command is bounded before execution. Guard and Shield share the same execution-side operator but differ in training context, so they should be read as runtime deployment variants rather than a clean single-factor ablation. The clean same-checkpoint runtime-operator contrast is reported separately in Table~\ref{tab_clean_runtime_ablation}. We therefore use Guard, Shield, and Gated-risk as a family-level intervention group rather than as a strict ranking among three independently controlled ablations. The intervention rate is high, about 68--71 interventions per 100 steps. This indicates that the improvement is not fully internalized learned-policy behavior; it is runtime mitigation of frequent monitor-flagged acceleration proposals.

\subsection{External baselines}\label{sec_external}
The third question is whether a simpler baseline already explains the result. Table~\ref{tab_external_baseline} and Fig.~\ref{fig_external} show that the TTC/RSS-style filter is a nontrivial runtime comparator: relative to the PPO backbone, it improves success to 53.3\% and reduces cost to 44.2\%. However, Guard, Shield, and Gated-risk reduce cost further, to 18.3--20.8\%, while preserving 85.7--86.9\% route completion. RSS/TTC also has a similar intervention frequency to the proposed variants, 71.7 interventions per 100 steps versus 67.9--70.8, so the remaining gap is not simply caused by intervening more often. In this implementation and diagnostic setting, the PPO-Lagrangian row did not recover a progress-preserving low-cost behavior; we therefore treat it as a protocol-specific constrained-baseline outcome rather than as a general statement about training-time constrained RL.

\begin{figure}[t]
\centering
\includegraphics[width=0.98\textwidth]{fig3_external_baselines.pdf}
\caption{External baseline comparison at density 0.15. Higher success and route completion are better, whereas lower cost is better. The TTC/RSS-style runtime filter improves over the PPO backbone but retains higher cost and a weaker progress-safety trade-off than the proposed runtime variants in this protocol.}
\label{fig_external}
\end{figure}

\input{table_external_baseline_pub.tex}

\subsection{Density stress and operating envelope}\label{sec_density}
The fourth question is whether the result remains stable under denser traffic. Density stress exposes an operating envelope rather than a universal safety guarantee. At density 0.08, runtime variants achieve high success and low cost; at density 0.25, success drops and cost rises. Table~\ref{tab_density_summary} summarizes the PPO-backbone comparison and the lowest-cost runtime variant at each density, while Fig.~\ref{fig_density} and Appendix~\ref{app_density} show the fixed-variant trends and full density diagnostics. Because Table~\ref{tab_density_summary} selects the lowest-cost runtime variant at each density, Fig.~\ref{fig_density} is the primary evidence for fixed-variant behavior; the table is only a compact operating-envelope summary. The fixed-variant curves in Fig.~\ref{fig_density} should therefore be treated as the primary comparison; Table~\ref{tab_density_summary} only summarizes the best observed member of the runtime family at each density. The degradation at high density is important evidence because it prevents an overbroad claim.

\begin{figure}[t]
\centering
\includegraphics[width=0.98\textwidth]{fig4_density_stress.pdf}
\caption{Traffic-density stress test. Runtime variants preserve progress-safety better than the PPO backbone at the tested densities, but the highest density remains difficult.}
\label{fig_density}
\end{figure}

\input{table_density_summary_pub.tex}

\subsection{Sensitivity to TTC threshold}\label{sec_sensitivity}
The TTC-threshold sweep in Fig.~\ref{fig_ttc_sensitivity} tests whether the main result depends on a single fixed threshold. Conservative thresholds can reduce cost but also change route completion and intervention frequency, which is expected for a runtime controller. The sensitivity rows are independent diagnostic reruns, not duplicates of the Table~\ref{tab_core_mechanism} default run; even a row with the same nominal threshold should therefore be read as trend evidence rather than as an exact numerical repeat. The target-speed sweep is reported in Appendix~\ref{app_sensitivity_runtime} as a secondary sensitivity result.

\begin{figure}[t]
\centering
\includegraphics[width=0.98\textwidth]{fig5_ttc_threshold_sensitivity.pdf}
\caption{TTC-threshold sensitivity at density 0.15. Heatmaps report success, cost, and route completion for Guard, Shield, and Gated-risk. The heatmap is an independent rerun; the TTC=12 cell is a same-nominal configuration but not the stored core-evaluation row in Table~\ref{tab_core_mechanism}. The sweep shows threshold-dependent trade-offs rather than a single universally optimal setting.}
\label{fig_ttc_sensitivity}
\end{figure}

\subsection{Runtime overhead}\label{sec_runtime_overhead}
The fifth question is whether the runtime loop creates an obvious simulation bottleneck. Figure~\ref{fig_runtime_overhead} reports policy inference p95, full control-loop p95, and intervention frequency across traffic densities. The p95 loop time can be lower or higher than the PPO backbone because episode length, density, and intervention frequency alter the simulator workload; it should not be interpreted as a pure microbenchmark of the guard computation. These measurements are Python simulation-loop diagnostics, not vehicle-grade real-time certification. Appendix~\ref{app_sensitivity_runtime} provides the compact p95 runtime summary, while full per-seed timing remains in supplementary CSV form.

\begin{figure}[t]
\centering
\includegraphics[width=0.98\textwidth]{fig6_simulation_loop_overhead.pdf}
\caption{Simulation-loop wall-clock diagnostics, not vehicle-grade real-time certification. The panels separate policy inference p95, full control-loop p95, and intervention frequency across traffic densities.}
\label{fig_runtime_overhead}
\end{figure}

\section{Discussion}\label{sec_discussion}

The central finding is that cost-only safe-RL evaluation can be misleading in dense driving simulation. Risk-only appears safe under collision-oriented cost but is not a useful driving policy because it nearly stops. GuardShield-Runtime changes the closed-loop behavior by moving part of safety regulation from reward optimization to runtime feedback intervention, where monitor-flagged acceleration commands can be bounded before execution and each intervention can be logged.

\subsection{Cybernetic interpretation}\label{sec_discussion_cybernetic}
The results can be read as a feedback-regulation problem. The runtime monitor serves as the sensor, the intervention operator serves as the actuator, the simulator response supplies feedback, and progress-safety diagnostics are the closed-loop outputs. Under this interpretation, the Risk-only failure is not simply a weak baseline. It is a degenerate feedback loop in which the policy reduces measured cost by avoiding interaction rather than regulating risk while making progress.

This cybernetic view also clarifies the role of the runtime variants. Guard and Shield alter the action before environment execution, so the feedback loop is changed at the actuator side. Gated-risk changes both the actuator side and the reward side, but only when motion or route progress indicates an active control state. The evidence therefore supports a bounded mechanism claim: simulator-level feedback intervention helps prevent a cost-only objective from being mistaken for progress-preserving low-cost behavior.

\subsection{What the evidence supports}\label{sec_discussion_evidence}
Table~\ref{tab_claim_evidence} summarizes the evidence boundary. The supported claims concern artifact diagnosis and simulator-level runtime intervention. The bounded claims concern density stress and runtime overhead. The method should be interpreted as a family of runtime feedback interventions, not as a single universally dominant controller. The fixed-variant density curves and sensitivity sweeps are therefore part of the main evidence rather than hidden in supplementary files.

\input{table_claim_evidence_pub.tex}

\subsection{Intervention burden and operating envelope}\label{sec_intervention_burden}
The runtime variants intervene in a large fraction of steps: approximately 68--71 interventions per 100 steps at density 0.15 and more than 80 interventions per 100 steps for the best low-density rows. This should not be interpreted as an ideal deployment property. It indicates that the learned backbone frequently proposes acceleration commands that the monitor flags as high risk under dense traffic. The present contribution is therefore runtime feedback mitigation and diagnostic exposure, not an autonomous policy that has internalized the shield.

The operating envelope is likewise bounded. Density stress shows that the runtime family remains useful at moderate density but degrades under the highest tested density. Sensitivity sweeps show that TTC threshold and target speed alter the balance among cost, route completion, and intervention frequency. These results argue for future training that reduces intervention burden by helping the learned policy internalize guard-compatible behavior, rather than treating high intervention frequency as a finished control solution.

\subsection{Limitations and threats to validity}\label{sec_limitations}
Internal validity is limited by the Guard/Shield training-context confound: they share the execution-side operator but are not a strict same-policy ablation. The most direct follow-up is a same-checkpoint runtime-on/off comparison for curriculum and no-curriculum PPO checkpoints. Construct validity is limited by heuristic TTC thresholds and by simulator definitions of success, cost, low-progress, and TTC danger. External validity is limited because all evidence comes from MetaDrive simulation rather than real vehicles or hardware-in-the-loop control. Statistical validity is limited by three independently trained seeds; Appendix~\ref{app_ci} reports episode-level intervals and seed ranges, but these do not replace larger training-seed replication. Runtime validity is limited because wall-clock measurements are Python simulation-loop timings rather than embedded real-time guarantees. The tested PPO-Lagrangian result is a baseline under this implementation and protocol, not a claim that all constrained RL methods fail. Step-level behavioral traces would be a useful qualitative visualization extension, but they are outside the present episode-level evidence package.

\section{Conclusion}\label{sec_conclusion}

GuardShield-Runtime reframes dense-traffic safe RL as cybernetic runtime feedback regulation. The central evidence is that Risk-only achieves zero cost by stopping, whereas execution-side runtime variants reduce cost while preserving route progress. The implication is practical but bounded: progress-safety behavior in closed-loop simulation should be evaluated with artifact-aware feedback diagnostics, not cost alone. Formal safety certification and real-world validation remain outside the present claim. This supports the view that machine-learning driving policies should be evaluated not only as optimized decision rules, but as components of monitored feedback systems whose closed-loop behavior can reveal proxy-objective artifacts.

\backmatter

\bmhead{Supplementary information}
The supplementary package includes anonymized episode-level results, aggregate tables, plotting scripts, table-generation scripts, and configuration files required to reproduce the reported figures and tables.

\section*{Declarations}

\bmhead{Funding}
The authors received no specific funding for this work.

\bmhead{Competing interests}
The authors declare no competing interests.

\bmhead{Ethics approval and consent to participate}
Not applicable. The study uses closed-loop driving simulation and does not involve human participants, human tissue, or animals.

\bmhead{Consent for publication}
Not applicable.

\bmhead{Data availability}
The anonymized submission package contains the raw episode CSVs, summary tables, generated publication figures, and source tables needed to reproduce the manuscript results.

\bmhead{Code availability}
The anonymized submission package contains the training, evaluation, diagnostic, table-generation, and figure-generation code used for the reported simulator study.

\bmhead{Use of AI-assisted tools}
AI-assisted tools were used only for language polishing and editorial organization. All technical content, experiments, code, and claims were verified by the authors.

\bmhead{Author contribution}
Author contributions are omitted for anonymous review and will be provided in the final version.

\begin{appendices}
\renewcommand{\theHtable}{appendix.\thesection.\arabic{table}}
\renewcommand{\theHfigure}{appendix.\thesection.\arabic{figure}}

\section{Reproducibility and Evidence Map}\label{app_manifest}
\setcounter{table}{0}
\setcounter{figure}{0}
This appendix groups reproducibility material by the manuscript claim it supports. The printed tables give the evidence map, detailed parameters, and result-block provenance; full episode-level files and table-ready aggregates are retained in the supplementary package.

\input{table_manifest_pub.tex}
\input{table_parameter_defaults_pub.tex}
\input{table_result_block_provenance_pub.tex}

\section{Statistical Reliability at Density 0.15}\label{app_ci}
\setcounter{table}{0}
\setcounter{figure}{0}
Appendix B reports episode-level uncertainty and seed variation for the density-0.15 diagnostic comparison. These intervals make the comparison auditable, but they do not replace larger training-seed replication. Wider Shield ranges support the family-level interpretation rather than a strict ranking among runtime variants.

\input{table_ci_binary_pub.tex}
\FloatBarrier
\input{table_seed_range_pub.tex}
\FloatBarrier

\section{Full Density Operating-Envelope Diagnostics}\label{app_density}
\setcounter{table}{0}
\setcounter{figure}{0}
The main text summarizes density stress in Fig.~\ref{fig_density} and Table~\ref{tab_density_summary}. Table~\ref{tab_full_density} reports the full method-by-density diagnostics. This table is included because the paper claims a bounded operating envelope, not universal safety.

\input{table_density_operating_envelope_pub.tex}
\FloatBarrier

\section{Sensitivity and Runtime Diagnostics}\label{app_sensitivity_runtime}
\setcounter{table}{0}
\setcounter{figure}{0}
This section reports secondary diagnostics that are useful for interpreting the controller but are not primary evidence for the main mechanism claim. The sensitivity results check whether the runtime variants depend on a single parameter choice. The runtime results report Python simulation-loop timing only; they are not embedded real-time guarantees.

The target-speed sweep is included to check whether the runtime controller simply benefits from an arbitrary low-speed setting. The observed pattern shows a real progress-safety coupling: lower speed can reduce cost, while moderate speed often preserves success and route completion.

\begin{figure}[H]
\centering
\includegraphics[width=0.98\textwidth]{figS1_target_speed_sensitivity.pdf}
\caption{Target-speed sensitivity at density 0.15. The sweep is reported as secondary sensitivity evidence because the main text focuses on TTC-threshold behavior.}
\label{fig_target_speed_sensitivity}
\end{figure}

\input{table_sensitivity_summary_pub.tex}
\input{table_runtime_summary_pub.tex}
\FloatBarrier

\end{appendices}

\begingroup
\small
\bibliography{references}
\endgroup

\end{document}
"""
    out = PKG / "main.tex"
    out.write_text(main, encoding="utf-8")
    return out


def copy_assets(paths: list[Path], table_paths: list[Path]) -> None:
    for pattern in ["fig*.pdf", "fig*.svg", "fig*.tiff", "fig*.png", "table_*_pub.tex"]:
        for stale in PKG.glob(pattern):
            stale.unlink()
    for p in paths:
        shutil.copy2(p, PKG / p.name)
    for p in table_paths:
        shutil.copy2(p, PKG / p.name)


def select_printed_tables(generated_tables: list[Path], names: list[str]) -> list[Path]:
    by_name = {p.name: p for p in generated_tables}
    missing = [name for name in names if name not in by_name]
    if missing:
        raise FileNotFoundError(f"Printed table(s) were not generated: {missing}")
    return [by_name[name] for name in names]


def write_revision_report(figure_paths: list[Path], main_tables: list[Path], appendix_tables: list[Path]) -> Path:
    report = CONTROL / "IJMLC_JOURNALIZATION_REPORT.md"
    lines = [
        "# IJMLC journalization revision report",
        "",
        f"- Generated at: {datetime.now().isoformat(timespec='seconds')}",
        "- Objective: convert the manuscript from an experiment-diagnostic report into an IJMLC-style machine-learning/cybernetics journal paper.",
        "- Boundary: simulator-level diagnostic improvement only; no formal safety or real-world safety certification is claimed.",
        "- Figure backend: Python/matplotlib only.",
        "",
        "## Requirements implemented",
        "",
        "- Reframed the title, abstract, introduction, method, results, discussion, and conclusion around cybernetic runtime feedback.",
        "- Added closed-loop formulation, TTC monitor definition, Guard operator equations, Shield/Gated-risk definitions, and Algorithm 1.",
        "- Expanded Related Work into safe RL, runtime shielding, cybernetic feedback, driving simulation, and positioning.",
        "- Reduced the visible main text to six tables: signals/parameters, compared methods, core mechanism, external baselines, density summary, and claim-to-evidence.",
        "- Kept the existing Fig. 1 architecture asset and rebuilt Fig. 2 as a four-panel artifact-aware core evidence figure.",
        "- Split TTC-threshold sensitivity into the main text and compact target-speed sensitivity into the appendix.",
        "- Compressed the appendix from raw diagnostic dumps into evidence map, uncertainty, density envelope, sensitivity, and runtime summaries.",
        "",
        "## Evidence limitation",
        "",
        "- Current raw CSV files are episode-level diagnostics. No step-level route/speed/TTC/intervention trace files were found, so representative episode trace plots were not fabricated.",
        "- Recommended next experiment: run a diagnostic evaluator with per-step logging for PPO, Risk-only, Guard, and Gated-risk at density 0.15.",
        "",
        "## Generated figures",
        "",
    ]
    for p in sorted(figure_paths):
        lines.append(f"- `{p.relative_to(ROOT)}`")
    lines += ["", "## Main-text tables", ""]
    for p in sorted(main_tables):
        lines.append(f"- `{p.relative_to(ROOT)}`")
    lines += ["", "## Printed appendix tables", ""]
    for p in sorted(appendix_tables):
        lines.append(f"- `{p.relative_to(ROOT)}`")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def update_manifest(report: Path) -> None:
    manifest_path = CONTROL / "manuscript_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    manifest["ijmlc_journalization_revision"] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "report": str(report.relative_to(ROOT)),
        "manuscript": str((PKG / "main.tex").relative_to(ROOT)),
        "claim_boundary": "simulation-level diagnostic improvement only",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    configure()
    tables = base.load_tables()
    appendix_tables = base.write_publication_tables(tables)
    main_tables = write_main_tables(tables)
    generated_tables = appendix_tables + main_tables
    printed_main_tables = select_printed_tables(generated_tables, MAIN_TEXT_TABLE_FILES)
    printed_appendix_tables = select_printed_tables(generated_tables, APPENDIX_TABLE_FILES)
    fig_paths = []
    fig_paths += draw_fig1_feedback_architecture()
    fig_paths += draw_fig2_core_evidence(tables)
    fig_paths += base.draw_external(tables)
    fig_paths += base.draw_density(tables)
    fig_paths += draw_fig5_ttc_sensitivity(tables)
    fig_paths += draw_fig_s1_target_speed(tables)
    fig_paths += draw_fig6_runtime(tables)
    copy_assets(fig_paths, printed_main_tables + printed_appendix_tables)
    write_main_tex()
    ensure_bibliography()
    report = write_revision_report(fig_paths, printed_main_tables, printed_appendix_tables)
    update_manifest(report)
    print(f"Journalized manuscript: {PKG / 'main.tex'}")
    print(f"Figures: {len(fig_paths)} assets")
    print(f"Printed main tables: {len(printed_main_tables)}")
    print(f"Printed appendix tables: {len(printed_appendix_tables)}")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
