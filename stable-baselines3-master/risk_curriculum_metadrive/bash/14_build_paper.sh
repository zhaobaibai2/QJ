#!/usr/bin/env bash
SCRIPT_NAME="14_build_paper"
source "$(dirname "$0")/common.sh"
run_main
record_command "${RUN_LOG_DIR}/build_paper.log" python scripts/build_paper.py
finish_run completed
