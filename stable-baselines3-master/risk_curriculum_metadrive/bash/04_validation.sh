#!/usr/bin/env bash
SCRIPT_NAME="04_validation"
source "$(dirname "$0")/common.sh"
run_main
record_command "${RUN_LOG_DIR}/validation.log" python scripts/run_suite.py --preset validation --device "${DEVICE}" ${EXTRA_ARGS:-}
finish_run completed
