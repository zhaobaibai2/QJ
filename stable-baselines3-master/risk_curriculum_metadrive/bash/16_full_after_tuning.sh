#!/usr/bin/env bash
SCRIPT_NAME="16_full_after_tuning"
source "$(dirname "$0")/common.sh"
run_main
record_command "${RUN_LOG_DIR}/check_env.log" python scripts/check_env.py --require-gpu
record_command "${RUN_LOG_DIR}/tuning.log" python scripts/run_suite.py --preset tuning --device "${DEVICE}" --skip-existing
record_command "${RUN_LOG_DIR}/validation.log" python scripts/run_suite.py --preset validation --device "${DEVICE}" --skip-existing
record_command "${RUN_LOG_DIR}/million.log" python scripts/run_suite.py --preset million --device "${DEVICE}" --skip-existing
finish_run completed
