#!/usr/bin/env bash
set -euo pipefail

# 2026-06-30 nenv10 protocol update: proposed seed1 1.5M prehard
python scripts/train.py --variant proposed --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs
python scripts/evaluate_from_config.py --config-json outputs/iscsic_main_nenv10_1p5m_ent001/runs/proposed_ppo_s1/config.json --model outputs/iscsic_main_nenv10_1p5m_ent001/runs/proposed_ppo_s1/model/final_model.zip --episodes 50 --n-envs 10 --densities 0.0 0.08 0.15 --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/evaluations --device cuda


# 2026-06-30 diagnostic route-gate prehard seed1 nenv10
python scripts/train.py --variant proposed --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/tuning_routegate_prehard_nenv10_1p5m/runs
python scripts/evaluate_from_config.py --config-json outputs/tuning_routegate_prehard_nenv10_1p5m/runs/proposed_ppo_s1/config.json --model outputs/tuning_routegate_prehard_nenv10_1p5m/runs/proposed_ppo_s1/model/final_model.zip --episodes 50 --n-envs 10 --densities 0.0 0.08 0.15 --output-dir outputs/tuning_routegate_prehard_nenv10_1p5m/evaluations --device cuda


# 2026-06-30 diagnostic route-gate 0.80 prehard seed1 nenv10
python scripts/train.py --variant proposed --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/tuning_routegate080_prehard_nenv10_1p5m/runs
python scripts/evaluate_from_config.py --config-json outputs/tuning_routegate080_prehard_nenv10_1p5m/runs/proposed_ppo_s1/config.json --model outputs/tuning_routegate080_prehard_nenv10_1p5m/runs/proposed_ppo_s1/model/final_model.zip --episodes 50 --n-envs 10 --densities 0.0 0.08 0.15 --output-dir outputs/tuning_routegate080_prehard_nenv10_1p5m/evaluations --device cuda


# 2026-06-30 diagnostic low-learning-rate seed1 nenv10
python scripts/train.py --variant proposed --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --learning-rate 0.0001 --device cuda --output-dir outputs/tuning_lr1e4_prehard_nenv10_1p5m/runs
python scripts/evaluate_from_config.py --config-json outputs/tuning_lr1e4_prehard_nenv10_1p5m/runs/proposed_ppo_s1/config.json --model outputs/tuning_lr1e4_prehard_nenv10_1p5m/runs/proposed_ppo_s1/model/final_model.zip --episodes 50 --n-envs 10 --densities 0.0 0.08 0.15 --output-dir outputs/tuning_lr1e4_prehard_nenv10_1p5m/evaluations --device cuda
# 2026-06-30 monitor 1.5M convergence diagnostic, no new training launched
ps -eo pid,ppid,stat,etime,args | grep -E "run_one_defensive_proposed.py|run_defensive_ttc12_v18_s28_nenv10_1p5m|scripts/train.py|evaluate_from_config.py" | grep -v grep || true
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits
find outputs/defensive_ttc12_v18_nenv10_steps_diag_1p5m -maxdepth 4 -type f \( -name "defensive_proposed_ppo_s28.csv" -o -name "summary.csv" -o -name "final_model.zip" -o -name "checkpoint_*.zip" -o -name "*.log" \) -printf "%TY-%Tm-%Td %TH:%TM:%TS %s %p\n" | sort
tail -240 outputs/defensive_ttc12_v18_nenv10_steps_diag_1p5m/logs/defensive_s28_ttc12_v18_1p5m_*.log
# 2026-06-30 checkpoint diagnostic eval for 1.5M defensive seed28, screening only
for step in 375000 750000 1125000 1500000; do
  python scripts/evaluate_from_config.py \
    --config-json outputs/defensive_ttc12_v18_nenv10_steps_diag_1p5m/runs/defensive_proposed_ppo_s28/config.json \
    --model outputs/defensive_ttc12_v18_nenv10_steps_diag_1p5m/runs/defensive_proposed_ppo_s28/model/checkpoint_${step}_steps.zip \
    --episodes 20 \
    --densities 0.08 0.15 \
    --n-envs 10 \
    --device cuda \
    --output-dir outputs/defensive_ttc12_v18_nenv10_steps_diag_1p5m/checkpoint_eval/step_${step}
