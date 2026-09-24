#!/usr/bin/env bash
SCRIPT_NAME="03_tuning"
source "$(dirname "$0")/common.sh"
run_main
record_command "${RUN_LOG_DIR}/tuning.log" python scripts/run_suite.py --preset tuning --device "${DEVICE}" ${EXTRA_ARGS:-}
finish_run completed
