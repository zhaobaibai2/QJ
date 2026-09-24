# REWARD_TUNING_LEDGER

用于记录 reward 调参 screen。每条记录必须包含：目录、命令、seed、n_envs、timesteps、reward weights、评估 CSV、density metrics、是否扩展。


## R1 completion_boost planned/launched 2026-06-30
- Hypothesis: current hard-stage success is limited by weak terminal/progress incentive relative to safety/guard/overspeed terms.
- Change from current reward: reward_progress 30 -> 45; reward_success_bonus 40 -> 80; other RewardWeights unchanged.
- Protocol: variant=proposed, seed=2, timesteps=500,000, horizon=1200, n_envs=10, ent_coef=0.01, eval_n_envs=10, 50 episodes at densities 0.00/0.08/0.15.
- Output root: outputs/reward_screen_completion_boost_nenv10_500k
- Status: launching after proposed seed2 formal run completed.

### R1 early monitor 2026-06-30 ~348k
- Current training progress: ~348,160/500,000 timesteps.
- Recent stage2 metrics: window_success up to 0.333, window_cost around 0.033; rollout success_rate around 0.33-0.43.
- Early decision: continue to final evaluation. No parameter change mid-run.

## R1 completion_boost result 2026-06-30
- Output root: outputs/reward_screen_completion_boost_nenv10_500k
- CSV: outputs/reward_screen_completion_boost_nenv10_500k/evaluations/proposed_ppo_s2.csv
- Reward changes: progress=45, success_bonus=80; other weights unchanged.
- d0.00: success=0.90, cost=0.00, route=0.983, collision=0.00, out=0.00, shield=0.860
- d0.08: success=0.90, cost=0.02, route=0.968, collision=0.02, out=0.00, shield=0.847
- d0.15: success=0.32, cost=0.52, route=0.761, collision=0.52, out=0.00, shield=0.725
- Decision: fail as a direct final candidate because high-density success/cost worsened versus proposed seed2. Use this as evidence that completion incentive alone is insufficient; run R3 with stronger crash/out penalties.

## R3 completion_plus_safety launched 2026-06-30
- Hypothesis: R1 improved low/medium completion but high-density collision remained too high; stronger crash/out penalties may retain completion gain while reducing high-density cost.
- Reward changes: progress 30 -> 45; success_bonus 40 -> 80; crash_penalty 80 -> 120; out_of_road_penalty 80 -> 120.
- Protocol: proposed seed2, 500k, horizon=1200, n_envs=10, ent_coef=0.01, eval_n_envs=10.
- Output root: outputs/reward_screen_completion_plus_safety_nenv10_500k
- Status: launched.

### R3 mid monitor 2026-06-30 ~379k
- Current training progress: ~378,880/500,000 timesteps.
- Signal: weaker than R1; stage around 0/1, success_rate around 0.10-0.16, speed and route lagging.
- Decision: continue to evaluation because run is near completion, but likely not a promising expansion unless final d0.15 safety improves substantially.

## R3 completion_plus_safety result 2026-06-30
- Output root: outputs/reward_screen_completion_plus_safety_nenv10_500k
- CSV: outputs/reward_screen_completion_plus_safety_nenv10_500k/evaluations/proposed_ppo_s2.csv
- Reward changes: progress=45, success_bonus=80, crash_penalty=120, out_of_road_penalty=120.
- d0.00: success=0.80, cost=0.00, route=0.974, collision=0.00, out=0.00, shield=0.862
- d0.08: success=0.76, cost=0.12, route=0.948, collision=0.12, out=0.00, shield=0.850
- d0.15: success=0.50, cost=0.50, route=0.779, collision=0.50, out=0.00, shield=0.738
- Decision: fail as expansion candidate; does not beat formal proposed seed2 at d0.15 and sacrifices R1 medium-density gain.

## R2 safety_soften launched 2026-06-30
- Hypothesis: baseline cost/overspeed shaping may over-penalize motion and reduce completion pressure; lowering these terms may improve route completion/success. Risk is higher collision/cost.
- Reward changes: cost 20 -> 15; overspeed 2 -> 1.0; other weights unchanged.
- Protocol: proposed seed2, 500k, horizon=1200, n_envs=10, ent_coef=0.01, eval_n_envs=10.
- Output root: outputs/reward_screen_safety_soften_nenv10_500k
- Status: launched.

### R2 mid monitor 2026-06-30 ~317k
- Current training progress: ~317,440/500,000 timesteps.
- Signal: stage2 reached; window_success 0.133-0.333, window_cost around 0.10, speed around 12-13 km/h, no obvious early collision spike in sampled logs.
- Decision: continue to final evaluation.

## R2 safety_soften result 2026-06-30
- Output root: outputs/reward_screen_safety_soften_nenv10_500k
- CSV: outputs/reward_screen_safety_soften_nenv10_500k/evaluations/proposed_ppo_s2.csv
- Reward changes: cost=15, overspeed=1.0; other RewardWeights baseline.
- d0.00: success=0.78, cost=0.00, route=0.972, collision=0.00, out=0.00, shield=0.859
- d0.08: success=0.74, cost=0.06, route=0.936, collision=0.06, out=0.00, shield=0.844
- d0.15: success=0.44, cost=0.48, route=0.747, collision=0.46, out=0.02, shield=0.736
- Decision: fail as expansion candidate; no high-density gain over formal proposed seed2.

## Reward-screen interim conclusion 2026-06-30
- R1 completion_boost: best d0.08, but d0.15 worsens to success=0.32/cost=0.52.
- R3 completion_plus_safety: d0.15 success=0.50/cost=0.50, still not better than formal proposed seed2.
- R2 safety_soften: d0.15 success=0.44/cost=0.48, not better.
- Current conclusion: reward-only adjustments tested so far do not beat current formal proposed high-density result. Next priority is guard/TTC mechanism ablation before further reward expansion.

## R4 no_action_guard mechanism screen launched 2026-06-30
- Motivation: reward-only R1/R2/R3 did not beat formal proposed high-density result; inspect action-guard contribution before further reward tuning.
- Variant: no_action_guard; seed=2; 500k; n_envs=10; baseline RewardWeights.
- Output root: outputs/ablation_no_action_guard_nenv10_500k
- Status: launched.

### R4 no_action_guard mid monitor 2026-06-30 ~338k
- Current training progress: ~337,920/500,000 timesteps.
- Signal: stage2 reached; success_rate around 0.30-0.39, window_success up to 0.333, but window_cost 0.233-0.333 and out-of-road appears.
- Decision: continue to final evaluation; this is informative for guard/reward attribution.

## R4 no_action_guard result 2026-06-30
- Output root: outputs/ablation_no_action_guard_nenv10_500k
- CSV: outputs/ablation_no_action_guard_nenv10_500k/evaluations/no_action_guard_ppo_s2.csv
- Variant: no_action_guard; use_risk_reward=True; use_action_guard=False; baseline RewardWeights.
- d0.00: success=0.02, cost=0.98, route=0.297, collision=0.00, out=0.98, shield=0.000
- d0.08: success=0.00, cost=1.00, route=0.247, collision=0.38, out=0.62, shield=0.000
- d0.15: success=0.00, cost=1.00, route=0.181, collision=0.48, out=0.52, shield=0.000
- Decision: action guard is necessary; do not tune by removing guard. Proceed to TTC reward ablation.

## proposed_wo_ttc mechanism screen launched 2026-06-30
- Motivation: isolate TTC reward contribution while keeping action guard/curriculum active.
- Variant: proposed_wo_ttc; seed=2; 500k; n_envs=10; baseline RewardWeights except TTC component disabled by variant.
- Output root: outputs/ablation_proposed_wo_ttc_nenv10_500k
- Status: launched.

### proposed_wo_ttc mid monitor 2026-06-30 ~348k
- Current training progress: ~348,160/500,000 timesteps.
- Signal: success_rate around 0.35-0.38; window_success peaked at 0.633; stage around 1; out-of-road appears.
- Decision: continue to final evaluation to quantify TTC reward contribution.

## proposed_wo_ttc result 2026-06-30
- Output root: outputs/ablation_proposed_wo_ttc_nenv10_500k
- CSV: outputs/ablation_proposed_wo_ttc_nenv10_500k/evaluations/proposed_wo_ttc_ppo_s2.csv
- Variant: proposed_wo_ttc; reward_ttc=0.0; action guard enabled.
- d0.00: success=0.88, cost=0.00, route=0.982, collision=0.00, out=0.00, shield=0.855
- d0.08: success=0.68, cost=0.18, route=0.903, collision=0.16, out=0.02, shield=0.835
- d0.15: success=0.34, cost=0.60, route=0.727, collision=0.52, out=0.08, shield=0.747
- Decision: TTC reward is useful; keep it. Next reward screen should use moderate completion boost, not remove guard/TTC or make large penalty changes.

## R5 moderate_completion launched 2026-06-30
- Hypothesis: a gentler completion boost may preserve R1 medium-density gain without increasing high-density collision as much.
- Reward changes: progress 30 -> 40; success_bonus 40 -> 60; all other RewardWeights baseline.
- Protocol: proposed seed2, 500k, horizon=1200, n_envs=10, ent_coef=0.01, eval_n_envs=10.
- Output root: outputs/reward_screen_moderate_completion_nenv10_500k
- Status: launched.

### R5 mid monitor 2026-06-30 ~348k
- Current training progress: ~348,160/500,000 timesteps.
- Signal: stage2 reached; window_cost=0.0; window_success 0.467-0.667; rollout success_rate up to 0.54.
- Decision: continue to final evaluation. This is the most promising reward screen so far, but must survive final density eval.

## R5 moderate_completion result 2026-06-30
- Output root: outputs/reward_screen_moderate_completion_nenv10_500k
- CSV: outputs/reward_screen_moderate_completion_nenv10_500k/evaluations/proposed_ppo_s2.csv
- Reward changes: progress=40, success_bonus=60; all other RewardWeights baseline.
- d0.00: success=0.90, cost=0.00, route=0.983, collision=0.00, out=0.00, shield=0.856
- d0.08: success=0.74, cost=0.06, route=0.948, collision=0.06, out=0.00, shield=0.845
- d0.15: success=0.44, cost=0.50, route=0.751, collision=0.50, out=0.00, shield=0.734
- Decision: fail as expansion candidate; mid-run promise does not survive final evaluation. Baseline proposed remains better for high-density seed2.


## 2026-06-30 ttc14/v18 nenv16 tuning completed and rejected
- Time: 2026-06-30T16:29:52+08:00
- Protocol: scripts/run_one_defensive_proposed.py, n_envs=16, timesteps=1M, horizon=1500, ttc_threshold=14.0, target_speed=18.0, eval_n_envs=16, 50 episodes per density.
- Evidence: outputs/defensive_ttc14_v18_nenv16_tuning/evaluations/summary.csv and per-seed CSVs for seeds 26/27/28.
- seed26 d0.15: success=0.62 cost=0.20 collision=0.20 out=0.00 route=0.842.
- seed27 d0.15: success=0.44 cost=0.38 collision=0.32 out=0.06 route=0.777.
- seed28 d0.15: success=0.66 cost=0.20 collision=0.20 out=0.00 route=0.897.
- mean d0.00: success=0.973 cost=0.000 collision=0.000 out=0.000 route=0.990.
- mean d0.08: success=0.867 cost=0.093 collision=0.087 out=0.007 route=0.953.
- mean d0.15: success=0.573 cost=0.260 collision=0.240 out=0.020 route=0.839.
- Gate result: FAIL. The d0.15 three-seed mean success=0.573 is below the 0.60 minimum and mean cost=0.260 is above the 0.25 ceiling.
- Interpretation: raising TTC threshold to 14 helps seed26/28 relative to the weakest ttc12/v18 cases but worsens seed27 success and remains unstable; improvement over ttc12/v18 mean is too small for a paper-facing final claim.
- Decision: keep ttc14/v18 as diagnostic parameter-sensitivity evidence only. Do not freeze it as Branch A. Move to Branch B standard comparison with n_envs=16 and start from the full proposed method, while retaining defensive results for appendix/tuning discussion.

