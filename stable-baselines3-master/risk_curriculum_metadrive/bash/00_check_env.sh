#!/usr/bin/env bash
SCRIPT_NAME="00_check_env"
source "$(dirname "$0")/common.sh"
run_main
record_command "${RUN_LOG_DIR}/check_env.log" python scripts/check_env.py --require-gpu
finish_run completed
