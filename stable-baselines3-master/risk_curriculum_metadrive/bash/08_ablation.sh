#!/usr/bin/env bash
SCRIPT_NAME="08_ablation"
source "$(dirname "$0")/common.sh"
run_main
record_command "${RUN_LOG_DIR}/ablation.log" python scripts/run_suite.py --preset ablation --device "${DEVICE}" ${EXTRA_ARGS:-}
finish_run completed