## 2026-06-30 Branch B proposed seed0 nenv16 completed and failed main gate
- Time: 2026-06-30T17:03:41+08:00
- Run: outputs/iscsic_main_nenv16_v2/runs/proposed_ppo_s0.
- Protocol: proposed full method, seed0, train/eval n_envs=16, timesteps=1.5M, horizon=1200, ent_coef=0.01, eval 50 episodes per density.
- Evaluation CSV: outputs/iscsic_main_nenv16_v2/evaluations/proposed_ppo_s0.csv; summary: outputs/iscsic_main_nenv16_v2/evaluations/summary.csv.
- d0.00: success=0.90 cost=0.00 collision=0.00 out=0.00 route=0.984 shield=0.862.
- d0.08: success=0.76 cost=0.12 collision=0.12 out=0.00 route=0.929 shield=0.842.
- d0.15: success=0.48 cost=0.42 collision=0.40 out=0.02 route=0.791 shield=0.749.
- Gate result: FAIL for paper main line. High-density cost/collision is too high and success is below target; do not expand this exact protocol to seed1/seed2 as the main proposed method.
- Decision: launch targeted safety tuning using stronger TTC/collision penalties and lower target speed, based on defensive branch evidence and prior reward screens showing completion-only tuning worsens high-density collision.

## 2026-06-30 launch proposed safety-tuned seed0 nenv16 screen
- Time: 2026-06-30T17:03:41+08:00
- Output root: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m 1000000 1200 --ent-coef 0.01 --reward-ttc 6 --reward-cost 40 --reward-overspeed 3 --reward-target-speed 18 --reward-progress 40 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 120 --reward-ttc-threshold 12 --stage2-success 0.40 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: stronger TTC/cost/crash penalties and lower target speed should reduce d0.15 collision/cost relative to standard proposed seed0, while preserving enough route completion for a safety-success tradeoff.
- Promotion rule: only expand if d0.15 cost is materially below 0.42 and preferably <=0.25 without collapsing d0.08 success.

## 2026-06-30 safety-tuned proposed seed0 nenv16 early health check
- Time: 2026-06-30T17:04:21+08:00
- Run: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/runs/proposed_ppo_s0.
- Config verified: n_envs=16, timesteps=1M, horizon=1200, ent_coef=0.01, reward_ttc=6, reward_cost=40, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.40, stage2_cost=0.25, demote_cost=0.35.
- Early log: about 32k timesteps, stage0, no cost/collision yet; low route completion is expected during warmup.
- Resource check: GPU free about 10.8GB, CPU available about 24GB, disk free about 41GB. Continue to 250k/500k quality checks.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~311k
- Time: 2026-06-30T17:06:20+08:00
- Health: process alive; checkpoint_250000_steps.zip exists; GPU free about 10.9GB.
- Training signal: reached stage1 by about 278k-311k. Success window remains low at about 0.067; route window dropped from about 0.600 to 0.436, while sampled route can reach about 0.604.
- Risk signal: window_cost ranges about 0.067-0.200. Safety pressure is working, but the run may be too conservative/slow early.
- Decision: continue to 500k before changing parameters. Watch whether route/success recover under the lower target speed and stronger TTC/cost penalties.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~508k
- Time: 2026-06-30T17:08:24+08:00
- Health: process alive; checkpoints at 250k and 500k exist; GPU free about 10.9GB.
- Training signal: still stage1 around 508k. Route window improved to about 0.685, success window about 0.133; sampled route can reach about 0.829 but an out-of-road cost sample appeared.
- Risk/benefit: stronger safety tuning is slowing curriculum progress but may reduce high-density collision relative to standard proposed. It is not idle collapse.
- Decision: continue to 750k/final evaluation. If final d0.15 cost improves but success collapses, next diagnostic should relax completion/speed slightly rather than revert to standard reward.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~704k
- Time: 2026-06-30T17:11:14+08:00
- Health: process alive; checkpoints at 250k and 500k exist; GPU free about 10.9GB.
- Training signal: recovered from slow early stage1 and reached stage3 by about 688k. Window_route_completion peaked around 0.862 and window_success about 0.467; current sampled route remains moderate to high.
- Risk signal: window_cost is 0.0 in the recent stage2/stage3 blocks, a clear improvement over the standard proposed run's high-cost training windows.
- Decision: continue to final evaluation. This screen remains promising for reducing d0.15 cost; final success tradeoff will decide promotion.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~918k
- Time: 2026-06-30T17:14:47+08:00
- Health: process alive; checkpoints at 250k/500k/750k exist.
- Training signal: after reaching stage3 earlier, latest log near 918k is stage2 with route window about 0.749 and success window about 0.067.
- Risk signal: recent window_cost is low, about 0.033-0.067, much lower than standard proposed, but success appears under pressure.
- Decision: finish and evaluate. If final d0.15 cost drops strongly but success is too low, next tuning should relax success/completion pressure or reduce safety strength slightly.

## 2026-06-30 safety-tuned proposed seed0 training completed, evaluation running
- Time: 2026-06-30T17:17:50+08:00
- Training status: completed 1M scheduled timesteps and saved outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/runs/proposed_ppo_s0/model/final_model.zip plus checkpoint_1000000_steps.zip.
- Final training signal: stage2 near 1.016M, window_route_completion about 0.743, window_success about 0.167, window_cost about 0.133.
- Interpretation before eval: much lower apparent cost than standard proposed, but success/stage progression is weaker. Held-out eval will decide whether this is a useful safety-success tradeoff.
- Evaluation status: evaluate_from_config.py is running with eval_n_envs=16, densities 0.00/0.08/0.15, 50 episodes per density.

## 2026-06-30 safety-tuned proposed seed0 nenv16 screen completed and rejected
- Time: 2026-06-30T17:21:05+08:00
- Run: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/runs/proposed_ppo_s0.
- Protocol: proposed seed0, train/eval n_envs=16, timesteps=1M, horizon=1200, ent_coef=0.01, reward_ttc=6, cost=40, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.40, stage2_cost=0.25, demote_cost=0.35.
- Evaluation CSV: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/evaluations/proposed_ppo_s0.csv.
- d0.00: success=0.70 cost=0.00 collision=0.00 out=0.00 route=0.969 shield=0.860.
- d0.08: success=0.64 cost=0.12 collision=0.10 out=0.02 route=0.935 shield=0.839.
- d0.15: success=0.28 cost=0.40 collision=0.34 out=0.06 route=0.704 shield=0.699.
- Gate result: FAIL. Compared with standard proposed seed0 d0.15 success=0.48/cost=0.42, cost only improves slightly while success collapses. Do not expand this configuration.
- Decision: launch defensive-like horizon1500 cost50 diagnostic, because prior defensive branch suggests horizon1500 + stricter progression gives better high-density tradeoff than horizon1200 safety penalty alone.

## 2026-06-30 launch defensive-like proposed h1500 cost50 seed0 nenv16 screen
- Time: 2026-06-30T17:21:05+08:00
- Output root: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m 1000000 1500 --ent-coef 0.01 --reward-ttc 6 --reward-cost 50 --reward-overspeed 3 --reward-target-speed 18 --reward-progress 40 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 120 --reward-ttc-threshold 12 --stage2-success 0.50 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: horizon=1500 and stricter stage2 gate should preserve route/success better than the failed horizon1200 safety screen, while cost=50 attempts to push d0.15 cost below the defensive ttc12/v18 mean.
- Promotion rule: must beat standard proposed seed0 on d0.15 cost by a clear margin and avoid the safety-tuned screen's success collapse.

## 2026-06-30 defensive-like h1500 cost50 seed0 early health check
- Time: 2026-06-30T17:21:39+08:00
- Run: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Config verified: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Early log: about 32k timesteps, stage0, no cost/collision, low route completion as expected.
- Resource check: GPU free about 10.8GB, CPU available about 24GB, disk free about 41GB. Continue to 250k/500k checks.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~295k
- Time: 2026-06-30T17:23:35+08:00
- Health: process alive; checkpoint_250000_steps.zip exists; GPU free about 10.8GB.
- Training signal: reached stage1 by ~278k. Recent window_success rose to about 0.233, with route window around 0.528-0.607.
- Risk signal: window_cost is 0.0-0.10 in early stage1, better than the failed horizon1200 safety screen at comparable progress.
- Decision: continue to 500k/750k. This diagnostic is still viable because horizon1500 appears to preserve early success better while keeping cost low.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~508k
- Time: 2026-06-30T17:26:11+08:00
- Health: process alive; checkpoints at 250k and 500k exist.
- Training signal: around 508k still stage1, but route window is strong at about 0.813 and success window about 0.267. This is better route/success behavior than the failed horizon1200 safety screen.
- Risk signal: window_cost rose to about 0.233, near the intended stage2 cost ceiling. It is not yet clean enough to freeze.
- Decision: continue to 750k/final. Need final d0.15 cost to decide whether cost50 helps or just trades instability for route.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~688k
- Time: 2026-06-30T17:28:58+08:00
- Health: process alive; checkpoints at 250k and 500k exist.
- Training signal: reached stage2 by about 672k. Window_route_completion about 0.854, window_success about 0.30, and success samples appear.
- Risk signal: cost spiked around 622k-639k up to window_cost about 0.30, then improved to about 0.10 by 672k-688k.
- Decision: continue to 750k/final. This is now the most promising tuning screen so far because it preserves route/success better than the horizon1200 safety screen while recovering cost.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~918k
- Time: 2026-06-30T17:32:16+08:00
- Health: process alive; checkpoints at 250k/500k/750k exist.
- Training signal: around 900k-918k the run is stage2 and success_rate increases, but route samples are mixed.
- Risk signal: window_cost worsened to about 0.333-0.467, mainly out-of-road samples, despite cost50. This is a serious warning sign.
- Decision: continue to final held-out eval for evidence, but do not treat this diagnostic as promotable unless the CSV unexpectedly shows much lower d0.15 cost.

## 2026-06-30 defensive-like h1500 cost50 seed0 training completed, evaluation running
- Time: 2026-06-30T17:35:19+08:00
- Training status: completed 1M scheduled timesteps and saved outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/runs/proposed_ppo_s0/model/final_model.zip plus checkpoint_1000000_steps.zip.
- Final training signal: stage2 near 1.016M, window_route_completion about 0.776, window_success about 0.467, window_cost about 0.20.
- Interpretation before eval: better success/route than the horizon1200 safety screen, but out-of-road/cost instability remains. Held-out eval decides promotion or rejection.
- Evaluation status: evaluate_from_config.py is running with eval_n_envs=16, densities 0.00/0.08/0.15, 50 episodes per density.

## 2026-06-30 defensive-like h1500 cost50 seed0 screen completed: improved but failed
- Time: 2026-06-30T17:38:31+08:00
- Run: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Protocol: proposed seed0, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, cost=50, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25.
- Evaluation CSV: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/evaluations/proposed_ppo_s0.csv.
- d0.00: success=0.96 cost=0.00 collision=0.00 out=0.00 route=0.986 shield=0.867.
- d0.08: success=0.84 cost=0.12 collision=0.10 out=0.02 route=0.936 shield=0.846.
- d0.15: success=0.54 cost=0.34 collision=0.24 out=0.10 route=0.815 shield=0.716.
- Gate result: FAIL but improved. Compared with standard proposed seed0, d0.15 improved from success=0.48/cost=0.42 to success=0.54/cost=0.34, but cost remains too high and out_of_road=0.10 is a new bottleneck.
- Decision: next tuning should target lane/out-of-road control, not just global cost. Launch h1500 lane/out diagnostic with lower target speed and stronger lane/out penalties.

## 2026-06-30 launch defensive-like h1500 lane/out seed0 nenv16 screen
- Time: 2026-06-30T17:38:31+08:00
- Output root: outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m 1000000 1500 --ent-coef 0.01 --reward-ttc 6 --reward-cost 50 --reward-overspeed 3 --reward-target-speed 16 --reward-progress 40 --reward-lane 2.0 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 150 --reward-ttc-threshold 12 --stage2-success 0.50 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: h1500/cost50 improved success but left high out_of_road and lane deviation; stronger lane/out penalty plus target_speed=16 should reduce d0.15 cost without repeating the horizon1200 success collapse.
- Promotion rule: must reduce d0.15 cost below 0.34 and preferably <=0.25 while keeping success near or above 0.50.

