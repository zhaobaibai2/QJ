#!/usr/bin/env bash
set -euo pipefail
PROJECT=/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
cd "$PROJECT"
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
  source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
  source "$HOME/anaconda3/etc/profile.d/conda.sh"
elif [ -f "/opt/conda/etc/profile.d/conda.sh" ]; then
  source "/opt/conda/etc/profile.d/conda.sh"
else
  echo "conda.sh not found" >&2
  exit 1
fi
conda activate sb3
export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0}
export MPLCONFIGDIR=${MPLCONFIGDIR:-/tmp/mpl-racrl}
ROOT=outputs/external_seed_robustness_nenv16_20260701_0425
N_ENVS=16
EPISODES=50
DEVICE=cuda
mkdir -p "$ROOT" "$ROOT/configs" "$ROOT/evaluations" "$ROOT/logs" "$ROOT/aggregate"
echo -e "label\ttrain_seed\ttest_start_seed\tdensities\tstatus\tstart\tend\teval_csv\tlog\tconfig_json\tmodel\tsource_run" > "$ROOT/status.tsv"
echo -e "label\ttrain_seed\tsource_run\tconfig_json\tmodel" > "$ROOT/source_manifest.tsv"

source_run_for() {
  local label="$1" seed="$2"
  case "$label" in
    guard_only) echo "outputs/tuned_ablation_guard_only_nenv16_seed${seed}_1m/runs/guard_only_ppo_s${seed}" ;;
    shield_only) echo "outputs/tuned_compare_shield_only_nenv16_seed${seed}_1m/runs/shield_only_ppo_s${seed}" ;;
    retuned_full) echo "outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed${seed}_1m/runs/proposed_ppo_s${seed}" ;;
    proposed_gated_risk) echo "outputs/gated_risk_proposed_nenv16_seed${seed}_1m/runs/proposed_gated_risk_ppo_s${seed}" ;;
    risk_only) echo "outputs/tuned_compare_risk_nenv16_seed${seed}_1m/runs/risk_ppo_s${seed}" ;;
    no_action_guard) echo "outputs/tuned_ablation_no_action_guard_nenv16_seed${seed}_1m/runs/no_action_guard_ppo_s${seed}" ;;
    *) echo "unknown label $label" >&2; return 2 ;;
  esac
}

valid_csv() {
  local csv_path="$1"
  [ -s "$csv_path" ] || return 1
  python - "$csv_path" <<'PYCSV'
import csv, sys
p = sys.argv[1]
with open(p, newline='') as f:
    rows = list(csv.DictReader(f))
if len(rows) >= 100 and {round(float(r['density']), 2) for r in rows if r.get('density')} >= {0.08, 0.15}:
    raise SystemExit(0)
raise SystemExit(1)
PYCSV
}

