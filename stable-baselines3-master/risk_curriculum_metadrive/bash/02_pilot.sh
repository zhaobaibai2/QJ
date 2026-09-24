#!/usr/bin/env bash
SCRIPT_NAME="02_pilot"
source "$(dirname "$0")/common.sh"
run_main
record_command "${RUN_LOG_DIR}/pilot.log" python scripts/run_suite.py --preset pilot --device "${DEVICE}" ${EXTRA_ARGS:-}
finish_run completed
