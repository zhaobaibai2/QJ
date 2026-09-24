#!/usr/bin/env bash
SCRIPT_NAME="07_paper_with_sac"
source "$(dirname "$0")/common.sh"
run_main
record_command "${RUN_LOG_DIR}/paper_with_sac.log" python scripts/run_suite.py --preset paper --include-sac --device "${DEVICE}" ${EXTRA_ARGS:-}
finish_run completed
