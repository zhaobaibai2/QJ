#!/usr/bin/env bash
SCRIPT_NAME="06_paper"
source "$(dirname "$0")/common.sh"
run_main
record_command "${RUN_LOG_DIR}/paper.log" python scripts/run_suite.py --preset paper --device "${DEVICE}" ${EXTRA_ARGS:-}
finish_run completed
