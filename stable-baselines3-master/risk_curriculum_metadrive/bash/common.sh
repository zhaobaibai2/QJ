#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive"
BASH_ROOT="${PROJECT_ROOT}/bash"
LOG_ROOT="${BASH_ROOT}/logs"
RUN_HISTORY="${BASH_ROOT}/RUN_HISTORY.md"
CHANGELOG="${BASH_ROOT}/CHANGELOG.md"
CONDA_SH="${CONDA_SH:-/home/aaa/miniconda3/etc/profile.d/conda.sh}"
CONDA_ENV="${CONDA_ENV:-sb3}"
GPU_ID="${GPU_ID:-0}"
DEVICE="${DEVICE:-cuda}"
RUN_ID="${RUN_ID:-$(date +%Y%m%d_%H%M%S)_${SCRIPT_NAME:-run}}"
RUN_LOG_DIR="${LOG_ROOT}/${RUN_ID}"

export CUDA_VISIBLE_DEVICES="${GPU_ID}"
export PYTHONUNBUFFERED=1
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/mpl-racrl}"
export PYTHONHASHSEED="${PYTHONHASHSEED:-0}"

activate_sb3() {
  if [[ ! -f "${CONDA_SH}" ]]; then
    echo "Cannot find conda profile script: ${CONDA_SH}" >&2
    exit 1
  fi
  source "${CONDA_SH}"
  conda activate "${CONDA_ENV}"
}

prepare_run() {
  mkdir -p "${RUN_LOG_DIR}"
  cd "${PROJECT_ROOT}"
  touch "${RUN_HISTORY}"
  {
    echo "# Run ${RUN_ID}"
    echo "start_time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "script: ${SCRIPT_NAME:-unknown}"
    echo "project_root: ${PROJECT_ROOT}"
    echo "conda_env: ${CONDA_ENV}"
    echo "device: ${DEVICE}"
    echo "cuda_visible_devices: ${CUDA_VISIBLE_DEVICES}"
    echo "log_dir: ${RUN_LOG_DIR}"
    echo
    echo "## git"
    git rev-parse --short HEAD 2>/dev/null || true
    git status --short 2>/dev/null || true
    echo
    echo "## gpu"
    nvidia-smi 2>/dev/null || true
    echo
    echo "## python"
    which python || true
    python --version || true
  } > "${RUN_LOG_DIR}/environment.txt"
  git diff -- . ':!outputs' ':!bash/logs' > "${RUN_LOG_DIR}/code_diff.patch" 2>/dev/null || true
  git status --short > "${RUN_LOG_DIR}/git_status.txt" 2>/dev/null || true
  {
    echo
    echo "## ${RUN_ID}"
    echo
    echo "- **开始时间**: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "- **脚本**: \`${SCRIPT_NAME:-unknown}\`"
    echo "- **日志目录**: \`${RUN_LOG_DIR}\`"
    echo "- **GPU**: \`${CUDA_VISIBLE_DEVICES}\`"
    echo "- **状态**: running"
  } >> "${RUN_HISTORY}"
}

record_command() {
  local log_file="$1"
  shift
  {
    echo
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] COMMAND: $*"
    echo
  } | tee -a "${RUN_LOG_DIR}/commands.txt"
  "$@" 2>&1 | tee -a "${log_file}"
}

finish_run() {
  local status="$1"
  {
    echo
    echo "- **结束时间**: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "- **最终状态**: ${status}"
  } >> "${RUN_HISTORY}"
}

run_main() {
  activate_sb3
  prepare_run
  trap 'finish_run failed' ERR
}
