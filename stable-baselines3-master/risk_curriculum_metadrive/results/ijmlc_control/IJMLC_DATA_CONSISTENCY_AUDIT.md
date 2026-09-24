# IJMLC Data Consistency Audit

This audit records the data checks requested before the IJMLC journal revision. It is generated from current CSVs and run manifests, not from manuscript prose.

## 1. PPO success=0 provenance

- Core Table 3 PPO row: success=0.0%, cost=100.0%, route=20.7%, episodes=120, train_seeds=3.
- External Table 5 PPO row matches the same unshielded PPO row: success=0.0%, cost=100.0%, route=20.7%.
- Density Table 6 PPO rows are consistently 0.0% success across densities 0.08, 0.15, 0.20, 0.25; this is not a single-table typo.
- Source: `summary_tables/p1_all_density_core_aggregate.csv` built from `raw_csv/p1_all_density_core_episodes.csv`.
- Formal PPO backbone checkpoints in manifest: 3 seeds, n_envs=[np.int64(16)], timesteps=[np.int64(1000000)].
- Manuscript action: name the row as an unshielded PPO backbone/policy without runtime intervention, and state it is a dense-protocol lower-bound comparator rather than a deliberately weakened SOTA baseline.

## 2. RSS/TTC filter source

- RSS/TTC filter row: success=53.3%, cost=44.2%, route=78.9%, interventions=71.7/100 steps.
- Run manifests record `action_filter=rss_ttc` and use frozen-model diagnostic evaluation, so the manuscript should describe this as a classical runtime filter applied to the same PPO backbone family, not as an independently trained policy.

## 3. Sensitivity default-cell consistency

- The TTC-threshold sensitivity sweep is an independent diagnostic rerun using the same nominal seeds/start-seeds but separate run manifests. It should be interpreted as trend evidence, not as an exact duplicate of Table 3.
- Guard: threshold=10 minus core -> success +6.7 pp, cost +0.0 pp, route +0.5 pp.
- Shield: threshold=10 minus core -> success -3.3 pp, cost +5.8 pp, route +0.0 pp.
- Gated-risk: threshold=10 minus core -> success -4.2 pp, cost +10.8 pp, route -1.9 pp.
- Manuscript action: explicitly state the independent rerun boundary in Section 5.5 and avoid claiming the default sensitivity cell exactly reproduces Table 3.

## 4. Episode accounting

- Each formal density-0.15 comparison row aggregates 120 diagnostic episodes from 3 train seeds and 40 diagnostic episodes per train seed.
- Evidence-volume totals in manifest tables are aggregate row sums and should not be presented as unique simulator episodes in main-text claims.

## 5. Requested manuscript edits implied by audit

- Use bounded baseline language for PPO and PPO-Lagrangian / RCPO-style Lagrangian.
- Keep RSS/TTC as a meaningful comparator and note that its intervention rate is comparable to Guard/Shield/Gated-risk.
- Move step-level representative traces to a future logging/action item unless actual step-level traces are found; current raw CSVs are episode-level.
