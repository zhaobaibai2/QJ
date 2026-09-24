# External Seed Robustness Addendum

Updated: 2026-07-01T08:39:24+08:00

## Protocol

- Source root: `outputs/external_seed_robustness_nenv16_20260701_0425`.
- Models: frozen accepted/diagnostic models, no retraining in this sweep.
- Train seeds: 0, 1, 2 for each label.
- External scenario seeds: `test_start_seed=20000` and `30000`.
- Densities: 0.08 and 0.15.
- Episodes: 50 per density per train seed per external scenario seed, giving 300 episodes per label-density aggregate.
- Evaluation parallelism: `n_envs=16`.

## Density 0.15 Ranking

- 1. shield_only: success=0.687, cost=0.207, route=0.878, episodes=300
- 2. proposed_gated_risk: success=0.663, cost=0.213, route=0.866, episodes=300
- 3. guard_only: success=0.613, cost=0.240, route=0.852, episodes=300
- 4. retuned_full: success=0.597, cost=0.280, route=0.838, episodes=300
- 5. no_action_guard: success=0.000, cost=1.000, route=0.191, episodes=300
- 6. risk_only: success=0.000, cost=0.000, route=0.009, episodes=300

## Decision

This sweep supports the guard/shield-centered manuscript line under external scenario seeds. `shield_only`, `proposed_gated_risk`, and `guard_only` remain far ahead of the negative controls at density 0.15. `proposed_gated_risk` is competitive and improves over risk-only stagnation, but it still should be framed as a refinement/addendum rather than as statistically dominant over shield-only.

`risk_only` has near-zero cost only because route completion collapses, so it must not be described as a safe successful controller. `no_action_guard` confirms the action-level guard/shield is structurally necessary: success is zero and cost is 1.0 under both external seed blocks.

## Files Written for Paper Use

- `external_seed_robustness_mean.csv`: label-density aggregate.
- `external_seed_robustness_rank_d015.csv`: density 0.15 ordered table.
- `external_seed_robustness_by_test_start.csv`: external-seed split table.
- `external_seed_robustness_eval_units.csv`: label/train-seed/test-start/density units.
- `../final_paper_manifest_20260701_0415/table4_external_seed_robustness.csv`: manifest copy.

## Claim Boundary

Use this as reviewer-facing robustness validation of the frozen final evidence package. It is not training evidence, not a new tuning branch, and not a reason to reopen reward-only retuning. If the manuscript names a single method, the safest wording is that the action guard/shield mechanism is the dominant stabilizer and gated risk is a useful refinement.