done
# 2026-06-30 ttc14/v18 500k screening, single-parameter tuning from ttc12 to ttc14
python scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 500000 --root outputs/tuning_ttc14_v18_nenv10_500k --ttc-threshold 14.0 --target-speed 18.0 --device cuda
# 2026-06-30 ttc12/v16 500k screening, single-parameter target_speed tuning from 18 to 16
python scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 500000 --root outputs/tuning_ttc12_v16_nenv10_500k --ttc-threshold 12.0 --target-speed 16.0 --device cuda
# 2026-06-30 P0 main comparison baseline seed1, n_envs=10, 1.5M, ent_coef=0.01
python scripts/train.py --variant baseline --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs
python scripts/evaluate_from_config.py --config-json outputs/iscsic_main_nenv10_1p5m_ent001/runs/baseline_ppo_s1/config.json --model outputs/iscsic_main_nenv10_1p5m_ent001/runs/baseline_ppo_s1/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/evaluations
# 2026-06-30 P0 main comparison baseline seed2, n_envs=10, 1.5M, ent_coef=0.01
python scripts/train.py --variant baseline --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs
python scripts/evaluate_from_config.py --config-json outputs/iscsic_main_nenv10_1p5m_ent001/runs/baseline_ppo_s2/config.json --model outputs/iscsic_main_nenv10_1p5m_ent001/runs/baseline_ppo_s2/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/evaluations
# 2026-06-30 P0 main comparison curriculum seed1, n_envs=10, 1.5M, ent_coef=0.01
python scripts/train.py --variant curriculum --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs
python scripts/evaluate_from_config.py --config-json outputs/iscsic_main_nenv10_1p5m_ent001/runs/curriculum_ppo_s1/config.json --model outputs/iscsic_main_nenv10_1p5m_ent001/runs/curriculum_ppo_s1/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/evaluations

# 2026-06-30 launch P0 main risk seed1, n_envs=10, 1.5M, ent_coef=0.01
python scripts/train.py --variant risk --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs
python scripts/evaluate_from_config.py --config-json outputs/iscsic_main_nenv10_1p5m_ent001/runs/risk_ppo_s1/config.json --model outputs/iscsic_main_nenv10_1p5m_ent001/runs/risk_ppo_s1/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/evaluations

# 2026-06-30 launch P0 main risk seed2, n_envs=10, 1.5M, ent_coef=0.01
python scripts/train.py --variant risk --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs
python scripts/evaluate_from_config.py --config-json outputs/iscsic_main_nenv10_1p5m_ent001/runs/risk_ppo_s2/config.json --model outputs/iscsic_main_nenv10_1p5m_ent001/runs/risk_ppo_s2/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/evaluations

# 2026-06-30 launch P0 main proposed seed2, n_envs=10, 1.5M, ent_coef=0.01
python scripts/train.py --variant proposed --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs
python scripts/evaluate_from_config.py --config-json outputs/iscsic_main_nenv10_1p5m_ent001/runs/proposed_ppo_s2/config.json --model outputs/iscsic_main_nenv10_1p5m_ent001/runs/proposed_ppo_s2/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/evaluations

# 2026-06-30 R1 reward screen completion_boost, n_envs=10, seed2, 500k
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
source /home/aaa/miniconda3/etc/profile.d/conda.sh
conda activate sb3
export CUDA_VISIBLE_DEVICES=0
export MPLCONFIGDIR=/tmp/mpl-racrl
python scripts/train.py --variant proposed --algo ppo --seed 2 --timesteps 500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --reward-progress 45 --reward-success-bonus 80 --device cuda --output-dir outputs/reward_screen_completion_boost_nenv10_500k/runs
python scripts/evaluate_from_config.py --config-json outputs/reward_screen_completion_boost_nenv10_500k/runs/proposed_ppo_s2/config.json --model outputs/reward_screen_completion_boost_nenv10_500k/runs/proposed_ppo_s2/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/reward_screen_completion_boost_nenv10_500k/evaluations

