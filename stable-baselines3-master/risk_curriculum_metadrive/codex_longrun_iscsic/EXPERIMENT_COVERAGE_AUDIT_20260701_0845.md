# EXPERIMENT_COVERAGE_AUDIT_20260701_0845

Time: 2026-07-01T08:39:24+08:00

## Runtime State

- No active training or evaluation process was found during the 08:36-08:45 CST checks.
- GPU was available with only desktop/remote-display usage; no MetaDrive Python job was consuming CUDA.
- Current authoritative project root: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive`.
- Wider `/home/aaa/data/qj` scan found no separate active `iscsic2026_metadrive_riskgate`/CAR-Gate code or result tree; current experiment supervision should therefore use this project as the source of truth.

## Completed Paper Evidence

- Main/comparator evidence: `codex_longrun_iscsic/paper_tables_20260701_0258/main_comparators_nenv16.csv`.
- Ablation evidence: `codex_longrun_iscsic/paper_tables_20260701_0258/ablation_mechanism_nenv16.csv`.
- Stress evidence: `codex_longrun_iscsic/paper_tables_20260701_0258/stress_density_020_025.csv` and gated-risk stress addendum.
- Behavior/trajectory evidence: `codex_longrun_iscsic/behavior_rollouts_20260701_0406`.
- Final manifest: `codex_longrun_iscsic/final_paper_manifest_20260701_0415`.
- External seed robustness: `outputs/external_seed_robustness_nenv16_20260701_0425` and `codex_longrun_iscsic/paper_tables_20260701_0258/external_seed_robustness_addendum.md`.

## Latest External Seed Result

At density 0.15 over 300 episodes per label, external scenario-seed ranking is:

- 1. shield_only: success=0.687, cost=0.207, route=0.878, episodes=300
- 2. proposed_gated_risk: success=0.663, cost=0.213, route=0.866, episodes=300
- 3. guard_only: success=0.613, cost=0.240, route=0.852, episodes=300
- 4. retuned_full: success=0.597, cost=0.280, route=0.838, episodes=300
- 5. no_action_guard: success=0.000, cost=1.000, route=0.191, episodes=300
- 6. risk_only: success=0.000, cost=0.000, route=0.009, episodes=300

## Decision

Do not start another reward-only tuning branch now. The latest evidence is already sufficient for a conservative paper line: action guard/shield is the dominant stabilizing mechanism; gated risk is a viable refinement; risk-only and no-action-guard are negative controls. The next useful work is manuscript/table/figure packaging or, if more validation is needed, narrowly scoped reviewer-facing checks that do not change the frozen protocol.
