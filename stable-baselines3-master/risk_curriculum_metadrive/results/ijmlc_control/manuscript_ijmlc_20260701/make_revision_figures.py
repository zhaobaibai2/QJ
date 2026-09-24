#!/usr/bin/env python3
"""Revision-only figures for the IJMLC manuscript."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
ROLLOUT_CSV = ROOT / "codex_longrun_iscsic" / "behavior_rollouts_20260701_0406" / "trajectory_points.csv"

COLORS = {
    "Risk-only": "#C44E52",
    "No-action guard": "#4C72B0",
    "Gated-risk": "#55A868",
}

VARIANT_LABELS = {
    "risk_only": "Risk-only",
    "no_action_guard": "No-action guard",
    "proposed_gated_risk": "Gated-risk",
}


def configure() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.0,
            "axes.titlesize": 8.5,
            "axes.labelsize": 8.0,
            "xtick.labelsize": 7.2,
            "ytick.labelsize": 7.2,
            "legend.fontsize": 7.2,
            "axes.linewidth": 0.7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def clean(ax, grid: bool = True) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(width=0.65, length=2.5)
    if grid:
        ax.grid(True, color="#DADDE3", linewidth=0.45, alpha=0.75)
        ax.set_axisbelow(True)


def block(ax, xy, wh, title, subtitle, color, title_size=9.2, subtitle_size=6.9):
    x, y = xy
    w, h = wh
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor="#FFFFFF",
            edgecolor=color,
            linewidth=1.1,
        )
    )
    ax.text(x + w / 2, y + h * 0.64, title, ha="center", va="center", fontsize=title_size, fontweight="bold", color="#20242B")
    ax.text(x + w / 2, y + h * 0.34, subtitle, ha="center", va="center", fontsize=subtitle_size, color="#4C5562", linespacing=1.12)


def arrow(ax, start, end, rad=0.0, color="#323842", lw=1.0):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>",
            mutation_scale=10,
            linewidth=lw,
            color=color,
        )
    )


def draw_fig1() -> None:
    fig, ax = plt.subplots(figsize=(7.25, 3.25))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    blocks = {
        "policy": ((0.045, 0.62), (0.18, 0.20), "Policy", r"$\pi_\phi(o_t)$"),
        "action": ((0.285, 0.62), (0.18, 0.20), "Action", r"$a_t^\pi$"),
        "monitor": ((0.045, 0.25), (0.20, 0.22), "Monitor", "TTC | speed\nroute | lane"),
        "intervention": ((0.305, 0.25), (0.20, 0.22), "Intervention", "bounded\nlongitudinal cmd"),
        "env": ((0.565, 0.43), (0.17, 0.21), "MetaDrive", "traffic plant"),
    }
    palette = {
        "policy": "#4E5D7A",
        "action": "#4E5D7A",
        "monitor": "#C65764",
        "intervention": "#C65764",
        "env": "#4F7C59",
    }
    for key, (xy, wh, title, subtitle) in blocks.items():
        block(ax, xy, wh, title, subtitle, palette[key])

    arrow(ax, (0.225, 0.72), (0.285, 0.72))
    arrow(ax, (0.405, 0.62), (0.405, 0.47), rad=0.00)
    arrow(ax, (0.245, 0.36), (0.305, 0.36))
    arrow(ax, (0.505, 0.39), (0.565, 0.49), rad=0.02)
    arrow(ax, (0.565, 0.58), (0.465, 0.72), rad=0.03)
    arrow(ax, (0.565, 0.44), (0.245, 0.28), rad=-0.08)

    ax.text(0.39, 0.925, "Policy decision layer", fontsize=8.2, fontweight="bold", ha="center", color="#4E5D7A")
    ax.text(0.27, 0.085, "Runtime safety-feedback layer", fontsize=8.2, fontweight="bold", ha="center", color="#C65764")
    ax.text(0.65, 0.205, "Audit and learning layer", fontsize=8.2, fontweight="bold", ha="center", color="#6C4A7E")

    ax.add_patch(
        FancyBboxPatch(
            (0.77, 0.22),
            0.19,
            0.54,
            boxstyle="round,pad=0.012,rounding_size=0.014",
            facecolor="#F4F1F7",
            edgecolor="#6C4A7E",
            linewidth=0.95,
        )
    )
    ax.text(0.865, 0.65, "Stationary\nartifact", ha="center", va="center", fontsize=8.6, fontweight="bold", color="#20242B")
    ax.text(0.865, 0.49, "Joint\ndiagnostics", ha="center", va="center", fontsize=8.6, fontweight="bold", color="#20242B")
    ax.text(0.865, 0.32, "Progress-preserving\nregulation", ha="center", va="center", fontsize=8.1, fontweight="bold", color="#20242B")
    arrow(ax, (0.865, 0.59), (0.865, 0.545), color="#6C4A7E", lw=0.9)
    arrow(ax, (0.865, 0.43), (0.865, 0.385), color="#6C4A7E", lw=0.9)
    arrow(ax, (0.735, 0.50), (0.77, 0.50), color="#6C4A7E", lw=0.9)

    fig.savefig(OUT / "fig1_cybernetic_feedback_architecture.pdf", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(OUT / "fig1_cybernetic_feedback_architecture.png", dpi=300, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def draw_rollout(density: float, outfile: str) -> None:
    df = pd.read_csv(ROLLOUT_CSV)
    df = df[(df["density"].round(2) == round(density, 2)) & (df["variant"].isin(VARIANT_LABELS))]
    df = df.copy()
    df["method"] = df["variant"].map(VARIANT_LABELS)

    fig, axs = plt.subplots(2, 2, figsize=(7.25, 4.65))
    ax_traj, ax_speed, ax_risk, ax_int = axs.ravel()

    for method in ["Risk-only", "No-action guard", "Gated-risk"]:
        sub = df[df["method"] == method].sort_values("step")
        c = COLORS[method]
        label = method
        ax_traj.plot(sub["x"], sub["y"], lw=1.45, color=c, label=label)
        ax_traj.scatter(sub["x"].iloc[0], sub["y"].iloc[0], s=18, color=c, marker="o")
        ax_traj.scatter(sub["x"].iloc[-1], sub["y"].iloc[-1], s=24, color=c, marker="x")
        ax_speed.plot(sub["step"], sub["speed_kmh"], lw=1.25, color=c, label=label)
        ax_risk.plot(sub["step"], sub["ttc_risk"], lw=1.25, color=c, label=label)
        ints = sub[sub["shield_intervention"] > 0]
        if len(ints):
            ax_int.vlines(ints["step"], 0, 1, color=c, alpha=0.22, linewidth=0.55)
        ax_int.plot(sub["step"], sub["shield_intervention"].rolling(20, min_periods=1).mean(), lw=1.25, color=c, label=label)

    ax_traj.set_title("(a) Trajectory")
    ax_traj.set_xlabel("x")
    ax_traj.set_ylabel("y")
    ax_traj.axis("equal")
    clean(ax_traj)

    ax_speed.set_title("(b) Speed over time")
    ax_speed.set_xlabel("step")
    ax_speed.set_ylabel("km/h")
    clean(ax_speed)

    ax_risk.set_title("(c) TTC-risk state")
    ax_risk.set_xlabel("step")
    ax_risk.set_ylabel("risk")
    ax_risk.set_ylim(-0.03, 1.03)
    clean(ax_risk)

    ax_int.set_title("(d) Intervention events")
    ax_int.set_xlabel("step")
    ax_int.set_ylabel("rolling intervention rate")
    ax_int.set_ylim(-0.03, 1.03)
    clean(ax_int)

    handles, labels = ax_speed.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.02))
    fig.suptitle(f"Representative rollout diagnostics at density {density:.2f}", y=1.075, fontsize=9.2, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(OUT / outfile, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def main() -> None:
    configure()
    # Fig. 1 is supplied manually; do not regenerate or overwrite it here.
    draw_rollout(0.15, "figS2_behavior_rollouts_density_0p15.pdf")
    draw_rollout(0.25, "figS3_behavior_rollouts_density_0p25.pdf")


if __name__ == "__main__":
    main()