# 2026-06-30 R3 reward screen completion_plus_safety, n_envs=10, seed2, 500k
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
source /home/aaa/miniconda3/etc/profile.d/conda.sh
conda activate sb3
export CUDA_VISIBLE_DEVICES=0
export MPLCONFIGDIR=/tmp/mpl-racrl
python scripts/train.py --variant proposed --algo ppo --seed 2 --timesteps 500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --reward-progress 45 --reward-success-bonus 80 --reward-crash-penalty 120 --reward-out-of-road-penalty 120 --device cuda --output-dir outputs/reward_screen_completion_plus_safety_nenv10_500k/runs
python scripts/evaluate_from_config.py --config-json outputs/reward_screen_completion_plus_safety_nenv10_500k/runs/proposed_ppo_s2/config.json --model outputs/reward_screen_completion_plus_safety_nenv10_500k/runs/proposed_ppo_s2/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/reward_screen_completion_plus_safety_nenv10_500k/evaluations

# 2026-06-30 R2 reward screen safety_soften, n_envs=10, seed2, 500k
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
source /home/aaa/miniconda3/etc/profile.d/conda.sh
conda activate sb3
export CUDA_VISIBLE_DEVICES=0
export MPLCONFIGDIR=/tmp/mpl-racrl
python scripts/train.py --variant proposed --algo ppo --seed 2 --timesteps 500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --reward-cost 15 --reward-overspeed 1.0 --device cuda --output-dir outputs/reward_screen_safety_soften_nenv10_500k/runs
python scripts/evaluate_from_config.py --config-json outputs/reward_screen_safety_soften_nenv10_500k/runs/proposed_ppo_s2/config.json --model outputs/reward_screen_safety_soften_nenv10_500k/runs/proposed_ppo_s2/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/reward_screen_safety_soften_nenv10_500k/evaluations

# 2026-06-30 R4 mechanism screen no_action_guard, n_envs=10, seed2, 500k
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
source /home/aaa/miniconda3/etc/profile.d/conda.sh
conda activate sb3
export CUDA_VISIBLE_DEVICES=0
export MPLCONFIGDIR=/tmp/mpl-racrl
python scripts/train.py --variant no_action_guard --algo ppo --seed 2 --timesteps 500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/ablation_no_action_guard_nenv10_500k/runs
python scripts/evaluate_from_config.py --config-json outputs/ablation_no_action_guard_nenv10_500k/runs/no_action_guard_ppo_s2/config.json --model outputs/ablation_no_action_guard_nenv10_500k/runs/no_action_guard_ppo_s2/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/ablation_no_action_guard_nenv10_500k/evaluations

# 2026-06-30 mechanism screen proposed_wo_ttc, n_envs=10, seed2, 500k
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
source /home/aaa/miniconda3/etc/profile.d/conda.sh
conda activate sb3
export CUDA_VISIBLE_DEVICES=0
export MPLCONFIGDIR=/tmp/mpl-racrl
python scripts/train.py --variant proposed_wo_ttc --algo ppo --seed 2 --timesteps 500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/ablation_proposed_wo_ttc_nenv10_500k/runs
python scripts/evaluate_from_config.py --config-json outputs/ablation_proposed_wo_ttc_nenv10_500k/runs/proposed_wo_ttc_ppo_s2/config.json --model outputs/ablation_proposed_wo_ttc_nenv10_500k/runs/proposed_wo_ttc_ppo_s2/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/ablation_proposed_wo_ttc_nenv10_500k/evaluations

# 2026-06-30 R5 reward screen moderate_completion, n_envs=10, seed2, 500k
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
source /home/aaa/miniconda3/etc/profile.d/conda.sh
conda activate sb3
export CUDA_VISIBLE_DEVICES=0
export MPLCONFIGDIR=/tmp/mpl-racrl
python scripts/train.py --variant proposed --algo ppo --seed 2 --timesteps 500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --reward-progress 40 --reward-success-bonus 60 --device cuda --output-dir outputs/reward_screen_moderate_completion_nenv10_500k/runs
python scripts/evaluate_from_config.py --config-json outputs/reward_screen_moderate_completion_nenv10_500k/runs/proposed_ppo_s2/config.json --model outputs/reward_screen_moderate_completion_nenv10_500k/runs/proposed_ppo_s2/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/reward_screen_moderate_completion_nenv10_500k/evaluations

