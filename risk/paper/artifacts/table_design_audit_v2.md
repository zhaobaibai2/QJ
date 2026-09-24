# Table Design Audit V2

Overall verdict: PASS

| Check | Status | Evidence |
|---|---|---|
| No directory/file-inventory table in manuscript body | PASS | `main.tex` inputs only protocol and experiment-result tables. |
| One table, one scientific message | PASS | Protocol, primary comparison, density sweep, ablation, external CI, stress, seed robustness, and parameter sensitivity are separated. |
| Metric directions shown | PASS | Headers use `↑`/`↓` notation in every result table. |
| Best/second-best marking not misleading | PASS | Main table does not highlight risk-only zero cost because it does not drive. |
| Deltas shown for ablation | PASS | Table IV reports deltas relative to action-guard reference. |
| Confidence intervals explicit | PASS | External-seed table reports Wilson 95% intervals. |
| Directory provenance retained outside results | PASS | Inventory CSVs remain in `artifacts/`, not in manuscript result tables. |
| Seed-label alias checked | PASS | `retuned_full_proposed` is explicitly mapped to the retuned full display row for seed robustness. |