## 2026-06-30 defensive-like h1500 lane/out seed0 early health check
- Time: 2026-06-30T17:39:05+08:00
- Run: outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Config verified: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, reward_lane=2.0, target_speed=16, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25.
- Early log: about 32k timesteps, stage0, no cost/collision; shaped reward is much lower because lane penalty is stronger.
- Resource check: GPU free about 10.8GB, CPU available about 24GB, disk free about 41GB. Continue to 250k; watch for over-conservative/low-motion collapse.

## 2026-06-30 defensive-like h1500 lane2/v16 seed0 early rejected
- Time: 2026-06-30T17:41:32+08:00
- Run: outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Status at about 311k: still stage0, window_route_completion about 0.077-0.082, window_success=0, window_cost=0, mean_speed about 0.5-0.6 km/h.
- Interpretation: reward_lane=2.0 plus target_speed=16 and strong out penalty makes the policy too conservative/low-motion. This is early idle/slow-motion collapse, not a useful paper candidate.
- Decision: terminate this run early and do not evaluate it. Launch a milder lane/out diagnostic: lane=1.0, target_speed=18, out penalty=150, keeping horizon1500 and cost50.

## 2026-06-30 launch defensive-like h1500 lane1/out150 seed0 nenv16 screen
- Time: 2026-06-30T17:41:32+08:00
- Output root: outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m 1000000 1500 --ent-coef 0.01 --reward-ttc 6 --reward-cost 50 --reward-overspeed 3 --reward-target-speed 18 --reward-progress 40 --reward-lane 1.0 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 150 --reward-ttc-threshold 12 --stage2-success 0.50 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: a moderate lane penalty and stronger out penalty may reduce out_of_road without the lane2/v16 low-motion collapse.

## 2026-06-30 defensive-like h1500 lane1/out150 seed0 screen completed: promoted to candidate
- Time: 2026-06-30T17:57:38+08:00
- Run: outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Protocol: proposed seed0, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, reward_lane=1.0, target_speed=18, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Evaluation CSV: outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m/evaluations/proposed_ppo_s0.csv; summary.csv exists.
- d0.00: success=0.96 cost=0.00 collision=0.00 out=0.00 route=0.988 shield=0.868.
- d0.08: success=0.88 cost=0.10 collision=0.10 out=0.00 route=0.965 shield=0.850.
- d0.15: success=0.70 cost=0.24 collision=0.22 out=0.02 route=0.872 shield=0.712.
- Comparison: vs standard proposed seed0 d0.15 improved from success=0.48/cost=0.42/route=0.791 to success=0.70/cost=0.24/route=0.872. Vs h1500 cost50 seed0 improved from success=0.54/cost=0.34/out=0.10 to success=0.70/cost=0.24/out=0.02.
- Interpretation: moderate lane penalty plus stronger out-of-road penalty fixes the lane2/v16 low-motion failure and materially reduces high-density cost while preserving route completion. The remaining d0.15 failures are mostly collision (0.22), not out-of-road.
- Gate result: PROMOTE TO CANDIDATE, not final. Expand seeds 1 and 2 with the same n_envs=16 protocol before freezing paper-facing results. If seed1/2 mean d0.15 remains success>=0.60 and cost<=0.28, use this as the main proposed setting and start ablations/comparisons against it.

## 2026-06-30 launch candidate lane1/out150 seed1-2 nenv16 replication
- Time: 2026-06-30T17:58:25+08:00
- Roots: outputs/candidate_lane1_out150_cost50_nenv16_seed1_1m and outputs/candidate_lane1_out150_cost50_nenv16_seed2_1m.
- Protocol: proposed seeds 1 and 2, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, reward_lane=1.0, target_speed=18, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Reason: seed0 promoted to candidate with d0.15 success=0.70/cost=0.24/out=0.02, but paper-facing main proposed setting requires multi-seed replication.
- Run policy: use independent roots for seed1/seed2 to avoid parallel root-level figure/report write conflicts; aggregate after both finish.

## 2026-06-30 candidate lane1/out150 seed1-2 monitor at ~600k
- Time: 2026-06-30T18:04:12+08:00
- Roots: outputs/candidate_lane1_out150_cost50_nenv16_seed1_1m and outputs/candidate_lane1_out150_cost50_nenv16_seed2_1m.
- Resource status: parallel n_envs=16 + n_envs=16 remains safe; GPU free about 10.5GB, CPU memory available about 21GB.
- Seed1 status: checkpoint_500000_steps.zip exists; by ~590k reached stage2, window_success about 0.667 at one check, rollout success_rate about 0.40, cost near 0.00-0.03.
- Seed2 status: checkpoint_500000_steps.zip exists; by ~590k reached stage2 once, then stage1/2 fluctuation; rollout success_rate about 0.28-0.32, cost about 0.10.
- Interpretation: both seeds had a slow stage0 start but recovered, so this is not the lane2/v16 idle collapse. Continue to 750k/final held-out evaluation.

## 2026-06-30 candidate lane1/out150 seed0-2 aggregate completed
- Time: 2026-06-30T18:17:01+08:00
- Aggregate root: outputs/candidate_lane1_out150_cost50_nenv16_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, DECISION.md.
- Sources: seed0 from outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m/evaluations/summary.csv; seed1/2 from outputs/candidate_lane1_out150_cost50_nenv16_seed1_1m and seed2_1m.
- d0.00 mean: success=0.973, cost=0.000, route=0.989.
- d0.08 mean: success=0.833, cost=0.133, collision=0.127, out=0.007, route=0.929.
- d0.15 mean: success=0.620, cost=0.247, collision=0.233, out=0.013, route=0.865.
- Variance warning: d0.15 success std=0.122 and seed2 is weak (success=0.48, cost=0.32). This is acceptable as current best only because the three-seed mean passes the promotion gate, not because every seed is clean.
- Decision: keep lane1/out150/cost50 as current main-method candidate and start ablations/comparisons around it. Remaining bottleneck is high-density collision, not out-of-road.

## 2026-06-30 tuned-protocol proposed_wo_ttc seed0 nenv16 completed
- Time: 2026-06-30T18:38:32.
- Root: outputs/tuned_ablation_wo_ttc_nenv16_seed0_1m.
- Protocol: proposed_wo_ttc seed0, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, target_speed=18, progress=40, cost=50, lane=1.0, success_bonus=55, crash=120, out=150, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Config check: reward_ttc=0.0 by variant; action guard and curriculum stay enabled. This is the intended TTC reward ablation, not a mistaken low-TTC full method.
- CSV: outputs/tuned_ablation_wo_ttc_nenv16_seed0_1m/evaluations/summary.csv.
- d0.00: success=1.00 cost=0.00 collision=0.00 out=0.00 route=0.992.
- d0.08: success=0.92 cost=0.04 collision=0.04 out=0.00 route=0.975.
- d0.15: success=0.44 cost=0.54 collision=0.54 out=0.00 route=0.743.
- Comparison to full tuned proposed seed0: full d0.15 success=0.70 cost=0.24 collision=0.22 out=0.02 route=0.872; removing TTC drops success by 0.26 and increases collision/cost by about 0.30.
- Interpretation: TTC reward is important specifically for dense-traffic collision suppression. The ablation can look strong at easy/medium density, but it fails the paper-relevant high-density safety-success tradeoff.
- Decision: keep TTC in the main method. Do not expand proposed_wo_ttc to more seeds until baseline/risk/curriculum/no_action_guard seed0 comparisons are available, unless the paper explicitly needs a three-seed TTC ablation table.

## 2026-06-30 batch C completed: curriculum and guard_only seed0 nenv16
- Time: 2026-06-30T19:26:49.
- curriculum root: outputs/tuned_compare_curriculum_nenv16_seed0_1m; summary CSV exists.
- curriculum config: use_risk_reward=False, use_action_guard=False, curriculum=True.
- curriculum d0.00: success=0.02 cost=0.98 collision=0.00 out=0.98 route=0.350.
- curriculum d0.08: success=0.00 cost=1.00 collision=0.32 out=0.68 route=0.256.
- curriculum d0.15: success=0.00 cost=1.00 collision=0.56 out=0.44 route=0.176.
- Interpretation: curriculum alone induces movement during training, but final evaluation fails by high-speed out-of-road/collision. Curriculum is not sufficient without the guard/safety mechanism.
- guard_only root: outputs/tuned_ablation_guard_only_nenv16_seed0_1m; summary CSV exists.
- guard_only config: use_risk_reward=False, use_action_guard=True, curriculum=True.
- guard_only d0.00: success=1.00 cost=0.00 route=0.992 shield_intervention_rate=0.872.
- guard_only d0.08: success=0.86 cost=0.08 collision=0.08 out=0.00 route=0.954 shield_intervention_rate=0.852.
- guard_only d0.15: success=0.62 cost=0.22 collision=0.20 out=0.02 route=0.861 shield_intervention_rate=0.728.
- Comparison to full tuned proposed seed0: full d0.15 success=0.70 cost=0.24 route=0.872. Guard_only is close: slightly lower success (-0.08), slightly lower cost (-0.02), similar route.
- Paper-risk interpretation: the guard+curriculum component explains a large part of the current seed0 gain. The risk reward contribution is positive on seed0 for high-density success, but not yet proven robust enough as a standalone claim.
- Decision: promote guard_only to critical comparison. Run guard_only seeds 1 and 2 before claiming the full method beats simpler guard+curriculum. If guard_only mean matches/exceeds full proposed, either retune the full risk reward or shift the paper claim toward guard/curriculum as the main mechanism.

## 2026-06-30 guard_only seed0-2 aggregate completed
- Time: 2026-06-30T19:53:00.
- Aggregate root: outputs/tuned_ablation_guard_only_nenv16_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, DECISION.md.
- Guard_only d0.00 mean: success=0.973 cost=0.000 route=0.990.
- Guard_only d0.08 mean: success=0.873 cost=0.093 collision=0.093 out=0.000 route=0.940.
- Guard_only d0.15 mean: success=0.633 cost=0.207 collision=0.200 out=0.007 route=0.868.
- Comparison to full proposed aggregate: at d0.15 guard_only is +0.013 success, -0.040 cost, +0.003 route, -0.033 collision, -0.007 out_of_road relative to current full proposed.
- Interpretation: the current full risk-reward setting does not beat guard+curriculum. The paper claim must not state that the risk reward is the dominant improvement under the current evidence.
- Decision: launch a light-risk full proposed retuning screen. Goal: retain the stability of guard_only while recovering any high-density success gain from a milder TTC/cost reward. If light-risk does not beat guard_only, reframe the main method around guard+curriculum and treat risk reward as optional/diagnostic.

## 2026-06-30 launch light-risk full proposed seed0 and seed2
- Time: 2026-06-30T19:53:49.
- Reason: guard_only seed0-2 aggregate matches/exceeds the current full proposed aggregate, so the full risk reward setting must be retuned before paper claims are frozen.
- Roots: outputs/tuning_proposed_light_risk_ttc3_cost25_lane03_nenv16_seed0_1m and outputs/tuning_proposed_light_risk_ttc3_cost25_lane03_nenv16_seed2_1m.
- Protocol: proposed seeds 0 and 2, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01.
- Light-risk weights: ttc=3, cost=25, lane=0.3, crash=80, out=150, overspeed=3, target_speed=18, progress=40, success_bonus=55, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Purpose: keep guard+curriculum stability while adding milder risk shaping. Seed0 checks that the strong seed is not harmed; seed2 targets the weak seed in the current full proposed aggregate.
- Promotion rule: light-risk must beat guard_only aggregate at d0.15 or at least improve full proposed seed2 materially without hurting seed0. Otherwise the paper main line should pivot toward guard+curriculum.

