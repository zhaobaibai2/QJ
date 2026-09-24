#!/usr/bin/env bash
SCRIPT_NAME="11_plot_results"
source "$(dirname "$0")/common.sh"
run_main
PRESET="${PRESET:-paper}"
SMOOTH="${SMOOTH:-30}"
record_command "${RUN_LOG_DIR}/plot_results_${PRESET}.log" python scripts/plot_results.py --input-dir "outputs/${PRESET}/evaluations" --output-dir "outputs/${PRESET}/figures" --runs-dir "outputs/${PRESET}/runs" --smooth "${SMOOTH}"
finish_run completed
