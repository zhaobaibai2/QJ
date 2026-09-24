#!/usr/bin/env bash
SCRIPT_NAME="01_smoke"
source "$(dirname "$0")/common.sh"
run_main
record_command "${RUN_LOG_DIR}/smoke.log" python scripts/run_suite.py --preset smoke --device "${DEVICE}" ${EXTRA_ARGS:-}
finish_run completed
