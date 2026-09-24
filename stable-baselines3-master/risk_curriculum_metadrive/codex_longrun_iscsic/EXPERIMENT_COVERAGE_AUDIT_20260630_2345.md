# EXPERIMENT_COVERAGE_AUDIT_20260630_2345

Scope: current n_envs=16 MetaDrive/SB3 evidence for paper-facing experiment planning. This audit separates promoted evidence, diagnostic evidence, active runs, and remaining gaps. It should be updated after the active v19 guard-centered runs finish.

## Current Paper Direction

The strongest verified mechanism is the action guard / shield family. Repeated full-risk reward retunes have not yet beaten guard_only or shield_only at high density in a stable three-seed way. Therefore the paper claim should not be framed as risk-reward dominance unless a later full proposed retune clearly exceeds guard/shield baselines.

## Completed Strong Evidence

### Action-Guard-Centered Controls

- `outputs/tuned_ablation_guard_only_nenv16_aggregate`: 3 seeds, n_envs=16, horizon=1500, 1M. High-density mean: success about 0.633, cost about 0.207, route about 0.868. This is the cleanest current guard+curriculum baseline.
- `outputs/tuned_compare_shield_only_nenv16_seed0_seed1_seed2_aggregate`: 3 seeds, n_envs=16, horizon=1500, 1M. High-density mean: success about 0.627, cost about 0.227, route about 0.871. This shows action guard alone is a dominant mechanism.

### Full Proposed / Retuned Full Proposed

- `outputs/candidate_lane1_out150_cost50_nenv16_aggregate`: older full proposed 3-seed aggregate; useful as historical full-risk baseline, but not the best current explanation.
- `outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed0_seed1_seed2_aggregate`: 3-seed retuned full method. Medium density improves, but high-density mean does not beat guard_only/shield_only and lane deviation is worse.
- `outputs/retune_proposed_ttc4_cost10_lane125_smooth003_accel0015_progress45_nenv16_seed1_seed2_diagnostic_aggregate`: 2-seed diagnostic. Fixes seed1 lateral deviation but degrades seed2 high-density robustness; do not expand to seed0.

### Reward/Component Ablations

- `outputs/tuned_ablation_wo_ttc_nenv16_seed0_seed1_seed2_aggregate`: 3 seeds. Removing TTC worsens dense-traffic mean versus full/guard baselines; supports TTC as a refinement, not the dominant factor.
- `outputs/tuned_ablation_wo_lane_nenv16_seed0_seed1_aggregate`: 2 seeds. Removing lane reward does not collapse success, but lane deviation is consistently high and high-density cost/route are weaker.
- `outputs/tuned_ablation_wo_smooth_nenv16_seed0_seed1_aggregate`: 2 seeds. Removing smooth/accel hurts medium/high-density stability.
- `outputs/tuned_ablation_no_action_guard_nenv16_seed0_1m`: seed0 only but already collapses badly. This is strong mechanism evidence that action guard is necessary; add seed1/2 only if the final paper requires symmetric multi-seed ablation tables.

## Active Runs

- `outputs/retune_guard_only_ttc12_v19_nenv16_seed1_1m`
- `outputs/retune_guard_only_ttc12_v19_nenv16_seed2_1m`

Purpose: guard-centered speed-target sensitivity. Promote only if seed1/2 improve high-density success or route versus guard_only ttc12/v18 same seeds while keeping d0.08 success/cost close. Reject if d0.08 degrades or high-density cost increases materially.

Current mid-run signal at 2026-06-30 23:42 CST:

- seed1 around 786k: stage2, window_cost about 0.067, window_route about 0.863, window_success about 0.267, rollout success_rate about 0.28. Continue.
- seed2 around 655k: stage3, window_cost about 0.233, window_route about 0.704, window_success about 0.100, rollout success_rate about 0.11. Continue, but this is a warning signal.

## Remaining Gaps

### Main Comparator Gap

Formal n_envs=16 baseline/curriculum/risk evidence is mostly seed0-level under `outputs/tuned_compare_*_nenv16_seed0_1m` and `outputs/iscsic_main_nenv16_v2`. If the final manuscript table requires full multi-seed comparator symmetry, run seed1/2 for baseline, curriculum, and risk. If space/time is limited, these can be framed as failed weak controls with seed0 plus historical n_envs=10/diagnostic evidence, but that is a weaker reviewer position.

### Ablation Symmetry Gap

`wo_lane` and `wo_smooth` currently have two seeds; `no_action_guard` has one seed. For a robust appendix table, add:

- `proposed_wo_lane` seed2 only if lane-deviation claim needs 3-seed symmetry.
- `proposed_wo_smooth` seed2 only if smoothness/stability claim needs 3-seed symmetry.
- `no_action_guard` seed1/2 only if reviewers may object that seed0 collapse is insufficient.

### Stress Evaluation Gap

After final candidate/baselines are frozen, run evaluation-only density stress at 0.20 and 0.25 for selected models only: guard_only, shield_only, best full proposed/retuned proposed, and baseline/risk if needed. Do not use stress results for retuning unless explicitly opening a new tuning round.

## Immediate Decision Rules

1. Wait for v19 seed1/2 summaries.
2. If v19 seed1/2 pass the gate, launch v19 seed0 and then write a three-seed aggregate.
3. If v19 fails or is mixed, keep default guard_only ttc12/v18 and shield_only as the main mechanism baselines.
4. Next after v19 should be either:
   - comparator completion: baseline/curriculum/risk seed1/2, or
   - ablation symmetry: no_action_guard seed1/2 and wo_lane/wo_smooth seed2.
5. Do not launch another full-risk reward retune until the current guard-centered branch is decided; previous full-risk retunes repeatedly failed to beat guard/shield.


## Update 2026-07-01: risk comparator completed
- Aggregate: `outputs/tuned_compare_risk_nenv16_seed0_seed1_seed2_aggregate`.
- Result: risk seed0/1/2 all failed as low-speed route stagnation, with mean success=0.000 at all densities and route completion about 0.009.
- Interpretation: this closes the risk-only comparator symmetry gap. Zero cost is not safety evidence because progress is near zero.
- Remaining comparator symmetry gaps: baseline seed1/2 and curriculum seed1/2.


## Update 2026-07-01: baseline comparator completed
- Aggregate: `outputs/tuned_compare_baseline_nenv16_seed0_seed1_seed2_aggregate`.
- Result: baseline seed0/1/2 mean success=0.000 and cost=1.000 at all densities, with route completion nonzero but dominated by collision/out_of_road.
- Remaining main-comparator symmetry gap: curriculum seed1/2.


## Update 2026-07-01: curriculum comparator completed
- Aggregate: `outputs/tuned_compare_curriculum_nenv16_seed0_seed1_seed2_aggregate`.
- Result: curriculum seed0/1/2 final held-out evaluation remains unsafe, with mean success near zero and cost near or at one across densities.
- Main comparator symmetry gap is closed for baseline, risk, curriculum, guard_only, shield_only, and full proposed aggregates.


## Update 2026-07-01: stress density evaluation completed
- Aggregate: `outputs/stress_density_020_025_nenv16_20260701_0153/aggregate`.
- Result: at d0.20 shield_only is strongest by mean success; at d0.25 guard_only is the cleanest survivor. Full proposed and retuned full proposed do not dominate guard/shield under stress.
- Interpretation: this closes the planned 0.20/0.25 stress-evaluation gap for selected frozen models. It supports action-guard-centered robustness, not risk-reward dominance.
- Next evidence gap, if more work is needed: paper-table packaging and optional final method naming/reframing; avoid another reward retune unless opening a new tuning round with a clearly different mechanism.