## 2026-06-30 light-risk seed0/2 early config and health check
- Time: 2026-06-30T19:55:48.
- Config verified for both seeds: variant=proposed, use_risk_reward=True, use_action_guard=True, curriculum=True, n_envs=16, horizon=1500, timesteps=1M.
- Light-risk weights verified: ttc=3, cost=25, lane=0.3, crash=80, out=150, target_speed=18, progress=40, success_bonus=55.
- seed0 around 246k: stage1, window_cost about 0.03, route window about 0.60, rollout success_rate about 0.10. It is slower than guard_only but not collapsed.
- seed2 around 246k: still stage0, window_success=0, route window about 0.44, cost fluctuating but not catastrophic. This is weaker than desired and must be watched closely.
- Decision: continue to 500k before judging. If seed2 remains stage0/zero-success at 500k, light-risk is likely not solving the weak-seed issue.

## 2026-06-30 light-risk full proposed seed0/2 completed and rejected as main setting
- Time: 2026-06-30T20:15:44+08:00.
- Aggregate root: outputs/tuning_proposed_light_risk_ttc3_cost25_lane03_nenv16_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- Final seed0: d0.00 success=0.98 cost=0.00 route=0.991; d0.08 success=0.90 cost=0.06 collision=0.06 route=0.956; d0.15 success=0.64 cost=0.28 collision=0.26 out=0.02 route=0.859.
- Final seed2: d0.00 success=0.96 cost=0.00 route=0.990; d0.08 success=0.86 cost=0.12 collision=0.12 route=0.930; d0.15 success=0.52 cost=0.30 collision=0.30 out=0.00 route=0.821.
- Light-risk mean over seeds 0 and 2: d0.00 success=0.970 cost=0.000 route=0.990; d0.08 success=0.880 cost=0.090 route=0.943; d0.15 success=0.580 cost=0.290 collision=0.280 out=0.010 route=0.840.
- Comparison to guard_only 3-seed aggregate: at d0.08 light-risk is roughly comparable/slightly higher success, but at d0.15 it is worse (success 0.580 vs 0.633, cost 0.290 vs 0.207, collision 0.280 vs 0.200, route 0.840 vs 0.868).
- Comparison to current full proposed 3-seed aggregate: light-risk improves d0.08 but worsens d0.15 (success 0.580 vs 0.620, cost 0.290 vs 0.247, route 0.840 vs 0.865).
- Interpretation: milder TTC/cost/lane risk shaping did not solve the high-density weak-seed issue. The current evidence still says guard+curriculum is the robust mechanism; risk reward is not ready to be claimed as the dominant gain.
- Decision: do not promote this light-risk full setting. Run missing reward-component ablations next (`proposed_wo_lane`, `proposed_wo_smooth`) under the tuned full-proposed protocol, with CLI overrides chosen so the intended zeroed reward terms are not accidentally restored.

## 2026-06-30 launch reward-component ablations wo_lane and wo_smooth seed0
- Time: 2026-06-30T20:17:25+08:00.
- Roots: outputs/tuned_ablation_wo_lane_nenv16_seed0_1m and outputs/tuned_ablation_wo_smooth_nenv16_seed0_1m.
- Protocol: n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Shared tuned full-proposed weights: ttc=6, cost=50, overspeed=3, target_speed=18, progress=40, success_bonus=55, crash=120, out_of_road=150, ttc_threshold=12.
- proposed_wo_lane config verified: variant=proposed_wo_lane, use_risk_reward=True, use_action_guard=True, curriculum=True, lane=0.0, smooth=0.02, accel=0.01.
- proposed_wo_smooth config verified: variant=proposed_wo_smooth, use_risk_reward=True, use_action_guard=True, curriculum=True, lane=1.0, smooth=0.0, accel=0.0.
- Early health at about 82k: both runs alive on GPU, still stage0 with success=0 and low route completion. This is treated as normal cold start; next checkpoint is around 250k before intervention.
- Purpose: complete reward-component ablations without accidentally restoring the ablated CLI weights. These results will support whether lane keeping and smoothness terms are material or mostly cosmetic relative to TTC/cost/guard/curriculum.

## 2026-06-30 reward-component ablations monitor at ~350k
- Time: 2026-06-30T20:19:59+08:00.
- proposed_wo_lane: around 344k, stage1, window_success about 0.30, rollout success_rate about 0.35, route window about 0.62, window_cost about 0.17. It is learning despite lane=0, but lane_deviation is visibly high in samples (about 0.4-1.0), so final eval should reveal whether lane reward mainly improves tracking/stability rather than raw success.
- proposed_wo_smooth: around 393k, still stage0, window_success=0, route window about 0.23, speed about 1.5 km/h, no cost yet. This looks like a real ablation degradation from removing smooth/accel regularization, not a launch/config failure.
- Decision: do not tune or rescue these ablations mid-run, because the purpose is to measure component removal under the same tuned full-proposed protocol. Continue to final held-out summary.csv and then decide whether to replicate with more seeds.

## 2026-06-30 reward-component ablation seed0 completed
- Time: 2026-06-30T20:35:35+08:00.
- Aggregate root: outputs/tuned_reward_component_ablation_seed0_aggregate.
- Files: seed0_component_ablation_summary.csv, deltas_vs_full_seed0.csv, DECISION.md.
- full_proposed seed0 d0.15: success=0.70, cost=0.24, collision=0.22, route=0.872.
- wo_ttc seed0 d0.15: success=0.44, cost=0.54, collision=0.54, route=0.743.
- wo_lane seed0 d0.15: success=0.60, cost=0.28, collision=0.28, route=0.862, lane_deviation=0.348.
- wo_smooth seed0 d0.15: success=0.58, cost=0.24, collision=0.24, route=0.849.
- Interpretation: TTC removal is the strongest reward-term degradation; lane removal mainly harms lateral tracking and high-density safety/success; smooth/accel removal weakens high-density success and training conversion but is less catastrophic than expected from mid-run.
- Decision: replicate at least wo_ttc beyond seed0 and add shield_only seed0 next. Do not overclaim reward terms from a single-seed table.

## 2026-06-30 launch wo_ttc seed1 and shield_only seed0
- Time: 2026-06-30T20:37:50+08:00.
- Roots: outputs/tuned_ablation_wo_ttc_nenv16_seed1_1m and outputs/tuned_compare_shield_only_nenv16_seed0_1m.
- proposed_wo_ttc seed1 config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, n_envs=16, horizon=1500, timesteps=1M, ttc=0.0, lane=1.0, cost=50, crash=120, out=150.
- shield_only seed0 config verified: use_risk_reward=False, use_action_guard=True, curriculum=False, n_envs=16, horizon=1500, timesteps=1M.
- Early health: both alive on GPU. proposed_wo_ttc is still stage0/cold-start around 115k. shield_only has no curriculum and already shows the expected low-speed/low-route pattern: route about 0.06-0.07, success=0, one out-of-road sample.
- Purpose: replicate the strongest reward-term negative effect beyond seed0 and isolate whether the action guard alone can work without curriculum.
- Decision: continue both to final evaluation; do not tune shield_only because its role is a mechanism control, not a candidate method.

## 2026-06-30 wo_ttc seed1 and shield_only seed0 completed
- Time: 2026-06-30T21:00:21+08:00.
- wo_ttc aggregate root: outputs/tuned_ablation_wo_ttc_nenv16_seed0_seed1_aggregate.
- proposed_wo_ttc seed1 d0.15: success=0.66, cost=0.20, collision=0.20, route=0.905. This contradicts the seed0-only interpretation that TTC removal always collapses high-density performance.
- proposed_wo_ttc seed0-1 mean d0.15: success=0.550, cost=0.370, collision=0.370, route=0.824.
- shield_only seed0: d0.00 success=1.00 cost=0.00 route=0.992; d0.08 success=0.96 cost=0.04 collision=0.02 out=0.02 route=0.975; d0.15 success=0.56 cost=0.32 collision=0.32 out=0.00 route=0.833.
- Interpretation: action guard alone is a major mechanism and is very strong up to medium density, but high-density safety/success still lags guard_only/full. TTC reward contribution is high-variance across seeds and must not be overclaimed from seed0.
- Decision: launch proposed_wo_ttc seed2 and shield_only seed1 next. This resolves TTC variance and checks shield_only stability.

## 2026-06-30 launch wo_ttc seed2 and shield_only seed1
- Time: 2026-06-30T21:02:21+08:00.
- Roots: outputs/tuned_ablation_wo_ttc_nenv16_seed2_1m and outputs/tuned_compare_shield_only_nenv16_seed1_1m.
- proposed_wo_ttc seed2 config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, n_envs=16, horizon=1500, timesteps=1M, ttc=0.0, lane=1.0, cost=50, crash=120, out=150.
- shield_only seed1 config verified: use_risk_reward=False, use_action_guard=True, curriculum=False, n_envs=16, horizon=1500, timesteps=1M.
- Early health: both runs alive on GPU. proposed_wo_ttc seed2 is cold-start stage0 around 131k. shield_only seed1 is still early and shows lower stability than seed0 with out-of-road samples; this is not yet a final judgement.
- Purpose: resolve the high variance between wo_ttc seed0 and seed1, and test whether shield_only seed0's strong medium-density result is seed-stable.


## 2026-06-30 wo_ttc seed2 completed and three-seed aggregate written
- Time: 2026-06-30T21:20:19+08:00.
- New aggregate root: outputs/tuned_ablation_wo_ttc_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- proposed_wo_ttc seed2 final: d0.00 success=0.96 cost=0.00 route=0.990; d0.08 success=0.96 cost=0.04 collision=0.04 route=0.959; d0.15 success=0.52 cost=0.34 collision=0.34 route=0.821.
- Three-seed wo_ttc mean: d0.00 success=0.987 cost=0.000 route=0.991; d0.08 success=0.900 cost=0.067 collision=0.067 route=0.950; d0.15 success=0.540 cost=0.360 collision=0.360 route=0.823.
- Comparison to full proposed aggregate at d0.15: success 0.540 vs 0.620, cost 0.360 vs 0.247, route 0.823 vs 0.865. Removing TTC is worse on average in dense traffic.
- Comparison to guard_only aggregate at d0.15: success 0.540 vs 0.633, cost 0.360 vs 0.207, route 0.823 vs 0.868. The TTC-ablated full method is also weaker than guard+curriculum in dense traffic.
- Interpretation: TTC reward contribution is high-variance but negative when removed at d0.15. Claim boundary: TTC reward helps dense-traffic robustness on average; do not claim it is universally necessary or that risk reward dominates guard+curriculum.
- Active run still in progress: outputs/tuned_compare_shield_only_nenv16_seed1_1m. Current decision is to wait for shield_only seed1 before starting shield_only seed2 or additional reward ablation seeds.

## 2026-06-30 shield_only seed1 completed and seed0-1 interim aggregate written
- Time: 2026-06-30T21:25:29+08:00.
- New aggregate root: outputs/tuned_compare_shield_only_nenv16_seed0_seed1_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- shield_only seed1 final: d0.00 success=0.98 cost=0.00 route=0.991; d0.08 success=0.92 cost=0.08 collision=0.06 out=0.02 route=0.944; d0.15 success=0.56 cost=0.22 collision=0.22 route=0.867.
- shield_only seed0-1 mean: d0.00 success=0.990 cost=0.000 route=0.991; d0.08 success=0.940 cost=0.060 collision=0.040 out=0.020 route=0.960; d0.15 success=0.560 cost=0.270 collision=0.270 route=0.850.
- Interpretation: action guard alone is seed-stable enough to require a seed2 follow-up. It is very strong at easy/medium densities and still meaningful at high density, though high-density success remains below full proposed/guard_only means.
- Decision: launch shield_only seed2 next. Also begin proposed_wo_lane seed1 while the GPU is free, because lane reward ablation currently has only seed0 evidence.

## 2026-06-30 launch/config check shield_only seed2 and wo_lane seed1
- Time: 2026-06-30T21:27:13+08:00.
- Active roots: outputs/tuned_compare_shield_only_nenv16_seed2_1m and outputs/tuned_ablation_wo_lane_nenv16_seed1_1m.
- Launch protocol: n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- shield_only seed2 config verified: variant=shield_only, seed=2, use_risk_reward=False, use_action_guard=True, curriculum=False. This completes the planned third seed for the action-guard-only mechanism control.
- proposed_wo_lane seed1 config verified: variant=proposed_wo_lane, seed=1, use_risk_reward=True, use_action_guard=True, curriculum=True, reward_weights.lane=0.0, ttc=6.0, smooth=0.02, accel=0.01, cost=50.0, crash=120.0, out=150.0.
- Early health: both processes alive. shield_only seed2 is in normal cold-start low-speed/low-route behavior. wo_lane seed1 shows high lane deviation/out-of-road risk early, which is expected for lane reward removal and should not be rescued mid-run unless it becomes a launch/config failure.
- Next checkpoint: inspect around 250k-350k timesteps for stage transition, cost window, and route/success trend; do not retune these controls before final evaluation unless the run crashes or config is wrong.