# 2026-06-30 P0 main curriculum seed2, n_envs=10, 1.5M
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
source /home/aaa/miniconda3/etc/profile.d/conda.sh
conda activate sb3
export CUDA_VISIBLE_DEVICES=0
export MPLCONFIGDIR=/tmp/mpl-racrl
python scripts/train.py --variant curriculum --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs
python scripts/evaluate_from_config.py --config-json outputs/iscsic_main_nenv10_1p5m_ent001/runs/curriculum_ppo_s2/config.json --model outputs/iscsic_main_nenv10_1p5m_ent001/runs/curriculum_ppo_s2/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/evaluations

# 2026-06-30 formal ablation proposed_wo_ttc seed2, n_envs=10, 1.5M
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
source /home/aaa/miniconda3/etc/profile.d/conda.sh
conda activate sb3
export CUDA_VISIBLE_DEVICES=0
export MPLCONFIGDIR=/tmp/mpl-racrl
python scripts/train.py --variant proposed_wo_ttc --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs
python scripts/evaluate_from_config.py --config-json outputs/iscsic_main_nenv10_1p5m_ent001/runs/proposed_wo_ttc_ppo_s2/config.json --model outputs/iscsic_main_nenv10_1p5m_ent001/runs/proposed_wo_ttc_ppo_s2/model/final_model.zip --episodes 50 --densities 0.00 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/evaluations

# 2026-06-30T14:00:53+08:00 nenv8 defensive seed26
nohup setsid bash codex_longrun_iscsic/run_defensive_ttc12_v18_s26_nenv8.sh > outputs/defensive_ttc12_v18_nenv8_final/logs/defensive_s26_nenv8_20260630_140018.log 2>&1 < /dev/null &

# 2026-06-30T14:21:39+08:00 nenv8 defensive seed27
nohup setsid bash codex_longrun_iscsic/run_defensive_ttc12_v18_s27_nenv8.sh > outputs/defensive_ttc12_v18_nenv8_final/logs/defensive_s27_nenv8_20260630_142139.log 2>&1 < /dev/null &

# 2026-06-30T14:24:15+08:00 stop nenv8 seed27 after protocol change
# archived to outputs/interrupted_nenv8_protocol_change_to_nenv16_20260630_142415

# 2026-06-30T14:25:31+08:00 nenv16 defensive seed26
nohup setsid bash codex_longrun_iscsic/run_defensive_ttc12_v18_s26_nenv16.sh > outputs/defensive_ttc12_v18_nenv16_final/logs/defensive_s26_nenv16_20260630_142531.log 2>&1 < /dev/null &

# 2026-06-30T14:42:40+08:00 nenv16 defensive seed27
nohup setsid bash codex_longrun_iscsic/run_defensive_ttc12_v18_s27_nenv16.sh > outputs/defensive_ttc12_v18_nenv16_final/logs/defensive_s27_nenv16_20260630_144235.log 2>&1 < /dev/null &

# 2026-06-30T14:44:48+08:00 stop nenv16 seed27 after protocol change to nenv32
# archived to outputs/interrupted_nenv16_protocol_change_to_nenv32_20260630_144448

# 2026-06-30T14:45:56+08:00 nenv32 defensive seed26
nohup setsid bash codex_longrun_iscsic/run_defensive_ttc12_v18_s26_nenv32.sh > outputs/defensive_ttc12_v18_nenv32_final/logs/defensive_s26_nenv32_20260630_144548.log 2>&1 < /dev/null &

# 2026-06-30T14:59:49+08:00 nenv16 defensive seed27 relaunched
nohup setsid bash codex_longrun_iscsic/run_defensive_ttc12_v18_s27_nenv16.sh > outputs/defensive_ttc12_v18_nenv16_final/logs/defensive_s27_nenv16_20260630_145943.log 2>&1 < /dev/null &