make_external_config() {
  local src_cfg="$1" dst_cfg="$2" label="$3" test_start="$4"
  python - "$src_cfg" "$dst_cfg" "$label" "$test_start" "$N_ENVS" "$EPISODES" <<'PYCFG'
import json, sys
src, dst, label, test_start, n_envs, episodes = sys.argv[1:]
with open(src, encoding='utf-8') as f:
    cfg = json.load(f)
cfg['variant'] = label
cfg['test_start_seed'] = int(test_start)
cfg['n_envs'] = int(n_envs)
cfg['eval_episodes'] = int(episodes)
with open(dst, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
PYCFG
}

aggregate_results() {
  python - "$ROOT" <<'PYAGG'
import csv
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

root = Path(sys.argv[1])
metrics = [
    'success', 'cost', 'route_completion', 'collision', 'out_of_road',
    'mean_speed_kmh', 'mean_lane_deviation', 'ttc_risk',
    'shield_intervention_rate', 'overspeed_guard_rate', 'risk_gate_rate',
]

def to_float(v):
    try:
        x = float(v)
    except Exception:
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    return x

def mean(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else ''

def std(vals):
    vals = [v for v in vals if v is not None]
    return statistics.stdev(vals) if len(vals) > 1 else 0.0 if len(vals) == 1 else ''

status_path = root / 'status.tsv'
status_rows = []
with status_path.open(newline='') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        status_rows.append(row)

all_rows = []
for st in status_rows:
    if st.get('status') not in {'ok', 'skipped_existing'}:
        continue
    p = Path(st['eval_csv'])
    if not p.exists():
        p = Path.cwd() / st['eval_csv']
    if not p.exists():
        continue
    with p.open(newline='') as f:
        for row in csv.DictReader(f):
            row['label'] = st['label']
            row['train_seed'] = st['train_seed']
            row['test_start_seed'] = st['test_start_seed']
            row['source_run'] = st['source_run']
            all_rows.append(row)

out_all = root / 'aggregate' / 'all_episode_rows.csv'
if all_rows:
    fieldnames = list(all_rows[0].keys())
    for extra in ['label', 'train_seed', 'test_start_seed', 'source_run']:
        if extra not in fieldnames:
            fieldnames.append(extra)
    with out_all.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader(); w.writerows(all_rows)

unit_groups = defaultdict(list)
for row in all_rows:
    key = (row['label'], row['train_seed'], row['test_start_seed'], f"{float(row['density']):.2f}")
    unit_groups[key].append(row)
unit_rows = []
for (label, seed, test_start, density), rows in sorted(unit_groups.items()):
    rec = {'label': label, 'train_seed': seed, 'test_start_seed': test_start, 'density': density, 'n_episodes': len(rows)}
    for m in metrics:
        rec[m] = mean([to_float(r.get(m, '')) for r in rows])
    unit_rows.append(rec)
with (root / 'aggregate' / 'summary_by_eval_unit.csv').open('w', newline='') as f:
    fields = ['label', 'train_seed', 'test_start_seed', 'density', 'n_episodes'] + metrics
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(unit_rows)

label_groups = defaultdict(list)
for r in unit_rows:
    label_groups[(r['label'], r['density'])].append(r)
label_rows = []
for (label, density), rows in sorted(label_groups.items()):
    rec = {'label': label, 'density': density, 'n_eval_units': len(rows), 'n_episodes': sum(int(r['n_episodes']) for r in rows)}
    for m in metrics:
        vals = [to_float(r.get(m, '')) for r in rows]
        rec[f'{m}_mean'] = mean(vals)
        rec[f'{m}_std_across_units'] = std(vals)
    label_rows.append(rec)
with (root / 'aggregate' / 'mean_by_label_density.csv').open('w', newline='') as f:
    fields = ['label', 'density', 'n_eval_units', 'n_episodes'] + [x for m in metrics for x in (f'{m}_mean', f'{m}_std_across_units')]
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(label_rows)

test_groups = defaultdict(list)
for r in unit_rows:
    test_groups[(r['test_start_seed'], r['label'], r['density'])].append(r)
test_rows = []
for (test_start, label, density), rows in sorted(test_groups.items()):
    rec = {'test_start_seed': test_start, 'label': label, 'density': density, 'n_eval_units': len(rows), 'n_episodes': sum(int(r['n_episodes']) for r in rows)}
    for m in metrics:
        rec[m] = mean([to_float(r.get(m, '')) for r in rows])
    test_rows.append(rec)
with (root / 'aggregate' / 'mean_by_test_start_label_density.csv').open('w', newline='') as f:
    fields = ['test_start_seed', 'label', 'density', 'n_eval_units', 'n_episodes'] + metrics
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(test_rows)

rank_rows = [r for r in label_rows if r['density'] == '0.15']
rank_rows.sort(key=lambda r: (-(to_float(r.get('success_mean')) or -1), (to_float(r.get('cost_mean')) or 999), -(to_float(r.get('route_completion_mean')) or -1)))
for i, r in enumerate(rank_rows, 1):
    r['rank_success_cost_route'] = i
with (root / 'aggregate' / 'rank_density_0p15.csv').open('w', newline='') as f:
    fields = ['rank_success_cost_route'] + list(rank_rows[0].keys()) if rank_rows else ['rank_success_cost_route']
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rank_rows)

lines = ['# External Seed Robustness Decision', '', 'Protocol: frozen trained models, n_envs=16, test_start_seed in {20000, 30000}, densities 0.08 and 0.15, 50 episodes per density per trained seed.', '', '## Density 0.15 ranking', '']
for r in rank_rows:
    lines.append(f"{r['rank_success_cost_route']}. {r['label']}: success={float(r['success_mean']):.3f}, cost={float(r['cost_mean']):.3f}, route={float(r['route_completion_mean']):.3f}, units={r['n_eval_units']}, episodes={r['n_episodes']}")
lines += ['', '## Claim boundary', '', '- This is external scenario-seed validation of frozen models, not additional training or tuning.', '- Use it to support robustness of the guard/shield-centered conclusion if positive methods remain ahead of risk-only/no-action-guard controls.', '- If a positive method drops materially below the formal held-out table, report the drop as external-seed sensitivity rather than hiding it.', '- Risk-only zero-cost rows must still be interpreted together with route completion.']
(root / 'aggregate' / 'DECISION.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('aggregate_root=' + str(root / 'aggregate'))
print('episode_rows=' + str(len(all_rows)))
print('eval_units=' + str(len(unit_rows)))
PYAGG
}

LABELS=(guard_only shield_only retuned_full proposed_gated_risk risk_only no_action_guard)
SEEDS=(0 1 2)
TEST_STARTS=(20000 30000)
DENSITIES="0.08 0.15"

for label in "${LABELS[@]}"; do
  for seed in "${SEEDS[@]}"; do
    run_dir=$(source_run_for "$label" "$seed")
    cfg="$run_dir/config.json"
    model="$run_dir/model/final_model.zip"
    echo -e "${label}\t${seed}\t${run_dir}\t${cfg}\t${model}" >> "$ROOT/source_manifest.tsv"
    if [ ! -f "$cfg" ] || [ ! -f "$model" ]; then
      echo "missing model/config for $label seed $seed: $run_dir" >&2
      exit 2
    fi
  done
done

for test_start in "${TEST_STARTS[@]}"; do
  eval_dir="$ROOT/evaluations/test_start_${test_start}"
  mkdir -p "$eval_dir"
  for label in "${LABELS[@]}"; do
    for seed in "${SEEDS[@]}"; do
      run_dir=$(source_run_for "$label" "$seed")
      src_cfg="$run_dir/config.json"
      model="$run_dir/model/final_model.zip"
      ext_cfg="$ROOT/configs/${label}_s${seed}_test${test_start}.json"
      out_csv="$eval_dir/${label}_ppo_s${seed}.csv"
      log="$ROOT/logs/${label}_s${seed}_test${test_start}.log"
      make_external_config "$src_cfg" "$ext_cfg" "$label" "$test_start"
      start=$(date -Is)
      if valid_csv "$out_csv"; then
        echo -e "${label}\t${seed}\t${test_start}\t${DENSITIES}\tskipped_existing\t${start}\t$(date -Is)\t${out_csv}\t${log}\t${ext_cfg}\t${model}\t${run_dir}" >> "$ROOT/status.tsv"
        continue
      fi
      echo "[$(date -Is)] eval label=${label} seed=${seed} test_start=${test_start}" | tee "$log"
      if timeout 45m python scripts/evaluate_from_config.py \
        --config-json "$ext_cfg" \
        --model "$model" \
        --episodes "$EPISODES" \
        --densities 0.08 0.15 \
        --output-dir "$eval_dir" \
        --device "$DEVICE" \
        --n-envs "$N_ENVS" >> "$log" 2>&1; then
        # evaluate_from_config names by config.variant/config.seed; with config variant overridden, this path should exist.
        if [ ! -f "$out_csv" ]; then
          echo "expected csv missing: $out_csv" >> "$log"
          echo -e "${label}\t${seed}\t${test_start}\t${DENSITIES}\tmissing_csv\t${start}\t$(date -Is)\t${out_csv}\t${log}\t${ext_cfg}\t${model}\t${run_dir}" >> "$ROOT/status.tsv"
          exit 3
        fi
        echo -e "${label}\t${seed}\t${test_start}\t${DENSITIES}\tok\t${start}\t$(date -Is)\t${out_csv}\t${log}\t${ext_cfg}\t${model}\t${run_dir}" >> "$ROOT/status.tsv"
        aggregate_results || true
      else
        rc=$?
        echo "evaluation failed rc=$rc" >> "$log"
        echo -e "${label}\t${seed}\t${test_start}\t${DENSITIES}\tfailed_rc_${rc}\t${start}\t$(date -Is)\t${out_csv}\t${log}\t${ext_cfg}\t${model}\t${run_dir}" >> "$ROOT/status.tsv"
        aggregate_results || true
        exit "$rc"
      fi
    done
  done
done
aggregate_results
cat > "$ROOT/README.md" <<'EOF'
# External Seed Robustness n_envs=16

Frozen-model reviewer validation. This sweep reuses completed formal models and changes only `test_start_seed` to 20000 and 30000. It evaluates densities 0.08 and 0.15 with 50 episodes per density, n_envs=16.

Use `aggregate/mean_by_label_density.csv`, `aggregate/rank_density_0p15.csv`, and `aggregate/DECISION.md` for paper-facing interpretation. Raw per-episode rows are in `aggregate/all_episode_rows.csv`.
EOF
# Paper package pointer is only written after full completion.
cat > codex_longrun_iscsic/paper_tables_20260701_0258/external_seed_robustness_pending.md <<EOF
# External seed robustness pending

Started external seed robustness sweep at $(date -Is).
Root: $ROOT
Protocol: frozen models, n_envs=16, test_start_seed 20000/30000, densities 0.08/0.15, 50 episodes per density.
EOF