## 2026-06-30 mid-run health shield_only seed2 and wo_lane seed1
- Time: 2026-06-30T21:31:54+08:00.
- shield_only seed2 around 344k: no config/process issue; success_rate about 0.30, route samples up to about 0.99, some out-of-road/cost remains. This matches the seed0/1 recovery pattern and should continue to final evaluation.
- proposed_wo_lane seed1 around 623k: reached curriculum stage2, window_success about 0.30, window_cost about 0.067, window_route about 0.82. Lane deviation remains high in samples (roughly 0.38-0.50 recently, max up to 2.0), which is expected evidence for lane reward removal rather than a launch failure.
- Decision: continue both runs unchanged. No reward rescue or retune before final summaries because both are mechanism/ablation controls.

## 2026-06-30 wo_lane seed1 completed and seed0-1 aggregate written
- Time: 2026-06-30T21:43:33+08:00.
- New aggregate root: outputs/tuned_ablation_wo_lane_nenv16_seed0_seed1_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, DECISION.md.
- proposed_wo_lane seed1 final: d0.00 success=0.88 cost=0.00 route=0.987 lane_dev=0.347; d0.08 success=0.90 cost=0.10 collision=0.10 route=0.971 lane_dev=0.322; d0.15 success=0.62 cost=0.28 collision=0.28 route=0.856 lane_dev=0.340.
- wo_lane seed0-1 mean: d0.00 success=0.940 cost=0.000 route=0.990 lane_dev=0.347; d0.08 success=0.900 cost=0.080 collision=0.080 route=0.964 lane_dev=0.341; d0.15 success=0.610 cost=0.280 collision=0.280 route=0.859 lane_dev=0.344.
- Interpretation: lane reward removal is seed-stable. It does not collapse success, but it consistently produces much higher lane deviation and slightly worse high-density cost/route than full proposed.
- Decision: do not tune wo_lane. Next reward-component replication priority is proposed_wo_smooth seed1, while shield_only seed2 continues to final evaluation.

## 2026-06-30 launch/config check wo_smooth seed1
- Time: 2026-06-30T21:44:26+08:00.
- Root: outputs/tuned_ablation_wo_smooth_nenv16_seed1_1m.
- Launch protocol: proposed_wo_smooth seed1, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, reward_weights.ttc=6.0, lane=1.0, smooth=0.0, accel=0.0, cost=50.0, crash=120.0, out=150.0.
- Early health: alive, stage0/cold-start, success_rate=0. This is expected for a new reward-component ablation and should not be rescued before mid-run evidence.
- Active concurrent run: shield_only seed2 is still training and should be evaluated/aggregated when complete.

## 2026-06-30 shield_only seed2 completed and three-seed aggregate written
- Time: 2026-06-30T21:50:06+08:00.
- New aggregate root: outputs/tuned_compare_shield_only_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- shield_only seed2 final: d0.00 success=1.00 cost=0.00 route=0.992; d0.08 success=0.86 cost=0.08 collision=0.06 out=0.02 route=0.958; d0.15 success=0.76 cost=0.14 collision=0.14 route=0.913.
- shield_only seed0-2 mean: d0.00 success=0.993 cost=0.000 route=0.992; d0.08 success=0.913 cost=0.067 collision=0.047 out=0.020 route=0.959; d0.15 success=0.627 cost=0.227 collision=0.227 route=0.871.
- Comparison to full proposed aggregate at d0.15: shield_only success 0.627 vs full 0.620, cost 0.227 vs 0.247, route 0.871 vs 0.865. Action guard alone matches/slightly exceeds the current full proposed mean.
- Comparison to guard_only at d0.15: shield_only success 0.627 vs guard_only 0.633, cost 0.227 vs 0.207, route 0.871 vs 0.868. Shield-only is close to guard+curriculum.
- Interpretation: action guard is the dominant verified mechanism. Current results do not support a risk-reward-dominant paper claim. Risk/reward components should be framed as high-density refinements unless a new retuned full variant clearly improves beyond shield/guard.
- Active run: proposed_wo_smooth seed1 continues; wait for final summary and aggregate with seed0.

## 2026-06-30 launch/config check proposed retune ttc4-cost10-lane1 seed2
- Time: 2026-06-30T21:51:22+08:00.
- Root: outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed2_1m.
- Rationale: shield_only three-seed aggregate matches/slightly exceeds current full proposed, so a conservative retune is needed. This candidate preserves action guard/curriculum/lane stability while reducing risk-reward aggressiveness.
- Protocol: proposed seed2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, reward_weights.ttc=4.0, lane=1.0, smooth=0.02, accel=0.01, cost=10.0, crash=100.0, out=150.0, ttc_threshold=12.0.
- Evaluation rule: this candidate is only useful if seed2 improves over the current full proposed seed2 and approaches shield_only seed2 at d0.15 without hurting d0.00/d0.08. Otherwise keep the paper claim pivot toward action guard dominance.
- Active concurrent run: proposed_wo_smooth seed1 continues.

## 2026-06-30 mid-run health wo_smooth seed1 and retune seed2
- Time: 2026-06-30T21:57:05+08:00.
- proposed_wo_smooth seed1 around 967k: still training near the end, stage2, success_rate about 0.10, window_success about 0.167, window_cost about 0.10, route window about 0.785. This looks weaker than desired and may confirm that removing smooth/accel harms training stability, but final held-out evaluation is required.
- retune proposed ttc4-cost10-lane1 seed2 around 623k: reached stage2, window_success about 0.333, window_cost about 0.10, window_route about 0.791. It is not collapsed and appears healthier than the original weak full-proposed seed2 at comparable mid-run points, but final d0.15 evaluation against shield_only seed2 is the gate.
- Decision: continue both unchanged. Do not promote retune until formal summary.csv exists.

## 2026-06-30 wo_smooth seed1 completed and seed0-1 aggregate written
- Time: 2026-06-30T22:03:11+08:00.
- New aggregate root: outputs/tuned_ablation_wo_smooth_nenv16_seed0_seed1_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, DECISION.md.
- proposed_wo_smooth seed1 final: d0.00 success=1.00 cost=0.00 route=0.991; d0.08 success=0.80 cost=0.18 collision=0.16 out=0.02 route=0.879; d0.15 success=0.48 cost=0.42 collision=0.40 out=0.02 route=0.736.
- wo_smooth seed0-1 mean: d0.00 success=0.990 cost=0.000 route=0.990; d0.08 success=0.820 cost=0.160 collision=0.150 out=0.010 route=0.909; d0.15 success=0.530 cost=0.330 collision=0.320 out=0.010 route=0.792.
- Interpretation: removing smooth/accel materially hurts stability and high-density evaluation. Smooth/accel terms are not the dominant mechanism, but they should remain in the full setting.
- Decision: continue retune proposed ttc4-cost10-lane1 seed2 to final evaluation before launching more experiments.

## 2026-06-30 proposed retune ttc4-cost10-lane1 seed2 completed and promoted to multi-seed candidate
- Time: 2026-06-30T22:11:54+0800.
- Root: outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed2_1m.
- Protocol: proposed seed2, n_envs=16, 1M steps, horizon=1500, EPISODES=50, reward ttc=4, cost=10, lane=1, smooth=0.02, accel=0.01, crash=100, out=150.
- Formal final: d0.00 success=1.00 cost=0.00 route=0.991; d0.08 success=0.86 cost=0.10 route=0.951; d0.15 success=0.68 cost=0.16 collision=0.14 out=0.02 route=0.871.
- Compared with old full-proposed seed2 at d0.15: success improves 0.48 -> 0.68, cost 0.32 -> 0.16, route 0.826 -> 0.871.
- Compared with shield_only seed2 at d0.15: still lower success/route (0.68/0.871 vs 0.76/0.913), but better than current full-proposed seed2 and competitive with shield_only three-seed mean.
- Decision: promote to multi-seed candidate and launch seed0/seed1. Do not claim final method superiority until the three-seed aggregate exists.

## 2026-06-30 launch retune proposed ttc4-cost10-lane1 seed0/seed1
- Time: 2026-06-30T22:13:15+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed0_1m and outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed1_1m.
- Protocol: variant=proposed, seeds=0/1, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Reward args: ent_coef=0.01, ttc=4, cost=10, overspeed=3, target_speed=18, progress=40, lane=1.0, success_bonus=55, crash_penalty=100, out_of_road_penalty=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Purpose: complete the three-seed stability test for the promising retuned full-proposed candidate after seed2 improved the weak original full-proposed seed2.
- Early launch check: processes alive; formal config verification to follow after config files are fully written.

## 2026-06-30 retune proposed ttc4-cost10-lane1 seed0/1 completed and three-seed aggregate written
- Time: 2026-06-30T22:32:54+0800.
- New aggregate root: outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- seed0 final: d0.00 success=0.94 cost=0.00 route=0.991 lane_dev=0.071; d0.08 success=0.98 cost=0.02 route=0.986 lane_dev=0.081; d0.15 success=0.56 cost=0.26 route=0.819 lane_dev=0.118.
- seed1 final: d0.00 success=0.96 cost=0.00 route=0.991 lane_dev=0.263; d0.08 success=0.82 cost=0.10 route=0.923 lane_dev=0.273; d0.15 success=0.62 cost=0.30 route=0.869 lane_dev=0.359.
- three-seed mean: d0.00 success=0.967 cost=0.000 route=0.991; d0.08 success=0.887 cost=0.073 route=0.953; d0.15 success=0.620 cost=0.240 route=0.853 lane_dev=0.207.
- Interpretation: medium-density result improves over old full proposed, but high-density mean does not beat shield_only or guard_only and lane deviation worsens, especially seed1. Do not promote as final main method.
- Next tuning direction: keep lower risk penalty but strengthen lateral/smooth regularization, or formally pivot claims toward action-guard dominance if the next candidate fails.

## 2026-06-30 launch lateral/smooth retune ttc4-cost10-lane2-smooth004-accel002 seed1/seed2
- Time: 2026-06-30T22:34:02+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane2_smooth004_accel002_nenv16_seed1_1m and outputs/retune_proposed_ttc4_cost10_lane2_smooth004_accel002_nenv16_seed2_1m.
- Protocol: proposed, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Reward args: ent_coef=0.01, ttc=4, cost=10, lane=2.0, smooth=0.04, accel=0.02, overspeed=3, target_speed=18, progress=40, success_bonus=55, crash_penalty=100, out_of_road_penalty=150, ttc_threshold=12.
- Rationale: previous ttc4-cost10-lane1 aggregate improved d0.08 but failed to beat guard/shield at d0.15 and had high lane deviation, especially seed1. This run tests whether stronger lateral/smooth regularization fixes that failure without losing seed2 high-density behavior.
- Gate: promote only if seed1 lane deviation drops materially and d0.15 success/route/cost improve without seed2 collapsing.

## 2026-06-30 abort lateral/smooth retune lane2-smooth004-accel002 seed1/seed2
- Time: 2026-06-30T22:38:56+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane2_smooth004_accel002_nenv16_seed1_1m and seed2_1m.
- Abort reason: mid-run evidence showed severe progress suppression. At about 524k/540k timesteps both runs remained in stage0 with window_route_completion about 0.10/0.09 and success_rate 0. This is much worse than the preceding ttc4-cost10-lane1 retune, which had already reached stage1/2 by this point.
- Diagnosis: lane=2.0 plus smooth=0.04/accel=0.02 over-regularizes motion and should not be completed as a formal candidate.
- Decision: stop these diagnostic runs and launch a gentler lateral retune instead: lane around 1.25, smooth 0.03, accel 0.015, with slightly higher progress reward to preserve motion.

