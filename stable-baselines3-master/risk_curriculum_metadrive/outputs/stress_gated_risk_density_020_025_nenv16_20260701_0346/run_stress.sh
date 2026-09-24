#!/usr/bin/env bash
set -euo pipefail
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
  source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
  source "$HOME/anaconda3/etc/profile.d/conda.sh"
else
  source /opt/conda/etc/profile.d/conda.sh
fi
conda activate sb3
ROOT=outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346
echo -e "seed\tstatus\tstart\tend\teval_csv" > "$ROOT/status.tsv"
for SEED in 0 1 2; do
  START=$(date -Is)
  CFG="outputs/gated_risk_proposed_nenv16_seed${SEED}_1m/runs/proposed_gated_risk_ppo_s${SEED}/config.json"
  MODEL="outputs/gated_risk_proposed_nenv16_seed${SEED}_1m/runs/proposed_gated_risk_ppo_s${SEED}/model/final_model.zip"
  LOG="$ROOT/logs/eval_seed${SEED}.log"
  OUT="$ROOT/evaluations/proposed_gated_risk_ppo_s${SEED}.csv"
  if python scripts/evaluate_from_config.py --config-json "$CFG" --model "$MODEL" --episodes 50 --densities 0.20 0.25 --output-dir "$ROOT/evaluations" --device cuda --n-envs 16 > "$LOG" 2>&1; then
    echo -e "${SEED}\tok\t${START}\t$(date -Is)\t${OUT}" >> "$ROOT/status.tsv"
  else
    echo -e "${SEED}\tfailed\t${START}\t$(date -Is)\t${OUT}" >> "$ROOT/status.tsv"
    exit 1
  fi
done
