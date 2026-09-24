# Writing Rationale Matrix

| Section | Rationale | Evidence | Claim boundary | Status |
|---|---|---|---|---|
| Introduction | Reframe short-paper method as cybernetic runtime feedback for IJMLC fit | IJMLC scope, framework files | No formal safety claim | drafted |
| Related Work | Position against safe RL, shielding, RSS/TTC, simulation artifacts | Working bibliography, code evidence | Bibliography should be externally citation-checked before submission | drafted |
| Method | Describe actual implementation from `racrl/envs.py` and diagnostics script | TTC thresholds, speed guard, gated risk reward | Heuristic runtime intervention, not CBF/RSS proof | drafted |
| Experiments | Explain P1/P2/P4/P5/CI matrix and supervision | `IJMLC_FINAL_EVIDENCE_MANIFEST.md` | Diagnostic shards differ from standard n_envs=16 path by design | drafted |
| Results | Tie each RQ to one table/figure and exact numeric values | table3/4/6/7, sensitivity, CI | Simulation-only | drafted |
| Discussion | State mechanism and limits directly | P3 decision, runtime table, density degradation | No real-world/certified claims | drafted |
| Declarations | Add Springer-required data/code/competing/funding/author sections | Official Springer submission guidelines | Author/funding fields need final author-team confirmation | drafted |
