#!/usr/bin/env bash
SCRIPT_NAME="05_million"
source "$(dirname "$0")/common.sh"
run_main
record_command "${RUN_LOG_DIR}/million.log" python scripts/run_suite.py --preset million --device "${DEVICE}" ${EXTRA_ARGS:-}
finish_run completed