## 2026-06-30 launch moderate lateral retune ttc4-cost10-lane125-smooth003-accel0015-progress45 seed1/seed2
- Time: 2026-06-30T22:39:26+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane125_smooth003_accel0015_progress45_nenv16_seed1_1m and seed2_1m.
- Protocol: proposed, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Reward args: ent_coef=0.01, ttc=4, cost=10, lane=1.25, smooth=0.03, accel=0.015, progress=45, overspeed=3, target_speed=18, success_bonus=55, crash_penalty=100, out_of_road_penalty=150, ttc_threshold=12.
- Rationale: lane2/smooth004 over-regularized and suppressed progress; this is a gentler lateral-stability retune with extra progress reward to preserve motion.
- Gate: seed1 must reduce lane deviation versus lane1 retune without losing d0.15 success/route; seed2 must remain competitive with its previous d0.15 result.

## 2026-06-30 moderate lateral retune seed1/seed2 diagnostic aggregate completed
- Time: 2026-06-30T23:00:54+0800.
- Aggregate root: outputs/retune_proposed_ttc4_cost10_lane125_smooth003_accel0015_progress45_nenv16_seed1_seed2_diagnostic_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_lane1_same_seeds.csv, compare_to_lane1_seed1_seed2_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- seed1 final: d0.00 success=0.98 cost=0.00 route=0.990 lane_dev=0.060; d0.08 success=0.88 cost=0.12 route=0.945 lane_dev=0.072; d0.15 success=0.64 cost=0.28 route=0.849 lane_dev=0.102.
- seed2 final: d0.00 success=0.98 cost=0.00 route=0.989 lane_dev=0.101; d0.08 success=0.88 cost=0.08 route=0.969 lane_dev=0.126; d0.15 success=0.62 cost=0.28 route=0.852 lane_dev=0.198.
- Two-seed mean: d0.00 success=0.980 cost=0.000 route=0.990 lane_dev=0.081; d0.08 success=0.880 cost=0.100 route=0.957 lane_dev=0.099; d0.15 success=0.630 cost=0.280 route=0.850 lane_dev=0.150.
- Interpretation: seed1 lateral instability is repaired, but seed2 high-density robustness degrades versus lane1. This candidate fails the promotion gate; do not run seed0.
- Next action: stop risk/lane reward-only retuning for now and test guard-centered/threshold-centered variants, since repeated full-risk retunes do not beat guard_only or shield_only.

## 2026-06-30 launch guard-centered guard_only ttc13/v18 seed1/seed2
- Time: 2026-06-30T23:02:49+0800.
- Roots: outputs/retune_guard_only_ttc13_v18_nenv16_seed1_1m and outputs/retune_guard_only_ttc13_v18_nenv16_seed2_1m.
- Protocol: variant=guard_only, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Active mechanism: use_action_guard=True, use_risk_reward=False, curriculum=True. Because risk reward is disabled, reward penalty weights are protocol records; behavior-relevant guard parameters are ttc_threshold=13 and target_speed=18.
- Rationale: repeated full-risk/lane retunes failed to beat guard_only/shield_only. A mild guard threshold shift tests whether action-guard-centered tuning can lower high-density cost without the instability previously observed for full-proposed ttc14/v18.
- Gate: promote only if seed1/seed2 keep d0.08 success near guard_only and improve d0.15 cost/route versus guard_only same seeds. Abort or reject if training suppresses route progress or seed2 worsens materially.

## 2026-06-30 guard_only ttc13/v18 config verification
- Time: 2026-06-30T23:03:52+0800.
- Verified both seed1 and seed2 configs: variant=guard_only, n_envs=16, horizon=1500, timesteps=1M, ent_coef=0.01, use_action_guard=True, use_risk_reward=False, curriculum=True.
- Verified behavior-relevant guard parameters: reward_weights.ttc_threshold=13.0 and target_speed_kmh=18.0. Stage gates: stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Early health around 82k: both processes alive; stage0/warmup route progress present, no launch/config mismatch.

## 2026-06-30 guard_only ttc13/v18 monitor at ~278k
- Time: 2026-06-30T23:06:15+0800.
- seed1 around 278k: stage2, window_success about 0.30-0.35, window_cost about 0.067, window_route about 0.776, rollout success_rate about 0.35. One sampled out_of_road episode appeared, but route progress is healthy.
- seed2 around 278k: stage2, window_success about 0.30, window_cost about 0.133, window_route about 0.855, rollout success_rate about 0.26.
- Decision: continue unchanged. This does not show the progress-suppression failure seen in the over-regularized lane2 run. Final held-out d0.08/d0.15 remains the gate.

## 2026-06-30 guard_only ttc13/v18 monitor at ~410k
- Time: 2026-06-30T23:09:45+0800.
- seed1 around 410k: stage2, window_cost about 0.033, window_route_completion about 0.808, window_success about 0.000-0.033, recent route samples 0.874-0.975, rollout success_rate about 0.02-0.03.
- seed2 around 410k: stage3, window_cost about 0.10, window_route_completion about 0.726, window_success about 0.033, recent route samples 0.533-0.813.
- Interpretation: progress is not suppressed and cost is not exploding, but success window is weak in the middle. Continue unchanged; final held-out evaluation is required before accepting/rejecting ttc13.

## 2026-06-30 guard_only ttc13/v18 monitor at ~600k
- Time: 2026-06-30T23:14:09+0800.
- seed1 around 606k-623k: stage2, window_cost about 0.000, window_route_completion about 0.838-0.847, window_success about 0.133-0.233, rollout success_rate about 0.20.
- seed2 around 590k-606k: stage2, window_cost about 0.000-0.033, window_route_completion about 0.838-0.841, window_success about 0.133-0.267, rollout success_rate about 0.22-0.24. One sampled collision appeared, but the rolling cost window remained low.
- Decision: continue to formal evaluation. ttc13 is not showing obvious training collapse; final d0.15 cost/route versus guard_only same seeds will decide.

## 2026-06-30 guard_only ttc13/v18 near-end training monitor
- Time: 2026-06-30T23:21:35+0800.
- seed1 around 950k-983k: stage2, window_cost 0.000-0.033, window_route about 0.789-0.835, rollout success_rate about 0.10-0.12.
- seed2 around 934k-967k: stage2, window_cost 0.067-0.100, window_route about 0.770-0.810, rollout success_rate about 0.20-0.23, with a sampled collision near 967k.
- Interpretation: no route/cost collapse, but success windows remain weak. Wait for formal evaluation before deciding; likely gate is whether d0.15 cost reduction compensates for possible success loss.

## 2026-06-30 guard_only ttc13/v18 seed1/seed2 diagnostic aggregate completed
- Time: 2026-06-30T23:28:54+0800.
- Aggregate root: outputs/retune_guard_only_ttc13_v18_nenv16_seed1_seed2_diagnostic_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_guard_only_same_seeds.csv, compare_to_guard_only_seed1_seed2_mean.csv, compare_to_guard_only_three_seed_mean.csv, compare_to_shield_only_three_seed_mean.csv, DECISION.md.
- seed1 final: d0.00 success=0.98 cost=0.00 route=0.990; d0.08 success=0.84 cost=0.08 route=0.954; d0.15 success=0.58 cost=0.20 route=0.857.
- seed2 final: d0.00 success=0.98 cost=0.00 route=0.989; d0.08 success=0.84 cost=0.16 route=0.929; d0.15 success=0.62 cost=0.16 route=0.886.
- Two-seed mean: d0.00 success=0.980 cost=0.000 route=0.990; d0.08 success=0.840 cost=0.120 route=0.941; d0.15 success=0.600 cost=0.180 route=0.872.
- Decision: do not run seed0. ttc13 is mixed parameter-sensitivity evidence, not a promoted guard-centered setting. Default guard_only ttc12/v18 remains the cleaner action-guard baseline.

## 2026-06-30 launch guard-centered guard_only ttc12/v19 seed1/seed2
- Time: 2026-06-30T23:29:27+0800.
- Roots: outputs/retune_guard_only_ttc12_v19_nenv16_seed1_1m and outputs/retune_guard_only_ttc12_v19_nenv16_seed2_1m.
- Protocol: variant=guard_only, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Active mechanism: use_action_guard=True, use_risk_reward=False, curriculum=True. Behavior-relevant guard parameters: ttc_threshold=12, target_speed=19.
- Rationale: ttc13/v18 reduced some seed2 high-density cost but hurt seed1 and d0.08 success. This orthogonal branch keeps the accepted TTC threshold and relaxes only the overspeed guard target to test whether d0.15 success/route can improve without a large cost penalty.
- Gate: promote only if seed1/seed2 improve d0.15 success or route versus guard_only ttc12/v18 same seeds while keeping d0.08 success/cost close. Reject if high-density cost increases materially or d0.08 degrades.

## 2026-06-30 guard_only ttc12/v19 config verification
- Time: 2026-06-30T23:30:30+0800.
- Verified both seed1 and seed2 configs: variant=guard_only, n_envs=16, horizon=1500, timesteps=1M, ent_coef=0.01, use_action_guard=True, use_risk_reward=False, curriculum=True.
- Verified behavior-relevant guard parameters: reward_weights.ttc_threshold=12.0 and target_speed_kmh=19.0. Stage gates: stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Early health around 82k: both processes alive; warmup has route progress but sampled out_of_road episodes. Too early to judge; continue to stage transition checks.

## 2026-06-30 guard_only ttc12/v19 monitor at ~300k
- Time: 2026-06-30T23:33:24+0800.
- seed1 around 295k-311k: stage2, window_cost about 0.10-0.133, window_route_completion about 0.809-0.817, window_success about 0.167-0.20, rollout success_rate about 0.28-0.30.
- seed2 around 279k-295k: reached stage3, window_cost about 0.133, window_route_completion about 0.867, window_success about 0.533, rollout success_rate about 0.31.
- Decision: continue unchanged. This branch is not stuck and seed2 is stronger than the ttc13/v18 branch at the same stage; final held-out cost will decide whether the relaxed speed guard is acceptable.

## 2026-06-30 guard_only ttc12/v19 monitor at ~786k/~655k
- Time: 2026-06-30T23:42:23+0800.
- seed1 around 786k: stage2, window_cost about 0.067, window_route_completion about 0.863, window_success about 0.267, rollout success_rate about 0.28. Latest sampled episode had collision cost, but rolling cost remains controlled; continue to final evaluation.
- seed2 around 655k: stage3, window_cost about 0.233, window_route_completion about 0.704, window_success about 0.100, rollout success_rate about 0.11. This is weaker than the early stage3 signal and close to the cost gate; continue but treat as a warning unless final held-out evaluation improves.
- Resource: CPU available about 18GiB; GPU memory used about 1.37GiB / 12.28GiB; protocol remains resource-safe.
- Decision: continue both unchanged. Do not launch seed0 or additional guard-centered runs until seed1/seed2 produce summary.csv and are compared against guard_only ttc12/v18 same seeds.

## 2026-06-30 guard_only ttc12/v19 monitor at ~934k/~754k
- Time: 2026-06-30T23:45:32+0800.
- seed1 around 934k: stage2, window_cost about 0.067, window_route_completion about 0.852, window_success about 0.300, rollout success_rate about 0.34. Latest sampled episode has no cost/collision/out-of-road and route_completion about 0.905. Seed1 is close to final and remains usable.
- seed2 around 754k: stage3, window_cost about 0.233, window_route_completion about 0.720, window_success about 0.067, rollout success_rate about 0.10. Latest sampled episode has collision cost and low route_completion about 0.273. This is a warning against promoting v19 unless final eval recovers strongly.
- Decision: continue to final summaries, but provisional judgement is mixed/weak. Do not launch v19 seed0 before seed1/seed2 final comparison.

## 2026-06-30 guard_only ttc12/v19 seed1/seed2 diagnostic aggregate completed
- Time: 2026-06-30T23:56:10+0800.
- Aggregate root: outputs/retune_guard_only_ttc12_v19_nenv16_seed1_seed2_diagnostic_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_guard_only_same_seeds.csv, compare_to_guard_only_seed1_seed2_mean.csv, compare_to_guard_only_three_seed_mean.csv, compare_to_shield_only_three_seed_mean.csv, DECISION.md.
- seed1 final: d0.00 success=0.98 cost=0.00 route=0.990; d0.08 success=0.92 cost=0.06 route=0.954; d0.15 success=0.58 cost=0.28 route=0.861.
- seed2 final: d0.00 success=1.00 cost=0.00 route=0.992; d0.08 success=0.84 cost=0.16 route=0.938; d0.15 success=0.72 cost=0.26 route=0.871.
- Two-seed mean: d0.00 success=0.990 cost=0.000 route=0.991; d0.08 success=0.880 cost=0.110 route=0.946; d0.15 success=0.650 cost=0.270 route=0.866.
- Same-seed comparison to default guard_only ttc12/v18 at d0.15: success improves only 0.64 -> 0.65, cost worsens 0.20 -> 0.27, route is essentially unchanged/slightly lower 0.871 -> 0.866.
- Decision: reject target_speed=19 as final guard-centered setting; do not launch seed0. Keep default guard_only ttc12/v18 and shield_only as cleaner action-guard baselines.


## 2026-06-30 launch no_action_guard seed1/seed2 nenv16 ablation completion
- Time: 2026-06-30T23:57:05+0800.
- Roots: outputs/tuned_ablation_no_action_guard_nenv16_seed1_1m and outputs/tuned_ablation_no_action_guard_nenv16_seed2_1m.
- Protocol: variant=no_action_guard, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Mechanism: use_risk_reward=True, use_action_guard=False, curriculum=True. This completes the planned three-seed evidence for the dominant action-guard ablation after seed0 collapsed.
- Gate: do not rescue/tune mid-run unless there is a launch/config failure. If both seeds reproduce high cost/low success, aggregate with seed0 and use as strong evidence that action guard is necessary.

## 2026-07-01 no_action_guard seed1/seed2 monitor at ~280k/295k
- Time: 2026-07-01T00:02:05+0800.
- seed1 around 279k: stage0, window_cost=0, window_route_completion about 0.153, window_success=0, rollout success_rate=0, mean_speed about 0.98 km/h, std about 1.01.
- seed2 around 295k: stage0, window_cost=0, window_route_completion about 0.199, window_success=0, rollout success_rate=0, mean_speed about 1.28 km/h, std about 1.00.
- Interpretation: no launch/config failure. The ablation is currently failing to form useful driving behavior rather than crashing; this is relevant mechanism evidence, so continue to final evaluation unless the process fails.
- Resource: GPU memory used about 1.36GiB / 12.28GiB; CPU available about 21GiB. Continue both unchanged.

## 2026-07-01 no_action_guard seed1/seed2 monitor at ~541k/~573k
- Time: 2026-07-01T00:04:33+0800.
- seed1 around 541k: reached stage1, window_cost=0, window_route_completion about 0.674, window_success about 0.467, rollout success_rate about 0.37, mean_speed about 11.6 km/h.
- seed2 around 573k: reached stage1, window_cost about 0.067, window_route_completion about 0.669, window_success about 0.433, rollout success_rate about 0.43, mean_speed about 10.6 km/h.
- Interpretation: unlike seed0 and the early 280k check, these seeds have recovered some driving behavior. Do not claim no_action_guard universally collapses until final held-out evaluation. Continue unchanged and aggregate with seed0 after summaries exist.

## 2026-07-01 no_action_guard seed1/seed2 monitor at ~754k/~786k
- Time: 2026-07-01T00:07:31+0800.
- seed1 around 754k: stage1, window_cost about 0.233, window_route_completion about 0.813, window_success about 0.600, rollout success_rate about 0.39. Latest sampled episode has no cost but route_completion about 0.668.
- seed2 around 786k: stage2, window_cost about 0.033, window_route_completion about 0.895, window_success about 0.667, rollout success_rate about 0.39. Latest sampled episode route_completion about 0.986.
- Interpretation: no_action_guard seed1/2 are not reproducing a simple universal collapse. The final ablation claim must be based on held-out d0.08/d0.15 cost/success and seed variance, not only seed0. Continue to final evaluation unchanged.

## 2026-07-01 no_action_guard seed0/1/2 aggregate completed
- Time: 2026-07-01T00:13:20+0800.
- Aggregate root: outputs/tuned_ablation_no_action_guard_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.027 cost=0.973 route=0.254; d0.08 success=0.000 cost=1.000 route=0.202; d0.15 success=0.000 cost=1.000 route=0.172.
- Failure mode: low density mostly out_of_road; medium/high density mix collision and out_of_road. seed1/2 had temporary training-window recovery, but held-out evaluation still collapsed.
- Decision: accept as three-seed no_action_guard ablation. Do not rescue/tune this ablation; action-level guard is necessary for stable held-out safety/completion under the current method.


## 2026-07-01 launch wo_lane seed2 and wo_smooth seed2 nenv16 ablation completion
- Time: 2026-07-01T00:14:10+0800.
- Roots: outputs/tuned_ablation_wo_lane_nenv16_seed2_1m and outputs/tuned_ablation_wo_smooth_nenv16_seed2_1m.
- Protocol: variants=proposed_wo_lane/proposed_wo_smooth, seed=2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Purpose: complete third seed for lane and smooth/accel reward-component ablations after seed0/1 aggregates showed high lane deviation and stability degradation respectively.
- Gate: run to final evaluation unless process/config fails; aggregate with seed0/1 after summaries exist.

## 2026-07-01 invalidated first wo_lane/wo_smooth seed2 launch due wrong ablation weights
- Time: 2026-07-01T00:16:00+0800.
- Issue: initial seed2 launches for proposed_wo_lane and proposed_wo_smooth were passed default reward weights, producing configs with lane=1.0 for wo_lane and smooth=0.02/accel=0.01 for wo_smooth, unlike seed0/seed1 where lane=0.0 or smooth=0.0/accel=0.0.
- Action: stopped the invalid process groups and archived the partial roots with INVALID_DO_NOT_USE.txt. These runs must not enter any table or aggregate.
- Fix: relaunch seed2 using explicit ablation weights: wo_lane with --reward-lane 0.0; wo_smooth with --reward-smooth 0.0 --reward-accel 0.0.

## 2026-07-01 corrected wo_lane/wo_smooth seed2 monitor at ~311k/~360k
- Time: 2026-07-01T00:18:52+0800.
- proposed_wo_lane seed2 around 311k: stage1, window_cost about 0.233, window_route_completion about 0.630, window_success=0, rollout success_rate about 0.03, lane_deviation about 0.463. This is consistent with lane-reward removal causing lateral instability; continue.
- proposed_wo_smooth seed2 around 360k: stage0, window_cost=0, window_route_completion about 0.459, window_success=0, rollout success_rate=0, mean_speed about 3.67 km/h. This is slower than desired but still making route progress; continue to 500k/750k before judging.
- Resource: GPU memory used about 1.35GiB / 12.28GiB. Continue both unchanged.

## 2026-07-01 corrected wo_lane/wo_smooth seed2 monitor at ~573k/~606k
- Time: 2026-07-01T00:21:53+0800.
- proposed_wo_lane seed2 around 573k: stage2, window_cost about 0.133, window_route_completion about 0.842, window_success about 0.300, rollout success_rate about 0.14, lane_deviation about 0.449. Lateral deviation remains high, consistent with lane-reward removal.
- proposed_wo_smooth seed2 around 606k: stage2, window_cost=0, window_route_completion about 0.865, window_success about 0.300, rollout success_rate about 0.34. This recovered from the earlier slow stage0, so final held-out metrics are needed.
- Decision: continue both unchanged to final evaluation and aggregate with seed0/1.

## 2026-07-01 wo_lane and wo_smooth seed2 completed; three-seed aggregates written
- Time: 2026-07-01T00:36:00+0800.
- Corrected seed2 runs used matching ablation weights after invalid first launch was archived.
- wo_lane aggregate root: outputs/tuned_ablation_wo_lane_nenv16_seed0_seed1_seed2_aggregate. Mean d0.15 success=0.607 cost=0.280 route=0.844 lane_dev=0.362. Decision: accept as lane-reward ablation; lane term supports lateral stability/route quality, not dominant raw success.
- wo_smooth aggregate root: outputs/tuned_ablation_wo_smooth_nenv16_seed0_seed1_seed2_aggregate. Mean d0.15 success=0.567 cost=0.287 route=0.821 lane_dev=0.245. Decision: accept as smooth/accel ablation; smooth/accel terms are stabilizers with high seed variance.
- PDF check: seed2 PDFs are under each run figures/ directory; no loose PDFs found for these runs.


## 2026-07-01 launch risk seed1/seed2 nenv16 formal comparator completion
- Time: 2026-07-01T00:37:00+0800.
- Roots: outputs/tuned_compare_risk_nenv16_seed1_1m and outputs/tuned_compare_risk_nenv16_seed2_1m.
- Protocol: variant=risk, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Purpose: complete the risk-only comparator after seed0 produced near-zero route/success. This tests whether risk reward alone is enough or whether action guard/curriculum mechanisms dominate.
- Gate: run to final evaluation unless config/process fails; aggregate with seed0 after summaries exist.

## 2026-07-01 risk seed1/seed2 monitor at ~180k
- Time: 2026-07-01T00:39:59+0800.
- seed1 around 180k: success_rate=0, route_completion about 0.025, mean_speed about 0.54 km/h, no cost/collision/out_of_road, std about 1.02.
- seed2 around 180k: success_rate=0, route_completion about 0.043, mean_speed about 0.77 km/h, no cost/collision/out_of_road, std about 1.01.
- Interpretation: risk-only without curriculum is currently low-speed/low-route and resembles seed0 early failure, but it is still early. Continue to 500k before deciding whether the comparator consistently fails.

## 2026-07-01 risk seed1/seed2 monitor at ~475k/~442k
- Time: 2026-07-01T00:44:02+0800.
- seed1 around 475k: success_rate=0, route_completion about 0.017, mean_speed about 0.44 km/h, cost=0. This is low-speed/route-stagnation failure, not useful safety.
- seed2 around 442k: success_rate=0, route_completion about 0.010, mean_speed about 0.44 km/h, cost=0. Same failure mode.
- Interpretation: risk reward + action guard without curriculum is not learning usable driving by mid-training, matching seed0 behavior. Continue to final evaluation for comparator evidence; do not tune this comparator mid-run.



## 2026-07-01 risk seed0/1/2 formal comparator aggregate completed
- Time: 2026-07-01T00:58:42+0800.
- Aggregate root: outputs/tuned_compare_risk_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.000 cost=0.000 route=0.009 speed=0.013; d0.08 success=0.000 cost=0.000 route=0.009 speed=0.013; d0.15 success=0.000 cost=0.000 route=0.009 speed=0.014.
- Decision: accept as risk-only formal comparator. This is a route-stagnation failure, not a safety success; zero cost is non-informative because the policy barely drives.
- Paper claim boundary: risk reward + action guard without curriculum does not learn usable driving under the formal n_envs=16 protocol. Do not tune this comparator; move to baseline/curriculum seed completion.
- PDF placement: run PDFs are under each single-run figures/ directory; aggregate directory intentionally contains only CSV/Markdown evidence.


## 2026-07-01 stress density 0.20/0.25 nenv16 evaluation completed
- Time: 2026-07-01T02:55:36.125071+08:00.
- Root: outputs/stress_density_020_025_nenv16_20260701_0153.
- Protocol: evaluation-only, densities 0.20 and 0.25, EPISODES=50 per density, n_envs=16, device=cuda, frozen models only.
- Labels/seeds: guard_only, shield_only, retune_proposed_ttc4_cost10_lane1, baseline, curriculum, risk, full_proposed_candidate; each has seeds 0/1/2 and 100 episode rows per seed.
- Execution: all 21 label/seed evals succeeded or were skipped because a valid CSV already existed; no active stress process remains.
- d0.20 means: shield_only success=0.480 cost=0.360 route=0.778; retuned full proposed success=0.453 cost=0.380 route=0.753; guard_only success=0.413 cost=0.407 route=0.733; full proposed candidate success=0.380 cost=0.400 route=0.744.
- d0.25 means: guard_only success=0.267 cost=0.487 route=0.658; full proposed candidate success=0.207 cost=0.587 route=0.587; shield_only success=0.193 cost=0.587 route=0.609; retuned full proposed success=0.173 cost=0.687 route=0.571.
- Failure controls: baseline/curriculum have success=0 and cost=1.0 at both stress densities; risk has near-zero route and zero cost, so it is idle/stagnation rather than safety.
- Decision: accept as frozen high-density stress evidence. Use it to support action-guard-centered robustness and graceful degradation; do not claim risk-reward dominance.


## 2026-07-01 proposed_gated_risk mechanism added and seed1/seed2 launched
- Time: 2026-07-01T03:10:01+08:00.
- Code change: added variant=proposed_gated_risk with use_risk_reward=True, use_action_guard=True, curriculum=True, and use_gated_risk_reward=True.
- Mechanism: continuous TTC/lane/smooth/accel/overspeed penalties are gated by meaningful motion/progress plus local risk; event cost, crash penalty, out-of-road penalty, progress reward, idle penalty, and action guard remain active. This targets the observed risk-reward idle/stagnation failure without changing the formal n_envs=16 evaluation protocol.
- Static/smoke verification: py_compile passed; config instantiation passed; short n_envs=16 smoke root outputs/smoke_proposed_gated_risk_20260701_0308 trained/evaluated and produced risk_gate_rate/continuous_risk_penalty/event_risk_penalty columns. Smoke is diagnostic only and must not enter paper tables.
- Formal diagnostic launches: outputs/gated_risk_proposed_nenv16_seed1_1m pid=109861 and outputs/gated_risk_proposed_nenv16_seed2_1m pid=109916.
- Protocol: timesteps=1M, horizon=1500, n_envs=16, EPISODES=50, DEVICE=cuda, ent_coef=0.01, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Gate: run seed1/seed2 to held-out evaluation unless process/config fails; decide on seed0 only after inspecting final metrics and failure mode versus guard_only/shield_only/retuned full proposed.


## 2026-07-01 proposed_gated_risk seed1/seed2 monitor at ~472k/~482k
- Time: 2026-07-01T03:12:58+08:00.
- seed1 around 472k env steps: recent100 success=0.090, cost=0.010, collision=0.000, out_of_road=0.010, route=0.292, speed=2.824, risk_gate_rate=0.170, continuous_risk_penalty=35.084, event_risk_penalty=0.100, shield_rate=0.002, curriculum_stage about 0.20.
- seed2 around 482k env steps: recent100 success=0.080, cost=0.080, collision=0.000, out_of_road=0.080, route=0.275, speed=2.441, risk_gate_rate=0.186, continuous_risk_penalty=28.587, event_risk_penalty=0.800, shield_rate=0.001, curriculum_stage about 0.14.
- Interpretation: gated risk is not collapsing into the risk-only near-zero-route failure, and safety/cost is currently low. However speed/stage/route are still conservative versus guard_only/shield_only; do not claim improvement from this window. Continue to final held-out evaluation before deciding on seed0 or mechanism revision.


## 2026-07-01 proposed_gated_risk seed1/seed2 monitor at ~711k/~728k
- Time: 2026-07-01T03:16:32+08:00.
- seed1 around 711k env steps: recent100 success=0.170, cost=0.010, collision=0.000, out_of_road=0.010, route=0.472, speed=6.856, risk_gate_rate=0.269, continuous_risk_penalty=53.112, event_risk_penalty=0.100, shield_rate=0.023, curriculum_stage about 0.68.
- seed2 around 728k env steps: recent100 success=0.170, cost=0.080, collision=0.020, out_of_road=0.060, route=0.473, speed=6.977, risk_gate_rate=0.279, continuous_risk_penalty=46.953, event_risk_penalty=0.800, shield_rate=0.032, curriculum_stage about 0.65.
- Interpretation: this is a recovery from the ~480k conservative window and clearly avoids risk-only route stagnation. Still, training-window metrics remain weaker than the guard/shield-centered best evidence, so continue to final held-out evaluation before deciding whether seed0 is worthwhile.


## 2026-07-01 proposed_gated_risk seed1/seed2 evaluation completed; seed0 launched
- Time: 2026-07-01T03:28:44+08:00.
- Completed roots: outputs/gated_risk_proposed_nenv16_seed1_1m and outputs/gated_risk_proposed_nenv16_seed2_1m.
- Per-seed held-out summary: seed1 d0.00/d0.08/d0.15 success=0.94/0.80/0.62, cost=0.00/0.10/0.28; seed2 success=0.94/0.90/0.56, cost=0.00/0.06/0.28.
- Preliminary two-seed aggregate: outputs/gated_risk_proposed_nenv16_seed1_seed2_prelim_aggregate. Mean d0.00 success=0.940 cost=0.000 route=0.987; d0.08 success=0.850 cost=0.080 route=0.959; d0.15 success=0.590 cost=0.280 route=0.843.
- Decision: gated risk fixes risk-only stagnation and is worth completing as a three-seed mechanism diagnostic, but current two-seed d0.15 does not displace guard_only/shield_only/retuned full. Keep guard/shield-centered paper claim boundary.
- New launch: outputs/gated_risk_proposed_nenv16_seed0_1m pid=111544, same 1M/horizon1500/n_envs16/EPISODES50 protocol with ent_coef=0.01, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.


## 2026-07-01 proposed_gated_risk seed0 monitor at ~497k
- Time: 2026-07-01T03:32:54+08:00.
- seed0 around 497k env steps: recent100 success=0.060, cost=0.010, collision=0.000, out_of_road=0.010, route=0.290, speed=2.895, risk_gate_rate=0.189, continuous_risk_penalty=38.136, event_risk_penalty=0.100, shield_rate=0.003, curriculum_stage about 0.26.
- Interpretation: seed0 matches seed1/seed2 mid-training recovery pattern and has no process/config failure. Continue unchanged to late-training and final held-out evaluation.


## 2026-07-01 proposed_gated_risk seed0 monitor at ~744k
- Time: 2026-07-01T03:35:50+08:00.
- seed0 around 744k env steps: recent100 success=0.150, cost=0.010, collision=0.000, out_of_road=0.010, route=0.463, speed=6.460, risk_gate_rate=0.274, continuous_risk_penalty=54.981, event_risk_penalty=0.100, shield_rate=0.024, curriculum_stage about 0.71.
- Interpretation: seed0 has the same late-training recovery pattern as seed1/seed2. Continue unchanged to model save and held-out evaluation.


## 2026-07-01 proposed_gated_risk three-seed aggregate completed
- Time: 2026-07-01T03:46:11+08:00.
- Aggregate root: outputs/gated_risk_proposed_nenv16_seed0_seed1_seed2_aggregate.
- Completed single-run roots: outputs/gated_risk_proposed_nenv16_seed0_1m, outputs/gated_risk_proposed_nenv16_seed1_1m, outputs/gated_risk_proposed_nenv16_seed2_1m.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, compare_to_retune_full_mean.csv, compare_to_risk_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.940 cost=0.000 route=0.988; d0.08 success=0.867 cost=0.080 route=0.961; d0.15 success=0.600 cost=0.253 route=0.849.
- Mechanism metrics: risk_gate_rate mean is 0.887/0.865/0.764 at d0.00/d0.08/d0.15; out_of_road=0.000 at all formal densities.
- Decision: accept as completed mechanism diagnostic. Gated risk fixes the risk-only stagnation failure, but does not replace the guard_only/shield_only/retuned-full main evidence because d0.15 remains slightly weaker.
- Paper package addendum: codex_longrun_iscsic/paper_tables_20260701_0258/gated_risk_mechanism_addendum.csv and gated_risk_mechanism_addendum.md.
- PDF placement: all generated PDFs are under the single-run figures/ directories; aggregate/addendum directories remain CSV/Markdown only.


## 2026-07-01 proposed_gated_risk stress eval launched
- Time: 2026-07-01T03:48:14+08:00.
- Root: outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346.
- Protocol: frozen proposed_gated_risk seed0/1/2 models, densities 0.20 and 0.25, 50 episodes per density, n_envs=16, device=cuda.
- Execution: serial driver PID 112760, seed0 evaluation confirmed running. Purpose is addendum evidence against the existing 0.20/0.25 stress table, not a new training run.


## 2026-07-01 proposed_gated_risk stress addendum completed
- Time: 2026-07-01T04:00:34+08:00.
- Stress root: outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346.
- Aggregate root: outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346/aggregate.
- Files: status.tsv, evaluations/proposed_gated_risk_ppo_s0.csv, evaluations/proposed_gated_risk_ppo_s1.csv, evaluations/proposed_gated_risk_ppo_s2.csv, aggregate/summary_by_seed.csv, aggregate/mean_by_density.csv, aggregate/std_by_density.csv, aggregate/rank_with_existing_stress.csv, aggregate/DECISION.md.
- Three-seed stress mean: d0.20 success=0.447 cost=0.367 route=0.766; d0.25 success=0.220 cost=0.527 route=0.628.
- Existing stress comparison: at d0.20 proposed_gated_risk ranks behind shield_only and retuned full by success; at d0.25 it ranks second behind guard_only by success/cost/route ordering.
- Paper package addendum: codex_longrun_iscsic/paper_tables_20260701_0258/gated_risk_stress_mean.csv, gated_risk_stress_rank_with_existing.csv, gated_risk_stress_addendum.md.
- Final boundary: conditional risk shaping is useful and improves over risk-only/retuned-full in some stress settings, but does not overturn the guard/shield-centered main claim.
- Process/PDF check: no active training/evaluation process remains; aggregate and paper_table directories contain no PDFs.


## 2026-07-01 reviewer robustness and behavior addenda completed
- Time: 2026-07-01T04:11:29+08:00.
- Updated coverage audit: codex_longrun_iscsic/EXPERIMENT_COVERAGE_AUDIT_20260701_0405.md.
- Reviewer statistics files in paper package: seed_level_robustness_formal.csv, seed_paired_deltas_vs_guard_shield.csv, seed_level_robustness_stress.csv, reviewer_statistics_notes.md.
- Behavior rollout directory: codex_longrun_iscsic/behavior_rollouts_20260701_0406.
- Representative qualitative seed: density=0.15, map_seed=10003. guard_only/shield_only/retuned_full/proposed_gated_risk succeed; no_action_guard fails by collision/high speed; risk_only has near-zero route and zero cost due stagnation.
- Representative plot: codex_longrun_iscsic/behavior_rollouts_20260701_0406/representative_density_0p15_seed10003.pdf.
- Paper package pointer: codex_longrun_iscsic/paper_tables_20260701_0258/behavior_rollout_addendum.md.
- Boundary: behavior plots are qualitative mechanism illustrations only, not replacements for aggregate metrics.

## 2026-07-01 final paper manifest and PDF placement

- Created `codex_longrun_iscsic/final_paper_manifest_20260701_0415`.
- Paper-facing PDFs copied to `codex_longrun_iscsic/final_paper_manifest_20260701_0415/pdf_figures/`.
- Tables/TeX copied or generated in the manifest root; aggregate claim source remains `codex_longrun_iscsic/paper_tables_20260701_0258`.
- Historical run PDFs remain in `outputs/*/figures/` for provenance only.

## 2026-07-01 external seed robustness nenv16 launched

- Time: 2026-07-01T04:27:43.008115+08:00.
- Root: `outputs/external_seed_robustness_nenv16_20260701_0425`.
- Driver: `codex_longrun_iscsic/run_external_seed_robustness_nenv16_20260701_0425.sh`.
- Active PID at launch check: driver `116825`.
- Protocol: frozen completed models, `n_envs=16`, `episodes=50`, densities `0.08/0.15`, external `test_start_seed=20000/30000`.
- Variants: `guard_only`, `shield_only`, `retuned_full`, `proposed_gated_risk`, `risk_only`, `no_action_guard`; seeds `0/1/2` each.
- Purpose: reviewer-facing external scenario-seed validation of the guard/shield-centered paper claim, not new reward tuning.
- Decision rule: aggregate by label/density after each finished unit; if positive methods degrade, report sensitivity instead of hiding it; do not interpret risk-only zero cost without route completion.
