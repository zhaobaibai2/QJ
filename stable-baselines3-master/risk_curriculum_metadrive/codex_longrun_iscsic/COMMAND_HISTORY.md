
## 2026-06-30 stage2 strict-gate diagnostic
python scripts/train.py --variant proposed --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --stage2-success 0.35 --stage2-cost 0.35 --device cuda --output-dir outputs/tuning_stage2strict035_prehard_nenv10_1p5m/runs
python scripts/evaluate_from_config.py --config-json outputs/tuning_stage2strict035_prehard_nenv10_1p5m/runs/proposed_ppo_s1/config.json --model outputs/tuning_stage2strict035_prehard_nenv10_1p5m/runs/proposed_ppo_s1/model/final_model.zip --episodes 50 --densities 0.0 0.08 0.15 --n-envs 10 --device cuda --output-dir outputs/tuning_stage2strict035_prehard_nenv10_1p5m/evaluations

## 2026-06-30 defensive ttc12/v18 nenv10 seed26
python scripts/run_one_defensive_proposed.py --seed 26 --n-envs 10 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv10_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda

## 2026-06-30 defensive ttc12/v18 nenv10 seed27
python scripts/run_one_defensive_proposed.py --seed 27 --n-envs 10 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv10_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda

## 2026-06-30 defensive ttc12/v18 nenv10 seed28
python scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv10_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda
