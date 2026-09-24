#!/usr/bin/env bash
SCRIPT_NAME="13_write_report"
source "$(dirname "$0")/common.sh"
run_main
PRESET="${PRESET:-paper}"
STATUS="${STATUS:-completed}"
INCLUDE_SAC_FLAG=""
if [[ "${INCLUDE_SAC:-0}" == "1" ]]; then
  INCLUDE_SAC_FLAG="--include-sac"
fi
record_command "${RUN_LOG_DIR}/write_report_${PRESET}.log" python scripts/write_run_report.py --experiment-root "outputs/${PRESET}" --preset "${PRESET}" --status "${STATUS}" ${INCLUDE_SAC_FLAG}
finish_run completed
