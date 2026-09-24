# Decision: defensive ttc14/v18 nenv16 tuning aggregate

Time: 2026-07-01T08:44:46+08:00

## Protocol

- Source root: outputs/defensive_ttc14_v18_nenv16_tuning.
- Variant: defensive proposed with ttc_threshold=14.0 and target_speed_kmh=18.0.
- Seeds: 26, 27, 28.
- Training/evaluation parallelism: n_envs=16.
- Evaluation: 50 episodes per density; densities 0.00, 0.08, 0.15.

## Three-seed mean

- d0.08: success=0.867, cost=0.093; ttc12/v18 same branch was success=0.873, cost=0.080.
- d0.15: success=0.573, cost=0.260, route=0.839; ttc12/v18 was success=0.567, cost=0.273.

## Decision

diagnostic only: does not pass the combined formal gate.

Interpretation: raising the TTC threshold from 12 to 14 slightly improves high-density cost relative to ttc12/v18, but success remains below the 0.60 minimum gate and medium-density is not better. This branch should remain diagnostic/parameter-sensitivity evidence, not a promoted paper result.

The broader evidence package still favors action guard/shield as the dominant mechanism, with tuned/full/gated variants framed as refinements.

## Files

- aggregate/summary_by_seed_density.csv
- aggregate/mean_by_density.csv
- aggregate/std_by_density.csv
- aggregate/compare_to_ttc12_v18.csv
