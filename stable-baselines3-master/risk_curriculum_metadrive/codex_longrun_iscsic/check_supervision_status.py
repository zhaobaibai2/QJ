#!/usr/bin/env python3
"""Lightweight supervisor for the risk_curriculum_metadrive evidence package.

This script is intentionally read-only unless --write is passed. It checks
runtime liveness, protocol integrity, and the paper-facing evidence package.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LONGRUN = ROOT / "codex_longrun_iscsic"
PAPER_TABLES = LONGRUN / "paper_tables_20260701_0258"
MANIFEST = LONGRUN / "final_paper_manifest_20260701_0415"

KEY_FILES = [
    LONGRUN / "EXPERIMENT_COMPLETION_AUDIT_20260701_0845.md",
    LONGRUN / "EXPERIMENT_REQUIREMENT_MATRIX_20260701_0845.csv",
    LONGRUN / "MANUSCRIPT_EVIDENCE_BRIEF_20260701_0848.md",
    MANIFEST / "table_manifest.csv",
    MANIFEST / "claim_boundary_matrix.csv",
    MANIFEST / "table1_formal_main_d015.csv",
    MANIFEST / "table2_ablation_d015.csv",
    MANIFEST / "table3_stress_ranked.csv",
    MANIFEST / "table4_external_seed_robustness.csv",
    MANIFEST / "table4_external_seed_robustness_d015_wilson95.csv",
]

TABLE_EXPECTATIONS = [
    (PAPER_TABLES / "main_comparators_nenv16.csv", 21),
    (PAPER_TABLES / "ablation_mechanism_nenv16.csv", 15),
    (PAPER_TABLES / "stress_density_020_025.csv", 14),
    (PAPER_TABLES / "gated_risk_mechanism_addendum.csv", 15),
    (PAPER_TABLES / "external_seed_robustness_mean.csv", 12),
    (PAPER_TABLES / "external_seed_robustness_d015_wilson95.csv", 6),
]

CONFIG_PATTERNS = [
    "outputs/tuned_compare_baseline_nenv16_seed*_1m/runs/*/config.json",
    "outputs/tuned_compare_risk_nenv16_seed*_1m/runs/*/config.json",
    "outputs/tuned_compare_curriculum_nenv16_seed*_1m/runs/*/config.json",
    "outputs/tuned_compare_shield_only_nenv16_seed*_1m/runs/*/config.json",
    "outputs/tuned_ablation_guard_only_nenv16_seed*_1m/runs/*/config.json",
    "outputs/tuned_ablation_no_action_guard_nenv16_seed*_1m/runs/*/config.json",
    "outputs/tuned_ablation_wo_ttc_nenv16_seed*_1m/runs/*/config.json",
    "outputs/tuned_ablation_wo_lane_nenv16_seed*_1m/runs/*/config.json",
    "outputs/tuned_ablation_wo_smooth_nenv16_seed*_1m/runs/*/config.json",
    "outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed*_1m/runs/*/config.json",
    "outputs/gated_risk_proposed_nenv16_seed*_1m/runs/*/config.json",
]

EVAL_PATTERNS = [
    "outputs/tuned_compare_*nenv16_seed*_1m/evaluations/*.csv",
    "outputs/tuned_ablation_*nenv16_seed*_1m/evaluations/*.csv",
    "outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed*_1m/evaluations/*.csv",
    "outputs/gated_risk_proposed_nenv16_seed*_1m/evaluations/*.csv",
    "outputs/stress_density_020_025_nenv16_20260701_0153/evaluations/*.csv",
    "outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346/evaluations/*.csv",
    "outputs/external_seed_robustness_nenv16_20260701_0425/evaluations/test_start_*/*.csv",
]


def run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    except Exception as exc:  # pragma: no cover - supervisor should not crash on missing tools
        return f"ERROR: {exc}"


def active_experiment_processes() -> list[str]:
    output = run(["ps", "-eo", "pid,ppid,stat,etime,pcpu,pmem,args"])
    rows = []
    # Keep this project-specific to avoid remote desktop/browser gpu-process false positives.
    needles = (
        "risk_curriculum_metadrive",
        "scripts/train.py",
        "scripts/evaluate",
        "run_one_defensive_proposed.py",
        "evaluate_from_config.py",
        "stable_baselines3",
        "metadriveenv",
    )
    ignore = (
        "check_supervision_status.py",
        "networkd-dispatcher",
        "unattended-upgrade",
        "gsd-screensaver",
        "sunlogin",
        "chrome",
        "xorg",
        "gpu-process",
    )
    for line in output.splitlines():
        low = line.lower()
        if any(n in low for n in needles) and not any(i in low for i in ignore):
            rows.append(line.rstrip())
    return rows


def gpu_summary() -> str:
    return run([
        "nvidia-smi",
        "--query-gpu=timestamp,name,memory.used,memory.total,utilization.gpu,temperature.gpu",
        "--format=csv,noheader,nounits",
    ]).strip()


def count_csv_rows(path: Path) -> int:
    with path.open(newline="") as f:
        return sum(1 for _ in csv.DictReader(f))


def check_key_files() -> list[tuple[str, bool, int]]:
    return [(str(p.relative_to(ROOT)), p.exists() and p.stat().st_size > 0, p.stat().st_size if p.exists() else 0) for p in KEY_FILES]


def check_tables() -> list[tuple[str, int, int, bool]]:
    checks = []
    for path, expected in TABLE_EXPECTATIONS:
        rows = count_csv_rows(path) if path.exists() else 0
        checks.append((str(path.relative_to(ROOT)), rows, expected, rows >= expected))
    return checks


def check_configs() -> tuple[int, list[str]]:
    configs = []
    for pattern in CONFIG_PATTERNS:
        configs.extend(ROOT.glob(pattern))
    bad = []
    for cfg in sorted(configs):
        data = json.loads(cfg.read_text())
        model = cfg.parent / "model" / "final_model.zip"
        if data.get("n_envs") != 16 or not model.exists():
            bad.append(str(cfg.relative_to(ROOT)))
    return len(configs), bad


def check_eval_csvs() -> tuple[int, list[str]]:
    evals = []
    for pattern in EVAL_PATTERNS:
        evals.extend(ROOT.glob(pattern))
    episode_csvs = [p for p in evals if p.name != "summary.csv"]
    bad = []
    for path in sorted(episode_csvs):
        with path.open(newline="") as f:
            vals = {row.get("eval_n_envs", "") for row in csv.DictReader(f) if "eval_n_envs" in row}
        if vals != {"16"}:
            bad.append(str(path.relative_to(ROOT)))
    return len(episode_csvs), bad


def render() -> str:
    now = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    procs = active_experiment_processes()
    gpu = gpu_summary()
    file_checks = check_key_files()
    table_checks = check_tables()
    cfg_count, cfg_bad = check_configs()
    eval_count, eval_bad = check_eval_csvs()

    status = "OK_IDLE" if not procs and not cfg_bad and not eval_bad and all(ok for _, ok, _ in file_checks) and all(ok for *_, ok in table_checks) else "ATTENTION"
    lines = [
        "# Supervision Status",
        "",
        f"Time: {now}",
        f"Root: {ROOT}",
        f"Status: {status}",
        "",
        "## Runtime",
        "",
        f"Active experiment processes: {len(procs)}",
    ]
    if procs:
        lines.extend(f"- {p}" for p in procs[:20])
    lines.extend(["", "GPU:", "", f"```text\n{gpu}\n```", ""])
    lines.extend(["## Evidence Files", "", "| file | ok | bytes |", "|---|---:|---:|"])
    lines.extend(f"| {name} | {ok} | {size} |" for name, ok, size in file_checks)
    lines.extend(["", "## Table Coverage", "", "| table | rows | expected_min | ok |", "|---|---:|---:|---:|"])
    lines.extend(f"| {name} | {rows} | {expected} | {ok} |" for name, rows, expected, ok in table_checks)
    lines.extend(["", "## Protocol Checks", ""])
    lines.append(f"- Accepted model configs checked: {cfg_count}; bad configs: {len(cfg_bad)}")
    lines.append(f"- Episode eval CSVs checked: {eval_count}; bad eval CSVs: {len(eval_bad)}")
    if cfg_bad:
        lines.append("- Bad configs: " + ", ".join(cfg_bad[:10]))
    if eval_bad:
        lines.append("- Bad eval CSVs: " + ", ".join(eval_bad[:10]))
    lines.extend([
        "",
        "## Decision",
        "",
        "No broad new training should be launched from this status alone. If Status is OK_IDLE, the next useful action is manuscript packaging or a narrowly scoped reviewer validation.",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write codex_longrun_iscsic/supervision_status_latest.md")
    args = parser.parse_args()
    text = render()
    print(text)
    if args.write:
        (LONGRUN / "supervision_status_latest.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
