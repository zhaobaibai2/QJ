#!/usr/bin/env bash
SCRIPT_NAME="12_plot_trajectories"
source "$(dirname "$0")/common.sh"
run_main
PRESET="${PRESET:-paper}"
ALGO="${ALGO:-ppo}"
SEED="${SEED:-0}"
DENSITY="${DENSITY:-0.25}"
HORIZON="${HORIZON:-1000}"
record_command "${RUN_LOG_DIR}/plot_trajectories_${PRESET}.log" python scripts/plot_trajectories.py --runs-dir "outputs/${PRESET}/runs" --output-dir "outputs/${PRESET}/figures" --algo "${ALGO}" --seed "${SEED}" --density "${DENSITY}" --horizon "${HORIZON}"
finish_run completed
