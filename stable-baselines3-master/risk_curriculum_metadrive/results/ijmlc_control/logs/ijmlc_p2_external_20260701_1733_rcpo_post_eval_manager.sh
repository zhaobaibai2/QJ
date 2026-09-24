#!/usr/bin/env bash
set -u
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
RUN_GROUP=ijmlc_p2_external_20260701_1733
RCPO_PID_FILE=results/ijmlc_control/logs/${RUN_GROUP}_rcpo_train_manager.pid
STATUS=results/ijmlc_control/p2_external_baselines/rcpo_post_eval_status.csv
MANIFEST=results/ijmlc_control/p2_external_baselines/p2_rcpo_lagrangian_manifest.csv
NORMAL_DIR=results/ijmlc_control/p2_external_baselines/rcpo_normal_eval_nenv16
mkdir -p results/ijmlc_control/p2_external_baselines results/ijmlc_control/logs "$NORMAL_DIR"
echo "stage,seed,status,start_time,end_time,exit_code,output_path,log_path" > "$STATUS"
# Wait until training manager exits and manifest exists.
while true; do
  if [ -f "$RCPO_PID_FILE" ]; then
    pid=$(cat "$RCPO_PID_FILE" 2>/dev/null || true)
    if [ -n "$pid" ] && ps -p "$pid" >/dev/null 2>&1; then
      sleep 60
      continue
    fi
  fi
  break
done
# Rebuild manifest in case the train manager was killed after models were written.
/home/aaa/miniconda3/envs/sb3/bin/python - <<'PYMAN'
import csv, json
from pathlib import Path
root=Path('/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive')
out_dir=root/'outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16'
man_path=root/'results/ijmlc_control/p2_external_baselines/p2_rcpo_lagrangian_manifest.csv'
rows=[]
for seed in [0,1,2]:
    model=out_dir/f'rcpo_lagrangian_ppo_s{seed}/model/final_model.zip'
    cfg=out_dir/f'rcpo_lagrangian_ppo_s{seed}/config.json'
    if model.exists() and cfg.exists():
        raw=json.loads(cfg.read_text(encoding='utf-8'))
        rows.append({
            'label':'rcpo_lagrangian','seed':str(seed),'variant':'rcpo_lagrangian','algo':'ppo','role':'external_safe_rl','status':'formal_trained',
            'config_exists':str(cfg.exists()),'model_exists':str(model.exists()),'n_envs':str(raw.get('n_envs','')),
            'timesteps':str(raw.get('timesteps','')),'use_risk_reward':str(raw.get('use_risk_reward','')),
            'use_action_guard':str(raw.get('use_action_guard','')),
            'target_speed_kmh':str((raw.get('reward_weights') or {}).get('target_speed_kmh','')),
            'ttc_threshold':str((raw.get('reward_weights') or {}).get('ttc_threshold','')),
            'run_dir':str(model.parents[1]),'config_json':str(cfg),'model':str(model),
            'ijmlc_missing_metrics':'needs_diagnostic_eval','next_action':'evaluate_ijmlc_diagnostics and evaluate_from_config n_envs16'
        })
fields=['label','seed','variant','algo','role','status','config_exists','model_exists','n_envs','timesteps','use_risk_reward','use_action_guard','target_speed_kmh','ttc_threshold','run_dir','config_json','model','ijmlc_missing_metrics','next_action']
with man_path.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
print(f'wrote_manifest={man_path} rows={len(rows)}')
PYMAN
rows=$(tail -n +2 "$MANIFEST" 2>/dev/null | wc -l || echo 0)
if [ "$rows" -lt 3 ]; then
  echo "manifest_has_${rows}_rows_not_3" >> results/ijmlc_control/logs/${RUN_GROUP}_rcpo_post_eval_manager.out
  exit 0
fi
for seed in 0 1 2; do
  cfg=$(awk -F, -v s="$seed" 'NR>1 && $2==s {print $16}' "$MANIFEST")
  model=$(awk -F, -v s="$seed" 'NR>1 && $2==s {print $17}' "$MANIFEST")
  LOG=results/ijmlc_control/logs/${RUN_GROUP}_rcpo_normal_eval_s${seed}.log
  OUT=${NORMAL_DIR}/rcpo_lagrangian_ppo_s${seed}.csv
  START=$(date --iso-8601=seconds)
  /home/aaa/miniconda3/envs/sb3/bin/python scripts/evaluate_from_config.py \
    --config-json "$cfg" --model "$model" --episodes 40 --densities 0.08 0.15 0.20 0.25 \
    --output-dir "$NORMAL_DIR" --device cuda --n-envs 16 >> "$LOG" 2>&1
  code=$?
  END=$(date --iso-8601=seconds)
  status=done; if [ "$code" -ne 0 ]; then status=failed; fi
  echo "normal_eval,$seed,$status,$START,$END,$code,$OUT,$LOG" >> "$STATUS"
  if [ "$code" -ne 0 ]; then exit "$code"; fi
done
# IJMLC diagnostics can run in 3 single-env shards after normal eval.
for seed in 0 1 2; do
  (
    RUN_ID=${RUN_GROUP}_rcpo_diag_s${seed}
    LOG=results/ijmlc_control/logs/${RUN_ID}.log
    RAW=results/ijmlc_control/raw_csv/${RUN_ID}_episodes.csv
    START=$(date --iso-8601=seconds)
    /home/aaa/miniconda3/envs/sb3/bin/python scripts/evaluate_ijmlc_diagnostics.py \
      --manifest "$MANIFEST" --labels rcpo_lagrangian --seeds "$seed" \
      --densities 0.08 0.15 0.20 0.25 --test-start-seeds 10000 20000 --episodes-per-start 20 \
      --device cuda --run-id "$RUN_ID" >> "$LOG" 2>&1
    code=$?
    END=$(date --iso-8601=seconds)
    status=done; if [ "$code" -ne 0 ]; then status=failed; fi
    echo "diagnostic_eval,$seed,$status,$START,$END,$code,$RAW,$LOG" >> "$STATUS"
  ) &
done
wait
