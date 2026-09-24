# Reviewer Statistics Notes

Time: 2026-07-01T04:04:23+08:00

## What these tables are

- `seed_level_robustness_formal.csv`: seed-level mean/std/min/max for formal densities 0.00/0.08/0.15.
- `seed_paired_deltas_vs_guard_shield.csv`: paired seed deltas versus guard_only and shield_only for key variants and ablations.
- `seed_level_robustness_stress.csv`: seed-level robustness for stress densities 0.20/0.25.

## Interpretation boundary

These tables deliberately treat seed as the replication unit. Episode-level rows are not treated as independent statistical replicates for method claims. With n=3 seeds, use these tables for robustness and reviewer transparency, not for aggressive significance claims.

## Current statistical reading

- Guard/shield remain the most defensible main mechanism: their seed-level means are high and their stress behavior is strongest or near strongest.
- `proposed_gated_risk` is a useful mechanism addendum because it avoids risk-only stagnation and is competitive under stress, especially at density 0.25.
- `retuned_full_proposed` and `proposed_gated_risk` do not consistently dominate guard_only/shield_only across seeds and densities, so the manuscript should not claim risk-reward dominance.

## External Seed Robustness Wilson Intervals

Added on 2026-07-01T08:40:30+08:00. `external_seed_robustness_wilson95.csv` reports episode-level Wilson 95% intervals for success and cost using the completed external seed sweep (`test_start_seed=20000/30000`, train seeds 0/1/2, 50 episodes per unit, `n_envs=16`). `external_seed_robustness_d015_wilson95.csv` is the hard-density subset for reviewer-facing robustness discussion.

At density 0.15, the ranking remains shield/guard centered: shield_only has the highest success estimate, proposed_gated_risk is competitive and above guard_only by success, while no_action_guard and risk_only remain negative controls for distinct failure modes. These intervals should be used as uncertainty context, not as a claim of statistical superiority over shield_only.

