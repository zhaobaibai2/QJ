#!/usr/bin/env bash
set -u
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
RUN_GROUP=ijmlc_p2_external_20260701_1733
OUT_DIR=outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
STATUS=results/ijmlc_control/p2_external_baselines/rcpo_train_status.csv
MANIFEST=results/ijmlc_control/p2_external_baselines/p2_rcpo_lagrangian_manifest.csv
mkdir -p results/ijmlc_control/p2_external_baselines results/ijmlc_control/logs "$OUT_DIR"
echo "seed,status,start_time,end_time,exit_code,model_path,log_path" > "$STATUS"
for seed in 0 1 2; do
  LOG=results/ijmlc_control/logs/${RUN_GROUP}_rcpo_s${seed}.log
  MODEL="$OUT_DIR/rcpo_lagrangian_ppo_s${seed}/model/final_model.zip"
  START=$(date --iso-8601=seconds)
  echo "[$START] start rcpo seed=$seed n_envs=16 timesteps=1000000" | tee -a "$LOG"
  if [ -f "$MODEL" ]; then
    END=$(date --iso-8601=seconds)
    echo "$seed,skipped_existing,$START,$END,0,$MODEL,$LOG" >> "$STATUS"
    continue
  fi
  /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py \
    --variant rcpo_lagrangian --algo ppo --seed "$seed" --timesteps 1000000 --n-envs 16 --device cuda \
    --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 \
    --output-dir "$OUT_DIR" >> "$LOG" 2>&1
  code=$?
  END=$(date --iso-8601=seconds)
  status=done
  if [ "$code" -ne 0 ]; then status=failed; fi
  if [ ! -f "$MODEL" ] && [ "$code" -eq 0 ]; then status=missing_model; code=97; fi
  echo "$seed,$status,$START,$END,$code,$MODEL,$LOG" >> "$STATUS"
  if [ "$code" -ne 0 ]; then break; fi
done
/home/aaa/miniconda3/envs/sb3/bin/python - <<'PYMAN'
import csv, json
from pathlib import Path
root=Path('/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive')
status_path=root/'results/ijmlc_control/p2_external_baselines/rcpo_train_status.csv'
man_path=root/'results/ijmlc_control/p2_external_baselines/p2_rcpo_lagrangian_manifest.csv'
rows=[]
if status_path.exists():
    for r in csv.DictReader(status_path.open(newline='', encoding='utf-8')):
        model=Path(r['model_path'])
        cfg=model.parents[1]/'config.json'
        if model.exists() and cfg.exists():
            raw=json.loads(cfg.read_text(encoding='utf-8'))
            rows.append({
                'label':'rcpo_lagrangian','seed':r['seed'],'variant':'rcpo_lagrangian','algo':'ppo','role':'external_safe_rl',
                'status':'formal_trained' if r['status'] in {'done','skipped_existing'} else r['status'],
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
