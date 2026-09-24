#!/usr/bin/env python
"""Draw the risk-curriculum MetaDrive framework diagram."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def box(ax, xy, wh, text, fc, ec="#263238"):
    patch = FancyBboxPatch(
        xy,
        wh[0],
        wh[1],
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=1.2,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + wh[0] / 2, xy[1] + wh[1] / 2, text, ha="center", va="center", fontsize=10)


def arrow(ax, start, end):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12, linewidth=1.2, color="#263238"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/stage1000_final_candidate/figures"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10.8, 5.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    box(ax, (0.4, 3.7), (1.9, 1.0), "MetaDrive\nscenario pool", "#E8F1FB")
    box(ax, (0.4, 1.5), (1.9, 1.0), "Adaptive\ncurriculum", "#EAF5EA")
    box(ax, (3.0, 3.7), (2.0, 1.0), "Observation\nlidar + ego state", "#F7F3E8")
    box(ax, (3.0, 1.5), (2.0, 1.0), "Risk metrics\nTTC, lane deviation", "#FBEDE8")
    box(ax, (5.7, 2.6), (1.9, 1.0), "PPO policy\nactor-critic", "#ECEAF7")
    box(ax, (8.2, 3.7), (1.4, 1.0), "Action\nsteer/throttle", "#E8F6F6")
    box(ax, (8.2, 1.5), (1.4, 1.0), "TTC shield\nsafe braking", "#F5EAF2")

    arrow(ax, (2.3, 4.2), (3.0, 4.2))
    arrow(ax, (2.3, 2.0), (3.0, 2.0))
    arrow(ax, (5.0, 4.2), (5.7, 3.25))
    arrow(ax, (5.0, 2.0), (5.7, 2.95))
    arrow(ax, (7.6, 3.1), (8.2, 4.0))
    arrow(ax, (7.6, 3.1), (8.2, 2.1))
    arrow(ax, (8.9, 2.5), (8.9, 3.7))
    arrow(ax, (8.2, 4.2), (9.6, 4.2))
    arrow(ax, (9.6, 4.2), (9.6, 5.2))
    arrow(ax, (9.6, 5.2), (0.4, 5.2))
    arrow(ax, (0.4, 5.2), (0.4, 4.7))

    ax.text(5.0, 5.35, "closed-loop interaction and logged paper metrics", ha="center", fontsize=10, color="#455A64")
    ax.text(5.0, 0.65, "reward = progress + success bonus - TTC/lane/control/cost/overspeed penalties", ha="center", fontsize=10, color="#455A64")

    fig.savefig(args.output_dir / "framework_diagram.pdf", bbox_inches="tight")
    fig.savefig(args.output_dir / "framework_diagram.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
