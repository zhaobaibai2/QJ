# V4 table data audit

Audit scope: Tables I--VIII and Figures 3, 4, 6, and 7 were checked against the remote CSV evidence package before V4 formatting changes. No numeric values were fabricated or improved; rows were only filtered between main ranking tables and diagnostic audit artifacts.

Key checked values:

- Table II primary d=0.15: Ours-Guard 63.3% success, 20.7% cost, 0.868 route; Ours-Shield 62.7% success, 22.7% cost, 0.871 route.
- Table III density sweep: Ours-Guard is best at formal d=0.15 success/cost; Ours-Shield is best at d=0.00 and d=0.08 success and has the best d=0.15 route.
- Table IV ablation: removing action guard remains 0.0% success and 100.0% cost; this row stays in the ablation table because it is the mechanism-collapse evidence.
- Table V external seeds: Ours-Shield 68.7% success with Wilson 95% CI [63.2, 73.7], highest mean in the external-seed block.
- Table VI stress: Ours-Shield leads d=0.20 success/cost/route; Ours-Guard leads d=0.25 success/cost/route among moving variants.
- Table VII seed robustness file now reports only competitive variants.
- Table VIII parameter sensitivity file is unchanged in values; it remains a model-selection closure artifact, while the main text uses Fig. 8 for the concise frontier.

Design decision: failure controls with repeated 0% success are scientifically retained but no longer over-displayed in the main promotion tables.
