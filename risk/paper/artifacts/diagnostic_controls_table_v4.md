# Diagnostic controls moved out of main promotion tables (V4)

These rows were not deleted from the evidence record. They were moved out of the main promotion/ranking tables because they are non-competitive failure diagnostics and visually over-weighted the 0% success cases.

| Source block | Variant | Density | Success (%) | Cost (%) | Route | Reason kept as diagnostic |
|---|---:|---:|---:|---:|---:|---|
| Primary d=0.15 | PPO baseline | 0.15 | 0.0 | 100.0 | 0.190 | lower-bound unsafe control |
| Primary d=0.15 | Curriculum PPO | 0.15 | 0.0 | 100.0 | 0.177 | curriculum-only lower bound |
| Primary d=0.15 | Risk reward only | 0.15 | 0.0 | 0.0 | 0.009 | non-driving zero-cost artifact |
| Primary d=0.15 | No action guard | 0.15 | 0.0 | 100.0 | 0.172 | mechanism-removal collapse |
| External d=0.15 | Risk reward only | 0.15 | 0.0 [0.0, 1.3] | 0.0 [0.0, 1.3] | 0.009 | non-driving zero-cost artifact |
| External d=0.15 | No action guard | 0.15 | 0.0 [0.0, 1.3] | 100.0 [98.7, 100.0] | 0.191 | mechanism-removal collapse |
| Stress d=0.20 | Risk reward only | 0.20 | 0.0 | 0.0 | 0.009 | non-driving zero-cost artifact |
| Stress d=0.25 | Risk reward only | 0.25 | 0.0 | 0.0 | 0.009 | non-driving zero-cost artifact |

Main-paper consequence: Tables II, III, V, VI, and VII now show competitive or mechanism-relevant rows instead of repeatedly ending with visually artificial 0% success blocks. Table IV still keeps the no-action-guard collapse because that is the direct mechanism ablation.
