#!/usr/bin/env bash
SCRIPT_NAME="17_all_paper_outputs"
source "$(dirname "$0")/common.sh"
run_main
PRESET="${PRESET:-paper}"
record_command "${RUN_LOG_DIR}/plot_results_${PRESET}.log" python scripts/plot_results.py --input-dir "outputs/${PRESET}/evaluations" --output-dir "outputs/${PRESET}/figures" --runs-dir "outputs/${PRESET}/runs"
record_command "${RUN_LOG_DIR}/plot_trajectories_${PRESET}.log" python scripts/plot_trajectories.py --runs-dir "outputs/${PRESET}/runs" --output-dir "outputs/${PRESET}/figures" --algo ppo --seed 0 --density 0.25
record_command "${RUN_LOG_DIR}/write_report_${PRESET}.log" python scripts/write_run_report.py --experiment-root "outputs/${PRESET}" --preset "${PRESET}" --status completed
record_command "${RUN_LOG_DIR}/build_paper.log" python scripts/build_paper.py
finish_run completed
